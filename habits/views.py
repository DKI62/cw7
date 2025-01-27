from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from .models import Habit
from .serializers import HabitSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Получить список привычек",
        description="Возвращает список привычек текущего пользователя и публичные привычки.",
    ),
    create=extend_schema(
        summary="Создать новую привычку",
        description="Создаёт привычку, привязанную к текущему пользователю.",
    ),
    retrieve=extend_schema(
        summary="Получить подробности о привычке",
        description="Возвращает данные о конкретной привычке по ID.",
    ),
    update=extend_schema(
        summary="Обновить привычку",
        description="Обновляет данные о привычке, принадлежащей текущему пользователю.",
    ),
    destroy=extend_schema(
        summary="Удалить привычку",
        description="Удаляет привычку, принадлежащую текущему пользователю.",
    ),
)
class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Показываем свои привычки и публичные
            return Habit.objects.filter(Q(user=user) | Q(is_public=True))
        # Для анонимных пользователей — только публичные привычки
        return Habit.objects.filter(is_public=True)

    def perform_create(self, serializer):
        # Привязываем привычку к текущему пользователю
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # Проверяем, что пользователь имеет доступ к изменению привычки
        if self.get_object().user != self.request.user:
            raise PermissionDenied("Вы не можете редактировать эту привычку.")
        serializer.save()

    def perform_destroy(self, instance):
        # Проверяем, что пользователь имеет доступ к удалению привычки
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не можете удалить эту привычку.")
        instance.delete()
