# replace 'uqi' with the name of your django uqiect.
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

#set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uqi.settings')

app = Celery('uqi')
app.config_from_object('uqi.celeryconfig')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))