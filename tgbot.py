from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
import random

# Опції гри
CHOICES = ["Камінь", "Ножиці", "Папір"]

# Збереження очок і рекордів для кожного користувача
user_scores = {}

# Функція для оновлення рекорду
def update_record(user_id):
    if user_scores[user_id]['score'] > user_scores[user_id]['record']:
        user_scores[user_id]['record'] = user_scores[user_id]['score']

# Стартова команда або кнопка "Старт"
async def start(update: Update, context):
    user_id = update.effective_user.id

    # Ініціалізація очок, якщо користувач запускає гру вперше
    if user_id not in user_scores:
        user_scores[user_id] = {"score": 0, "record": 0}

    keyboard = [
        [InlineKeyboardButton("Камінь", callback_data="Камінь")],
        [InlineKeyboardButton("Ножиці", callback_data="Ножиці")],
        [InlineKeyboardButton("Папір", callback_data="Папір")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Граймо! Обери свій хід:\n"
        f"Твій рахунок: {user_scores[user_id]['score']} | Рекорд: {user_scores[user_id]['record']}",
        reply_markup=reply_markup
    )

# Обробник вибору
async def handle_choice(update: Update, context):
    user_id = update.effective_user.id
    user_choice = update.callback_query.data
    bot_choice = random.choice(CHOICES)

    # Логіка визначення переможця
    if user_choice == bot_choice:
        result = f"Нічия! Ми обидва обрали {user_choice}."
    elif (user_choice == "Камінь" and bot_choice == "Ножиці") or \
         (user_choice == "Ножиці" and bot_choice == "Папір") or \
         (user_choice == "Папір" and bot_choice == "Камінь"):
        user_scores[user_id]['score'] += 1  # Додати очко
        update_record(user_id)  # Оновити рекорд
        result = f"Ти виграв! 🎉 Я обрав {bot_choice}, а ти — {user_choice}.\n" \
                 f"Твій рахунок: {user_scores[user_id]['score']} | Рекорд: {user_scores[user_id]['record']}."
    else:
        user_scores[user_id]['score'] = 0  # Скинути очки
        result = f"Ти програв! 😜 Я обрав {bot_choice}, а ти — {user_choice}.\n" \
                 f"Твій рахунок обнулено. Рекорд: {user_scores[user_id]['record']}."

    # Додати кнопку "Старт" та відправити результат
    keyboard = [
        [InlineKeyboardButton("Камінь", callback_data="Камінь")],
        [InlineKeyboardButton("Ножиці", callback_data="Ножиці")],
        [InlineKeyboardButton("Папір", callback_data="Папір")],
        [InlineKeyboardButton("Старт", callback_data="restart")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(result, reply_markup=reply_markup)

# Обробник кнопки "Старт"
async def restart(update: Update, context):
    user_id = update.effective_user.id

    # Ініціалізація очок, якщо користувача ще немає у словнику
    if user_id not in user_scores:
        user_scores[user_id] = {"score": 0, "record": 0}

    # Обнулити рахунок користувача
    user_scores[user_id]['score'] = 0

    keyboard = [
        [InlineKeyboardButton("Камінь", callback_data="Камінь")],
        [InlineKeyboardButton("Ножиці", callback_data="Ножиці")],
        [InlineKeyboardButton("Папір", callback_data="Папір")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        f"Гру перезапущено! Почнемо знову.\n"
        f"Твій рахунок: {user_scores[user_id]['score']} | Рекорд: {user_scores[user_id]['record']}",
        reply_markup=reply_markup
    )

# Головна кнопка "Старт" після запуску бота
async def show_start_button(update: Update, context):
    keyboard = [[InlineKeyboardButton("Старт", callback_data="restart")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Натисни 'Старт', щоб почати гру:", reply_markup=reply_markup)

# Налаштування бота
def main():
    app = ApplicationBuilder().token("8051441469:AAEXltyEuklWvaVBsQrvbuMm5dldCSohjzA").build()

    app.add_handler(CommandHandler("start", show_start_button))  # Головна кнопка "Старт"
    app.add_handler(CallbackQueryHandler(handle_choice, pattern="^(Камінь|Ножиці|Папір)$"))
    app.add_handler(CallbackQueryHandler(restart, pattern="^restart$"))

    print("Бот запущено!")
    app.run_polling()  # Запуск бота

if __name__ == "__main__":
    main()

