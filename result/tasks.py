# in any app that you want celery tasks, make a tasks.py and the celery app will autodiscover that file and those tasks.
from __future__ import absolute_import
from celery import shared_task

from random import randint
import sys

@shared_task
def add_random_numbers():
	rand_1 = randint(1,9)
	rand_2 = randint(1,9)

	total = rand_1 + rand_2
	print total
	sys.stdout.flush()
	return total