from django.conf import settings
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    action = models.CharField(max_length=255, help_text="Действие, которое представляет привычка")
    time = models.TimeField(help_text="Время выполнения привычки")
    place = models.CharField(max_length=255, help_text="Место выполнения привычки")
    is_pleasant = models.BooleanField(default=False, help_text="Это приятная привычка?")
    related_habit = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Связанная привычка (только для полезных привычек)",
        limit_choices_to={'is_pleasant': True},
    )
    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Вознаграждение за выполнение привычки"
    )
    frequency = models.PositiveIntegerField(default=1, help_text="Периодичность выполнения привычки (в днях)")
    estimated_time = models.PositiveIntegerField(
        default=120,
        help_text="Время на выполнение (в секундах, не более 120)"
    )
    is_public = models.BooleanField(default=False, help_text="Можно ли публиковать привычку для общего доступа")

    def __str__(self):
        return f"{self.action} ({'приятная' if self.is_pleasant else 'полезная'})"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.reward and self.related_habit:
            raise ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")

        if self.estimated_time > 120:
            raise ValidationError("Время выполнения привычки не может превышать 120 секунд.")

        if self.frequency < 1 or self.frequency > 7:
            raise ValidationError("Периодичность выполнения привычки должна быть от 1 до 7 дней.")

        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("Приятная привычка не может иметь вознаграждения или связанных привычек.")

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть только с признаком приятной привычки!")

    class Meta:
        ordering = ['id']  # Сортировка по ID


def __str__(self):
    return f"{self.action} ({'приятная' if self.is_pleasant else 'полезная'})"
