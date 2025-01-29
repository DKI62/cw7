from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
import logging

logger = logging.getLogger(__name__)  # Логирование ошибок


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(
                    {
                        "message": "User registered successfully",
                        "user": {
                            "id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "telegram_id": user.telegram_id
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                logger.error(f"Ошибка при сохранении пользователя: {e}")
                return Response({"error": "Ошибка при регистрации"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logger.error(f"Ошибка валидации: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        return RegisterSerializer  # Добавляем, чтобы работал Swagger
