from django.contrib import admin
from django.urls import include, path

urlpatterns = [
   path('', include('login.urls'), name='login'),
   path('register/', include('login.urls'), name='login'),
   path('admin/', admin.site.urls),    
   path('login/', include('login.urls'), name='login'),
   path('rent/', include('rent.urls'), name='rent'),
   path('iha/', include('iha.urls'), name='iha'),
]