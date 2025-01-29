from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные поля', {'fields': ('telegram_id',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительные поля', {'fields': ('telegram_id',)}),
    )

    list_display = ('username', 'email', 'telegram_id', 'is_staff', 'is_active')

    search_fields = ('username', 'email', 'telegram_id')

    ordering = ('id',)
