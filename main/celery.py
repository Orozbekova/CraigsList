import os
# from __future__ import absolute_import, unicode_literals
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
app = Celery('main')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

#sudo apt install redis-server
#redis-server
#sudo service redis-server stop
#sudo service redis-server start
# redis-cli ping -проверка
#celery -A main worker -l debug - запуск
