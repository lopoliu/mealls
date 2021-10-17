from django_redis import get_redis_connection
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer

redis_conn = get_redis_connection()


class Register(APIView):
    def post(self, request):
        ser = UserSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        # 验证短信验证码
        re_code = request.data.get("code")
        code = redis_conn.get("email_code_%s" % request.data['email'])
        if re_code != code:
            raise ValidationError('短信验证码不正确')

        ser.save()
        return Response(ser.data)