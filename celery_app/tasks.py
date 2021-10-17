import time

from celery_app.main import c_app


@c_app.task
def send_email(email, code):
    time.sleep(3)
    """发送邮件耗时3s，异步处理"""
    return code
