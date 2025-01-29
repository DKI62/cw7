import pytest
from users.models import CustomUser as User, CustomUser
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


@pytest.mark.django_db
def test_habit_clean():
    user = CustomUser.objects.create_user(username="testuser", password="password")
    habit = Habit(
        user=user,
        action="Test Habit",
        time=time(8, 0),
        place="Home",
        reward="Chocolate",
        related_habit=None,
        is_pleasant=False
    )
    habit.clean()

    habit.frequency = 0
    with pytest.raises(ValidationError):
        habit.clean()


@pytest.mark.django_db
def test_related_habit_must_be_pleasant():
    """Проверяем, что в связанные привычки можно добавить только приятные привычки."""
    user = CustomUser.objects.create(username="test_user")

    pleasant_habit = Habit.objects.create(
        user=user, action="Drink Tea", time=time(10, 0), place="Kitchen", is_pleasant=True
    )

    not_pleasant_habit = Habit.objects.create(
        user=user, action="Run 5km", time=time(7, 0), place="Park", is_pleasant=False
    )

    habit = Habit(
        user=user, action="Morning Walk", time=time(8, 0), place="Street", related_habit=not_pleasant_habit
    )

    with pytest.raises(ValidationError, match="Связанная привычка должна быть только с признаком приятной привычки!"):
        habit.clean()  # Ожидаем ошибку

    # Теперь проверяем, что с приятной привычкой ошибки нет
    habit.related_habit = pleasant_habit
    habit.clean()
