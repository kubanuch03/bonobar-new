from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery import shared_task
from django.core.cache import cache
from datetime import timedelta
from celery.schedules import crontab
import datetime
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bono_bar.django.base')

app = Celery('config')


app.config_from_object('django.conf:settings', namespace='CELERY')


@app.task
def send_report_booking():
    today = datetime.today()
    next_month = today.replace(day=28) + timedelta(days=4)
    last_day_of_current_month = next_month - timedelta(days=next_month.day)
    
    if today.day == last_day_of_current_month.day:
        print("Отправляем отчет о бронированиях, так как сегодня последний день месяца.")



app.conf.beat_schedule = {
    'send_report_booking': {
        'task': 'apps.book.tasks.send_report_booking',
        # 'schedule': timedelta(hours=4),
       'schedule': crontab(hour=0, minute=0), 

    },
}


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: ,{self.request!r}')
