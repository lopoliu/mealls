
from django.contrib import admin
from django.urls import path, include
from mealls.components.code import SendEmailCode

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('code/', SendEmailCode.as_view()),
]
