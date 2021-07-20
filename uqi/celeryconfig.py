#celeryconfig.py
#amqps://dnqkkqtn:QyF7LNAmCFNeR7-I1O8eOx4Xjajh2mH6@baboon.rmq.cloudamqp.com/dnqkkqtn
try:
	from local_celeryconfig import *
except ImportError:
	BROKER_URL = 'amqps://dnqkkqtn:QyF7LNAmCFNeR7-I1O8eOx4Xjajh2mH6@baboon.rmq.cloudamqp.com/dnqkkqtn' #insert cloudAMQP url
	BROKER_POOL_LIMIT = 1
	BROKER_CONNECTION_TIMEOUT = 10
	CELERYD_CONCURRENCY = 4
	CELERY_RESULT_BACKEND = 'amqps://dnqkkqtn:QyF7LNAmCFNeR7-I1O8eOx4Xjajh2mH6@baboon.rmq.cloudamqp.com/dnqkkqtn' #insert cloudAMQP url

	CELERY_TASK_SERIALIZER = 'json'
	CELERY_RESULT_SERIALIZER = 'json'
	CELERY_ACCEPT_CONTENT=['json']
	CELERY_TIMEZONE = 'African/Lagos'
	CELERY_ENABLE_UTC = True