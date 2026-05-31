from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = "7955497495:AAHbNb4kvca1oGVzRMZ9saiZkZoJyCeyIWE"

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🚗 Обрати автомобіль", callback_data="cars")],
        [InlineKeyboardButton("⭐ Відгуки", callback_data="reviews")]
    ]

    await update.message.reply_text(
        "🚘 Ласкаво просимо до сервісу оренди автомобілів!\n\nОберіть опцію:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "cars":

        keyboard = []

        for i in range(1, 16):
            keyboard.append([
                InlineKeyboardButton(
                    f"🚘 Car{i}",
                    callback_data=f"car{i}"
                )
            ])

        keyboard.append([
            InlineKeyboardButton("🏠 Головне меню", callback_data="home")
        ])

        await query.edit_message_text(
            "🚗 Оберіть автомобіль:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "home":

        keyboard = [
            [InlineKeyboardButton("🚗 Обрати автомобіль", callback_data="cars")],
            [InlineKeyboardButton("⭐ Відгуки", callback_data="reviews")]
        ]

        await query.edit_message_text(
            "🏠 Головне меню",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "reviews":

        keyboard = [
            [InlineKeyboardButton("🏠 Головне меню", callback_data="home")]
        ]

        await query.edit_message_text(
            "⭐ Відгуки клієнтів\n\n"
            "⭐⭐⭐⭐⭐ Дуже хороший сервіс!\n\n"
            "⭐⭐⭐⭐⭐ Швидке бронювання!\n\n"
            "⭐⭐⭐⭐⭐ Рекомендую!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data.startswith("car"):

        car = query.data.upper()

        users[user_id] = {
            "car": car,
            "step": "name"
        }

        await query.message.reply_text(
            f"✅ Ви обрали {car}\n\n"
            f"👤 Введіть ваше ім'я:"
        )

async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in users:
        return

    step = users[user_id]["step"]

    if step == "name":

        users[user_id]["name"] = update.message.text
        users[user_id]["step"] = "date"

        await update.message.reply_text(
            "📅 Введіть дату оренди\n\nНаприклад: 15.07.2026"
        )

    elif step == "date":

        users[user_id]["date"] = update.message.text

        await update.message.reply_text(
            f"🎉 Заявка успішно створена!\n\n"
            f"🚘 Автомобіль: {users[user_id]['car']}\n"
            f"👤 Ім'я: {users[user_id]['name']}\n"
            f"📅 Дата: {users[user_id]['date']}\n\n"
            f"📞 Наш менеджер зв'яжеться з вами найближчим часом."
        )

        del users[user_id]

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, messages)
    )

    print("Bot started")

    app.run_polling()

if __name__ == "__main__":
    main()