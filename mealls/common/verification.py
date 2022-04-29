"""
在某些特定条件下需要限制用户的访问次数
"""

from rest_framework.response import Response
from random import randint
from django_redis import get_redis_connection
from celery_app.tasks import send_email
from rest_framework.views import APIView
from .throttlings import CodeThrottling

redis_conn = get_redis_connection()


def create_code():
    code = ''
    for i in range(6):
        code += str(randint(0, 9))
    return code


class SendEmailCode(APIView):
    authentication_classes = []
    throttle_classes = [CodeThrottling, ]

    def get(self, request):
        code = create_code()
        redis_conn.setex('email_code_%s' % request.query_params['email'], 60 * 5, code)
        # send_email.delay(request.query_params.get('email'), code)
        return Response({'status': code})


class SendSmsConde(APIView):
    authentication_classes = []
    throttle_classes = [CodeThrottling, ]

    def get(self, request):
        code = create_code()
        redis_conn.setex('sms_code_%s' % request.query_params['phone'], 60 * 5, code)
        # send_sms
        return Response({'status': code})