import time

import jwt

from rest_framework.response import Response
from rest_framework.views import APIView
from mealls.settings.dev import SECRET_KEY
from .serializers import RegisterSerializer, LoginSerializer


class Register(APIView):
    authentication_classes = []

    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)


class Login(APIView):
    authentication_classes = []

    @classmethod
    def generate_token(cls, name, email):
        # 签发 jwt token
        headers = {'typ': 'jwt', 'alg': 'HS256'}
        payload = {
            'data': {'name': name, 'email': email},
            'exp': int(time.time()) + 1000      # token过期时间/毫秒
        }
        token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256', headers=headers)
        return token

    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        res = Response(data=ser.data)
        re_data = dict(ser.data)
        res['Authorization'] = self.generate_token(re_data['name'], re_data['email'])
        return res
