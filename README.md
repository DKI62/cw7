# Habit Tracker API

## Описание проекта

**Habit Tracker API** — это серверная часть приложения для отслеживания привычек. Пользователи могут добавлять свои
привычки, устанавливать время выполнения, получать напоминания через Telegram и отслеживать свои достижения. Приложение
реализовано в соответствии с принципами REST API.

---

## Функционал

### Основные возможности

- **Регистрация и авторизация пользователей** с использованием JWT-токенов.
- **CRUD для привычек**:
    - Создание, редактирование, удаление и просмотр привычек.
- **Публичные привычки**:
    - Просмотр привычек, отмеченных как публичные, другими пользователями.
- **Напоминания в Telegram**:
    - Уведомления о запланированных привычках через Telegram.
- **Пагинация**:
    - Списки привычек отображаются с ограничением 5 записей на страницу.
- **Отложенные задачи с Celery**:
    - Задачи для рассылки напоминаний настроены через Celery и `django-celery-beat`.

---

## Установка

### Требования

- Python 3.12+
- PostgreSQL
- Redis
- Установленный `Poetry` для управления зависимостями.

### Инструкция по установке

1. Склонируйте репозиторий:
    ```bash
    git clone <git@github.com:DKI62/cw7.git>
    ```

2. Установите зависимости:
    ```bash
    poetry install
    ```

3. Создайте и настройте файл `.env` в корне проекта:
    ```env
   пример заполнения .env.example
    ```

4. Выполните миграции базы данных:
    ```bash
    python manage.py migrate
    ```

5. Создайте суперпользователя:
    ```bash
    python manage.py createsuperuser
    ```

6. Запустите сервер разработки:
    ```bash
    python manage.py runserver
    ```

7. Настройте и запустите Celery:
    ```bash
    celery -A config worker --loglevel=info
    celery -A config beat --loglevel=info
    ```

---

## Использование

### Эндпоинты API

1. **Регистрация**:
    - `POST /api/users/register/`
    - Пример запроса:
      ```json
      {
          "username": "user",
          "password": "password",
          "email": "user@example.com"
      }
      ```

2. **Авторизация**:
    - `POST /api/token/` — получение JWT-токенов.
    - `POST /api/token/refresh/` — обновление токенов.

3. **Привычки**:
    - `GET /api/habits/` — список привычек текущего пользователя (с пагинацией),список публичных привычек для всех, в
      том
      числе неавторизованным пользователям
    - `POST /api/habits/` — создание новой привычки.
    - `GET /api/habits/{id}/` — получение подробной информации о привычке.
    - `PUT /api/habits/{id}/` — обновление привычки.
    - `PATCH /api/habits/{id}/` — частичное обновление привычки.
    - `DELETE /api/habits/{id}/` — удаление привычки.

---

## Особенности реализации

1. **Валидаторы**:
    - Проверка совместимости связанных привычек и вознаграждений.
    - Ограничение времени выполнения привычки до 120 секунд.
    - Проверка периодичности выполнения привычек.

2. **Интеграция с Telegram**:
    - Уведомления пользователям о привычках с помощью Telegram-бота.

3. **Тестирование**:
    - Покрытие тестами более 80%.
    - Использованы `pytest` и `pytest-django`.

4. **Пагинация**:
    - Реализована пагинация для списков привычек (по 5 записей на страницу).

---

## Зависимости

- Django
- Django REST Framework
- Celery
- django-celery-beat
- django-cors-headers
- redis
- drf-spectacular
- python-telegram-bot

---

## Документация API

Документация автоматически генерируется и доступна по адресу:

/api/docs/swagger/ & /api/docs/redoc/
--
Для визуального просмотра используйте Swagger UI:


---

## Разработка

1. **Код соответствует PEP-8**:
   - Проведена проверка `flake8`.
   - Результат: 100% при исключении миграций.

2. **Проект готов к развёртыванию**:
   - Используются переменные окружения.
   - Настроены зависимости в `poetry.lock`.

3. **Работа с асинхронностью**:
   - Использованы Celery и Telegram API для асинхронной отправки сообщений.

---


