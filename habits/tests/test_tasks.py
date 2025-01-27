import pytest
from django.contrib.auth.models import User
from habits.models import Habit
from datetime import datetime, time


@pytest.mark.django_db
def test_send_habit_reminders(mocker):
    user = User.objects.create(username="test_user")

    # Устанавливаем точное время
    Habit.objects.create(
        user=user,
        action="Test Habit",
        time=time(12, 0),
        place="Test Place",
        telegram_user_id="123456"
    )

    print(f"Привычки перед тестом: {list(Habit.objects.values())}")

    # Мокаем Telegram Bot
    mock_bot = mocker.patch('habits.tasks.Bot')
    mock_send_message = mocker.AsyncMock()  # Используем AsyncMock для асинхронного метода
    mock_bot.return_value.send_message = mock_send_message

    # Мокаем datetime
    mock_now = mocker.patch('habits.tasks.datetime')
    mock_now.now.return_value = datetime(2025, 1, 27, 12, 0, 0)
    mock_now.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

    # Вызываем задачу
    from habits.tasks import send_habit_reminders
    send_habit_reminders()

    # Проверяем, что сообщение отправлено
    mock_send_message.assert_called_once_with(
        chat_id="123456",
        text="Напоминание о привычке: Test Habit в Test Place"
    )
