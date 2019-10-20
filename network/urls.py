from django.conf.urls import url
from django.contrib import admin
import django.contrib.auth
from . import views
from django.urls import path, include

urlpatterns = [
    path('home/', views.home),
    path('basic-info/', views.basic_info),
    path('signup/', views.signup),
    path('add-info/', views.add_info),
    path('get-data/', views.get_data),
    path('water-map/', views.water_map),
    path('call-firefighter/', views.inform_neighbour),
    path('call-neighbour/', views.inform_neighbour),
    path('firefighter-console/', views.firefighter_console),
]
