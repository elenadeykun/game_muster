import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_catalog.settings.dev')

app = Celery('game_catalog')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'save-games-at-midnight': {
        'task': 'api.tasks.save_games',
        'schedule': crontab(minute=0, hour=0),
    },
}