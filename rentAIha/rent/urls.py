from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'rentAIha'

urlpatterns = [
    path('operation/', csrf_exempt(views.RentOperations.as_view()), name='rentOparations'),
    path('', views.dashboard, name='loginPage'),
    path('history/', views.history, name='history'),
]