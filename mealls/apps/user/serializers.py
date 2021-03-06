from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from mealls.common.tools import to_md5
from .models import User
from django_redis import get_redis_connection


class RegisterSerializer(serializers.Serializer):
    redis_conn = get_redis_connection()
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=128, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    re_password = serializers.CharField(required=True, write_only=True)
    code = serializers.CharField(max_length=12, write_only=True)

    @staticmethod
    def validate_email(value):
        """验证邮箱是否被注册"""
        if User.objects.filter(email=value).exists():
            raise ValidationError("邮箱已经注册, 请登录")
        return value

    def validate(self, attrs):
        # 检查两次密码输入是否一致
        if attrs['re_password'] != attrs['password']:
            raise ValidationError("两次密码输入不一致")

        # 检查验证码是否正确
        if attrs['code'] is None:
            raise ValidationError("验证码不能为空")

        code = self.redis_conn.get("email_code_%s" % attrs['email'])
        if code is None:
            raise ValidationError("请先获取验证码")

        if attrs['code'] != str(code, encoding='UTF-8'):
            raise ValidationError("验证码错误, 请重新输入")

        return attrs

    def create(self, validated_data):
        del validated_data['re_password']
        del validated_data['code']
        validated_data['password'] = to_md5(validated_data['password'])
        user = User(**validated_data)
        user.save()
        return user


class LoginReSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "is_delete")


class PasswordSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(required=False)
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    re_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if not self.instance.check_password(attrs['old_password']):
            raise ValidationError("旧密码不正确")

        if attrs['new_password'] != attrs['re_password']:
            raise ValidationError("两次密码输入不一致")
        return attrs

    def update(self, instance, validated_data):
        instance.password = to_md5(validated_data['new_password'])
        instance.save()
        return instance
