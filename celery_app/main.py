from celery import Celery

c_app = Celery('mealls', broker='redis://127.0.0.1:6379/1')

c_app.autodiscover_tasks(['celery_app.tasks'])