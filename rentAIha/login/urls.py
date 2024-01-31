from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.loginPage, name='loginPage'),
    path('register/', views.register, name='register'),
    path('user_sign_in/', (views.LoginHandler.as_view()), name='login'),
    path('user_register/', csrf_exempt(views.RegisterHandler.as_view()), name='register'),
]