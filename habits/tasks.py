import asyncio
from celery import shared_task
from telegram import Bot
from django.conf import settings
from datetime import datetime
from .models import Habit


@shared_task
def send_habit_reminders():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    now = datetime.now().time().replace(microsecond=0)  # Убираем микросекунды
    print(f"Текущее время: {now}")  # Лог текущего времени

    # Получаем привычки синхронно
    habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute).select_related("user")
    print(f"Найдено привычек: {len(habits)}")

    async def send_message_async(chat_id, text):
        print(f"Отправка сообщения для {chat_id}: {text}")  # Лог отправки
        await bot.send_message(chat_id=chat_id, text=text)

    async def main():
        tasks = []
        for habit in habits:
            # Убеждаемся, что у пользователя есть Telegram ID
            if habit.user.telegram_id:
                message = f"Напоминание о привычке: {habit.action} в {habit.place}"
                tasks.append(send_message_async(habit.user.telegram_id, message))
        if tasks:
            await asyncio.gather(*tasks)

    # Запускаем асинхронный цикл
    asyncio.run(main())
