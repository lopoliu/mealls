import time

import jwt
from django_redis import get_redis_connection
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from mealls.settings.dev import SECRET_KEY
from .serializers import RegisterSerializer, LoginSerializer

redis_conn = get_redis_connection()


class Register(APIView):
    authentication_classes = []

    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        # 验证短信验证码
        re_code = request.data.get("code")
        code = redis_conn.get("email_code_%s" % request.data['email'])
        if re_code != str(code, encoding='UTF-8'):
            raise ValidationError('短信验证码不正确')

        ser.save()
        return Response(ser.data)


class Login(APIView):
    authentication_classes = []

    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = User.objects.filter(email=request.data.get('email')).first()
        headers = {
            'typ': 'jwt', 'alg': 'HS256'
        }
        payload = {
            'data': {
                'name': user.name,
                'email': user.email
            },
            'exp': int(time.time()) + 1000
        }
        # 登录验证成功 签发 jwt token
        jwt_token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256', headers=headers)
        ser = LoginSerializer(instance=user)
        res = Response(data=ser.data)
        res['Authorization'] = jwt_token
        return res
