from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Route for the index page
    path('get-weather/', views.weather_details, name='get_weather'),  # Route for the raw API response
]
