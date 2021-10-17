import sys

import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_PATH)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mealls.settings.dev')

from django.core.mail import send_mail as sm
from celery_app.main import c_app


@c_app.task
def send_email(email, code):
    """发送验证码邮件"""
    templates = "欢迎您使用mealls, 你的验证码为 %s 请勿将验证码告知他人" % code
    sm("Mealls团队", templates, '982781738@qq.com', [email, ])
    return code
