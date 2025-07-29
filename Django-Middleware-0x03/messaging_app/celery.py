from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django-Middleware-0x03.settings')

# app = Celery('messaging_app')
app = Celery('Django-Middleware-0x03')

# Set RabbitMQ as broker
app.conf.broker_url = 'amqp://guest:guest@localhost:5672//'

# Read config from Django settings using namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in all registered apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
