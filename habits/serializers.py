from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)

    def validate_frequency(self, value):
        if value < 1 or value > 7:
            raise serializers.ValidationError("Периодичность выполнения привычки должна быть от 1 до 7 дней.")
        return value

    def validate_estimated_time(self, value):
        if value > 120:
            raise serializers.ValidationError("Время выполнения привычки не может превышать 120 секунд.")
        return value

    def validate(self, data):
        # Проверяем связанные привычки
        related_habit = data.get('related_habit')
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной.")

        # Проверяем приятные привычки
        if data.get('is_pleasant') and (data.get('reward') or data.get('related_habit')):
            raise serializers.ValidationError("Приятная привычка не может иметь вознаграждения или связанных привычек.")
        return data

    def validate_related_habit(self, value):
        if value and not value.is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной!")
        return value
