import pytest
from habits.serializers import HabitSerializer
from users.models import CustomUser


@pytest.mark.django_db
def test_habit_serializer_valid():
    user = CustomUser.objects.create_user(username="testuser", password="password")
    data = {
        "user": user.id,
        "action": "Test Habit",
        "time": "08:00:00",
        "place": "Home",
        "is_pleasant": True,
        "frequency": 1
    }
    serializer = HabitSerializer(data=data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_habit_serializer_invalid():
    data = {
        "action": "",
        "time": "08:00:00",
        "place": "",
        "frequency": 0
    }
    serializer = HabitSerializer(data=data)
    assert not serializer.is_valid()
    assert "action" in serializer.errors
    assert "place" in serializer.errors
