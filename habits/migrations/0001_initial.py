# Generated by Django 5.1.5 on 2025-01-26 18:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(help_text='Действие, которое представляет привычка', max_length=255)),
                ('time', models.TimeField(help_text='Время выполнения привычки')),
                ('place', models.CharField(help_text='Место выполнения привычки', max_length=255)),
                ('is_pleasant', models.BooleanField(default=False, help_text='Это приятная привычка?')),
                ('reward', models.CharField(blank=True, help_text='Вознаграждение за выполнение привычки', max_length=255, null=True)),
                ('frequency', models.PositiveIntegerField(default=1, help_text='Периодичность выполнения привычки (в днях)')),
                ('estimated_time', models.PositiveIntegerField(default=120, help_text='Время на выполнение (в секундах, не более 120)')),
                ('is_public', models.BooleanField(default=False, help_text='Можно ли публиковать привычку для общего доступа')),
                ('related_habit', models.ForeignKey(blank=True, help_text='Связанная привычка (только для полезных привычек)', limit_choices_to={'is_pleasant': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='habits.habit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habits', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
