import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ваш бот для отслеживания привычек.")


# Основная функция запуска бота
def run_bot():
    from django.conf import settings

    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Регистрация команды /start
    application.add_handler(CommandHandler("start", start))

    # Запуск бота
    application.run_polling()
