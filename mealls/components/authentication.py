from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user.models import User
from django.conf import settings
import jwt
from jwt import exceptions


class LoginAuth(BaseAuthentication):
    def authenticate(self, request):
        """获取请求头中的token"""
        token = str(request.headers.get('Authorization', None))
        if not token:
            raise AuthenticationFailed("请先登录后再重试")
        header_token = token.split(' ')[-1]
        try:
            # 对token进行解码操作
            payload = jwt.decode(jwt=header_token, key=settings.SECRET_KEY, algorithms='HS256')

        except exceptions.ExpiredSignatureError:
            # token过期
            raise AuthenticationFailed('Token已经过期,请重新登录')
        except exceptions.InvalidTokenError:
            # token 无效
            raise AuthenticationFailed('无效Token, 请重新登陆')
        return payload, token
