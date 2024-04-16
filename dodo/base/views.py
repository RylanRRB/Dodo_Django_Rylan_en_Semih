from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm, DodoForm
from django.contrib import messages
from .models import *
# Create your views here.

def startpagina(request):
    return render(request, "base/startpagina.html")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('start_pagina')
    else:
        form = UserCreationForm()
    
    context = {"form": form}
    return render(request, "registration/register.html", context)

def logoutview(request):
    logout(request)
    return redirect('start_pagina')

def say_firstname(request):
    context = {"first_name": "Rylan en Semih"}
    return render(request, "base/startpagina.html", context)

def say_lastname(request):
    context = {"last_name": "Baboelal en Sener"}
    return render(request, "base/pagina_twee.html", context)

def user_info(request):
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "User Info added succesfully")
            return redirect("user_info")
    else:
        form = UserForm()

    context = {"form": form}
    return render(request, "base/user_info.html", context)

def user_list(request):
    users = Profile.objects.all()
    context = {"users": users}
    return render(request, 'base/user_list.html', context)

@login_required #auth (fix)
def add_dodo(request):
    dodo_instance, created = Dodo.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = DodoForm(request.POST, instance=dodo_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Dodo Info added successfully")
            return redirect("add_dodo")
    else:
        form = DodoForm(instance=dodo_instance)

    context = {"form": form}
    return render(request, "base/add_dodo.html", context)
