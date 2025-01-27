import pytest
from celery import Celery
from celery.contrib.testing.worker import start_worker


@pytest.fixture(autouse=True)
def configure_celery_for_tests(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True


@pytest.fixture(scope='session')
def celery_app():
    app = Celery('test')
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.conf.update(task_always_eager=False)  # Для реального выполнения задач
    return app


@pytest.fixture()
def celery_worker(celery_app):
    with start_worker(celery_app, perform_ping_check=False) as worker:
        yield worker
