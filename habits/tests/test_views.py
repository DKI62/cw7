import pytest
from rest_framework.test import APIClient
from users.models import CustomUser as User
from habits.models import Habit


@pytest.mark.django_db
def test_habit_list_authenticated():
    user = User.objects.create_user(username="testuser", password="password")
    Habit.objects.create(
        user=user,
        action="Читать книгу",
        time="20:00:00",
        place="Дом",
        is_public=True,
    )

    client = APIClient()
    client.login(username="testuser", password="password")
    response = client.get("/api/habits/")

    assert response.status_code == 200
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_habit_list_unauthenticated():
    user = User.objects.create_user(username="testuser", password="password")
    Habit.objects.create(
        user=user,
        action="Читать книгу",
        time="20:00:00",
        place="Дом",
        is_public=True,
    )

    client = APIClient()
    response = client.get("/api/habits/")

    assert response.status_code == 200
    assert len(response.data["results"]) == 1
