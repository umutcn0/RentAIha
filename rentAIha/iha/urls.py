from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('handler/', csrf_exempt(views.IhaHandler.as_view()), name='ihaHandler'),
    path('', views.iha, name='iha')
]