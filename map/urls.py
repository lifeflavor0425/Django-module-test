from django.contrib import admin
from django.urls import path, include
from . import views
from django.shortcuts import redirect
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", views.index, name="home"),
    path("station_line_search/", views.station_line_search, name="station_line_search"),
    path("404/", views.None_404, name="Noen_404"),
    path("charts/", views.charts, name="charts"),
    path("table/", views.table, name="table"),
]
