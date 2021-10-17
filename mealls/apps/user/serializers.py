from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=128, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    re_password = serializers.CharField(required=True, write_only=True)

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
        return attrs

    def create(self, validated_data):
        del validated_data['re_password']
        return User.objects.create(**validated_data)