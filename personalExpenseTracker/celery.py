import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personalExpenseTracker.settings')
app = Celery('personalExpenseTracker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
app.conf.timezone = 'UTC'
app.autodiscover_tasks()
