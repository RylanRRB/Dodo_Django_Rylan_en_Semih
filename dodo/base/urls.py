from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("logoutview", views.logoutview, name="logoutview"),
    path("", include('django.contrib.auth.urls')),
    path("hello/", views.say_hello, name="hello"),
    path("nameform/", views.nameform, name="nameform"),
    path("distanceform/", views.distanceform, name="distanceform"),
    path("distanceform/<int:pk>/", views.edit_distance, name="edit_distance"),
    path("register/", views.register, name="register"),
    path("newtime/", views.new_time, name="newtime"),
    path("unapproved_times/", views.unapproved_times, name="unapproved_times"),
    path("approve_time/<int:pk>/", views.approve_time, name="approve_time"),
    path("deny_time/<int:pk>/", views.deny_time, name="deny_time"),
    path("all_user_times/", views.all_user_times, name="all_user_times")
]
