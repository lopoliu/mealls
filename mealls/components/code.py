from rest_framework.decorators import api_view
from rest_framework.response import Response
from random import randint
from django_redis import get_redis_connection
from celery_app.tasks import send_email

redis_conn = get_redis_connection()


def create_code():
    code = ''
    for i in range(6):
        code += str(randint(0, 9))
    return code


@api_view(http_method_names=['GET'])
def send_email_code(request):
    code = create_code()
    redis_conn.setex('email_code_%s' % request.query_params['email'], 60 * 5, code)
    send_email.delay(request.query_params.get('email'), code)
    return Response({'status': code})
