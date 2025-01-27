from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.worker_pool = "solo"
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'

periodicity = getattr(settings, 'CELERY_BEAT_SCHEDULE_PERIODICITY', {})
for task_name, task_info in periodicity.items():
    app.conf.beat_schedule[task_name] = {
        'task': task_info['task'],
        'schedule': task_info['schedule'],
    }
