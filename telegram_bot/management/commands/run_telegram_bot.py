from django.core.management.base import BaseCommand
from telegram_bot.bot import run_bot


class Command(BaseCommand):
    help = "Запуск Telegram-бота"

    def handle(self, *args, **kwargs):
        self.stdout.write("Запуск Telegram-бота...")
        run_bot()
