from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import UserForm, DodoForm
from django.contrib import messages
from .models import *
from datetime import datetime
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

def pagina_twee(request):
    approved_dead_dodos = Dodo.objects.filter(alive=False, dead_approved=True)
    context = {"approved_dead_dodos": approved_dead_dodos}
    return render(request, "base/pagina_twee.html", context)

@login_required
def user_info(request):
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "User Info added successfully")
            return redirect("user_info")
    else:
        form = UserForm()

    password_form = PasswordChangeForm(request.user)
    
    context = {"form": form, "password_form": password_form}
    return render(request, "base/user_info.html", context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Import this function
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_info')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'base/change_password.html', {'form': form})

def user_list(request):
    users = Profile.objects.all()
    context = {"users": users}
    return render(request, 'base/user_list.html', context)

@login_required
def add_dodo(request):
    if request.method == "POST":
        form = DodoForm(request.POST)
        if form.is_valid():
            dodo = form.save(commit=False)
            dodo.user = request.user
            dodo.save()
            messages.success(request, "Dodo added successfully")
            return redirect("add_dodo")
    else:
        form = DodoForm()
    
    context = {"form": form}
    return render(request, "base/add_dodo.html", context)



@staff_member_required
def dodo_goedkeuring(request):
    dodos_pending_approval = Dodo.objects.filter(alive=False, dead_approved=False)

    if request.method == "POST":
        dodo_id = request.POST.get("dodo_id")
        dodo_instance = Dodo.objects.get(pk=dodo_id)

        update_entry = Update.objects.create(
            dodo=dodo_instance,
            user=request.user,
            date=datetime.now(),
            description="Dodo approved by admin"
        )

        dodo_instance.dead_approved = True
        dodo_instance.dead_approved_by = request.user
        dodo_instance.save()

        messages.success(request, "Dodo approved successfully")

    context = {"dodos_pending_approval": dodos_pending_approval}
    return render(request, "base/dodo_goedkeuring.html", context)

@login_required
def update_dodo(request):
    dodos = Dodo.objects.filter(user=request.user, alive=True)

    if request.method == "POST":
        dodo_id = request.POST.get("dodo")
        dodo_instance = Dodo.objects.get(pk=dodo_id)
        form = DodoForm(request.POST, instance=dodo_instance)
        if form.is_valid():
            form.save()
            updated_by = request.user.username
            update_entry = Update.objects.create(
                dodo=dodo_instance,
                user=request.user,
                date=datetime.now(),
                description=f"Dodo updated by {updated_by}"
            )
            
            messages.success(request, "Dodo updated successfully")
            if 'admin' in request.META.get('HTTP_REFERER'):
                return redirect('dodo_goedkeuring')
            else:
                return redirect('start_pagina')
    else:
        dodo_id = request.GET.get("dodo")
        if dodo_id:
            dodo_instance = Dodo.objects.get(pk=dodo_id)
            form = DodoForm(instance=dodo_instance)
        else:
            form = DodoForm()

    context = {"form": form, "dodos": dodos}
    return render(request, "base/update_dodo.html", context)

def feed(request):
    updates = Update.objects.all().order_by('-date')
    context = {"updates": updates}
    return render(request, 'base/feed.html', context)

