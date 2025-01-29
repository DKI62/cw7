from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    telegram_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="ID пользователя в Telegram"
    )

    def __str__(self):
        return self.username
