from django.urls import path
from .import views

urlpatterns=[
		path('',views.user_login),
		path('weather/weather.html',views.index),
		
]