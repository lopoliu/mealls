import time

import jwt

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from mealls.settings.dev import SECRET_KEY
from .serializers import RegisterSerializer, PasswordSerializer, LoginReSerializer


class Register(APIView):
    authentication_classes = []

    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)


class Login(APIView):
    authentication_classes = []
    result = {"code": "200", "message": "success", "data": None}
    HEADERS = {'typ': 'jwt', 'alg': 'HS256'}
    ALGORITHM = 'HS256'

    @classmethod
    def generate_token(cls, uid, name, email):
        # 签发 jwt token
        payload = {
            'data': {'name': name, 'email': email, "id": uid},
            'exp': int(time.time()) + 24 * 60 * 60,  # token过期时间/毫秒
            'create_time': time.time()
        }
        token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=cls.ALGORITHM, headers=cls.HEADERS)
        return token

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get("password", None)
        # 检查用户是否存在
        user = User.objects.filter(email=email).first()
        # 检查用户密码是否正确
        if user.check_password(password):
            ser = LoginReSerializer(instance=user)
            self.result['data'] = ser.data
            response_obj = Response(self.result)
            response_obj['Authorization'] = self.generate_token(uid=user.id, email=email, name=user.name)
            return response_obj
        else:
            self.result['message'] = "登录失败,请检查用户名和密码"
            return Response(self.result)


class Password(APIView):
    result = {'status_code': 200, 'message': 'success', 'data': ''}

    def put(self, request):
        user = User.objects.filter(id=request.user['data']['id']).first()
        res = PasswordSerializer(instance=user, data=request.data)
        res.is_valid(raise_exception=True)
        res.save()
        self.result['data'] = res.data
        return Response(self.result)
