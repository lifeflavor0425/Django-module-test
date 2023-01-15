from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.index, name="home"),
    path("station_line_search/", views.station_line_search, name="station_line_search"),
    
]
