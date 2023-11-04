from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import account
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
                  # path('demo/', User.Demo.as_view()),
                  # 关于账号的功能
                  path('Register/', account.Register.as_view()),
                  path('Login/', account.Login.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
