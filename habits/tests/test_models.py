import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from habits.models import Habit
from datetime import time


@pytest.mark.django_db
def test_habit_creation():
    user = User.objects.create_user(username="testuser", password="password")
    habit = Habit.objects.create(
        user=user,
        action="Читать книгу",
        time=time(20, 0),
        place="Дом",
        is_pleasant=False,
        reward="Посмотреть фильм",
        frequency=1,
        estimated_time=120,
        is_public=True,
    )
    assert habit.action == "Читать книгу"
    assert habit.is_public is True


@pytest.mark.django_db
def test_habit_validation_error():
    user = User.objects.create_user(username="testuser", password="password")
    habit = Habit(
        user=user,
        action="Читать книгу",
        time=time(20, 0),
        place="Дом",
        is_pleasant=False,
        reward="Посмотреть фильм",
        frequency=15,  # Ошибка: периодичность больше 7
        estimated_time=120,
        is_public=True,
    )
    with pytest.raises(ValidationError):
        habit.full_clean()  # Проверка валидаторов
