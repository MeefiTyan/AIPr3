from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler,
    ContextTypes, filters
)

# ---- STATES ----
CHOOSE_FLOWER, ASK_PRICE, ASK_COLOR, ASK_COUNT, CONFIRM_ORDER, \
ASK_NAME, ASK_SURNAME, ASK_PHONE, ASK_EMAIL, ASK_ADDRESS, CONFIRM_DATA = range(11)

# ---- FLOWER LIST ----
FLOWERS = [
    "Троянда",
    "Ромашка",
    "Тюльпан",
    "Лілія",
    "Орхідея",
    "Хризантема",
    "Гортензія"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[flower] for flower in FLOWERS]
    await update.message.reply_text(
        "Оберіть квітку:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return CHOOSE_FLOWER

async def choose_flower(update: Update, context: ContextTypes.DEFAULT_TYPE):
    flower = update.message.text
    if flower not in FLOWERS:
        await update.message.reply_text("Оберіть квітку зі списку.")
        return CHOOSE_FLOWER

    context.user_data['flower'] = flower
    await update.message.reply_text("Вкажіть суму замовлення (грн):")
    return ASK_PRICE

async def ask_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['price'] = update.message.text
    await update.message.reply_text("Вкажіть бажаний колір:")
    return ASK_COLOR

async def ask_color(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['color'] = update.message.text
    await update.message.reply_text("Вкажіть кількість квітів:")
    return ASK_COUNT

async def ask_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['count'] = update.message.text

    flower = context.user_data['flower']
    price = context.user_data['price']
    color = context.user_data['color']
    count = context.user_data['count']

    summary = (
        f"Перевірте замовлення:\n"
        f"Квітка: {flower}\n"
        f"Сума: {price} грн\n"
        f"Колір: {color}\n"
        f"Кількість: {count}\n\n"
        "Все вірно? (так/ні)"
    )
    await update.message.reply_text(summary)
    return CONFIRM_ORDER

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower() != "так":
        await update.message.reply_text("Замовлення скасовано")
        return ConversationHandler.END

    await update.message.reply_text("Введіть ім'я:")
    return ASK_NAME

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Введіть прізвище:")
    return ASK_SURNAME

async def ask_surname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['surname'] = update.message.text
    await update.message.reply_text("Введіть номер телефону:")
    return ASK_PHONE

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("Введіть Email:")
    return ASK_EMAIL

async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['email'] = update.message.text
    await update.message.reply_text("Введіть адресу доставки:")
    return ASK_ADDRESS

async def ask_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['address'] = update.message.text

    data = context.user_data

    summary = (
        "Перевірте дані:\n"
        f"Ім'я: {data['name']}\n"
        f"Прізвище: {data['surname']}\n"
        f"Телефон: {data['phone']}\n"
        f"Email: {data['email']}\n"
        f"Адреса: {data['address']}\n\n"
        "Все вірно? (так/ні)"
    )

    await update.message.reply_text(summary)
    return CONFIRM_DATA

async def confirm_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower() != "так":
        await update.message.reply_text("Замовлення скасовано")
        return ConversationHandler.END

    await update.message.reply_text("Дякуємо за замовлення! Гарного дня та до побачення!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Замовлення скасовано")
    return ConversationHandler.END


def main():
    app = Application.builder().token("8266036717:AAG5BeHxUNmGc9G_EMhh8f4b_WxZMW_rB-g").build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE_FLOWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_flower)],
            ASK_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_price)],
            ASK_COLOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_color)],
            ASK_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_count)],
            CONFIRM_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_order)],

            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_surname)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)],
            ASK_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_address)],
            CONFIRM_DATA: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_data)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()
