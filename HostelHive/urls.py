from django.contrib import admin
from django.urls import path 
from HostelHive import views
urlpatterns = [
    path('', views.index,name='HostelHive'),
    path('booknow/', views.booknow,name='booknow'),
    path('location/', views.location,name='location'),
     path('location/booknow/', views.booknow, name='booknow'),
]
