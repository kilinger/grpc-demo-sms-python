# web: gunicorn sms.wsgi --preload --log-file -
celery: celery -A application.celery worker -l info
celery-scheduler: celery -A application.celery beat -l info
