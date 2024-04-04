from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.say_hello, name = "start_pagina"),
    path("", include('django.contrib.auth.urls')),
    path("hello/", views.say_hello)
]
