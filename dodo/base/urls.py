from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.say_firstname, name="start_pagina"),
    path("logoutview/", views.logoutview, name="logoutview"),
    path("", include('django.contrib.auth.urls')),
    path("register/", views.register, name="register"),
    path("startpagina/", views.say_firstname),
    path("pagina_twee/", views.pagina_twee, name="pagina_twee"),
    path("user_info/", views.user_info, name = "user_info"),
    path("user_list/", views.user_list, name="user_list"),
    path("add_dodo/", views.add_dodo, name="add_dodo"),
    path("update_dodo/", views.update_dodo, name= "update_dodo"),
    path("dodo_goedkeuring/", views.dodo_goedkeuring, name="dodo_goedkeuring"),
    path("feed/", views.feed, name="feed"),
    path("change_password/", views.change_password, name="change_password"),
    path("user_profile/<str:username>/", views.user_profile, name="user_profile"),
    path('delete_dodo/<int:dodo_id>/', views.delete_dodo, name='delete_dodo'),
    path("user_updates/", views.user_updates, name="user_updates"),
    path("update_update/<str:description>/", views.update_update, name="update_update"),
    path("delete_update/<int:update_id>/", views.delete_update, name="delete_update")
]
