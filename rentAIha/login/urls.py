from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.loginPage, name='loginPage'),
    path('register/', views.register, name='registerPage'),
    path('user_sign_in/', (views.LoginHandler.as_view()), name='userLogin'),
    path('user_register/', csrf_exempt(views.RegisterHandler.as_view()), name='userRegister'),
]