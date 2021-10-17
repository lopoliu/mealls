from rest_framework.authentication import BaseAuthentication


class LoginAuth(BaseAuthentication):
    def authenticate(self, request):
        pass