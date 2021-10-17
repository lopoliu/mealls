
from django.contrib import admin
from django.urls import path, include
from mealls.components.code import send_email_code

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('code/', send_email_code),
]
