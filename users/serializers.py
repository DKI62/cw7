from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    telegram_id = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'telegram_id']
        extra_kwargs = {'email': {'required': False}}  # Делаем email необязательным

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Хешируем пароль
        user = CustomUser.objects.create(**validated_data)
        return user
