from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.say_firstname, name="start_pagina"),
    path("", include('django.contrib.auth.urls')),
    path("register/", views.register, name="register"),
    path("startpagina/", views.say_firstname),
    path("pagina_twee/", views.say_lastname, name = "pagina_twee"),
    path("user_info/", views.user_info, name = "user_info"),
    path("user_list/", views.user_list, name="user_list"),
    path("add_dodo/", views.add_dodo, name="add_dodo")
]
