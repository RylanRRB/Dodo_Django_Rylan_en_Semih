from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import UserForm, DodoForm, UpdateForm
from django.contrib import messages
from .models import *
from datetime import datetime
from django.shortcuts import get_object_or_404

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
            messages.success(
                request, 'Your password was successfully updated!')
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


@staff_member_required
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
        staff_users = User.objects.filter(
            is_superuser=True) | User.objects.filter(is_staff=True)
        form = DodoForm()
        form.fields['user'].choices = [
            (user.id, user.username) for user in staff_users]

    context = {"form": form}
    return render(request, "base/add_dodo.html", context)


@staff_member_required
def dodo_goedkeuring(request):
    dodos_pending_approval = Dodo.objects.filter(
        alive=False, dead_approved=False)

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
    dodos = Dodo.objects.filter(alive=True)

    if request.method == "POST":
        dodo_id = request.POST.get("dodo")
        dodo_instance = Dodo.objects.get(pk=dodo_id)
        original_name = dodo_instance.dodo

        form = DodoForm(request.POST, instance=dodo_instance)
        if form.is_valid():
            dodo = form.save(commit=False)
            if dodo.dodo != original_name:
                dodo.dodo = original_name
            dodo.save()

            updated_by = request.user.username
            updated_description = f"Dodo: {original_name} updated by {updated_by}"
            update_entry = Update.objects.create(
                dodo=dodo_instance,
                user=request.user,
                date=datetime.now(),
                description=updated_description
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
            original_name = dodo_instance.dodo
            form = DodoForm(instance=dodo_instance,
                            initial={'dodo': original_name})
        else:
            form = DodoForm()

    context = {"form": form, "dodos": dodos}
    return render(request, "base/update_dodo.html", context) 


def feed(request):
    updates = Update.objects.all().order_by('-date')
    new_dodos = Dodo.objects.filter(alive=True).order_by('-date_of_birth')

    context = {"updates": updates, "new_dodos": new_dodos}
    return render(request, 'base/feed.html', context)


def user_profile(request, username):
    user = User.objects.get(username=username)
    user_updates = Update.objects.filter(user=user).order_by('-date')
    new_dodos = Dodo.objects.filter(
        user=user, alive=True).order_by('-date_of_birth')
    context = {"user": user, "user_updates": user_updates,
               "new_dodos": new_dodos}
    return render(request, 'base/user_profile.html', context)


@login_required
def delete_dodo(request, dodo_id):
    dodo = Dodo.objects.filter(pk=dodo_id).first()
    if request.method == 'POST':
        dodo.delete()
        return redirect('feed')

    return render(request, 'delete_dodo.html', {'dodo': dodo})

@login_required
def user_updates(request):
    current_user = request.user
    user_updates = Update.objects.filter(user=current_user).order_by('-date')
    new_dodos = Dodo.objects.filter(user=current_user, alive=True).order_by('-date_of_birth')
    context = {"user_updates": user_updates, "new_dodos": new_dodos}
    return render(request, 'base/user_updates.html', context)

@login_required
def update_update(request, update_id):
    update_instance = get_object_or_404(Update, id=update_id, user=request.user)
    original_dodo = update_instance.dodo.dodo
    original_user = update_instance.user.username

    if request.method == "POST":
        form = UpdateForm(request.POST, instance=update_instance)
        if form.is_valid():
            form.save()

            updated_by = request.user.username
            updated_description = f"Dodo: {original_dodo} updated by {original_user} (now by {updated_by})\n{form.cleaned_data['description']}"
            update_instance.description = updated_description
            update_instance.save()

            messages.success(request, "Update updated successfully")
            return redirect("user_updates")
    else:
        form = UpdateForm(instance=update_instance)

    return render(request, "base/update_update.html", {"form": form})





@login_required
def delete_update(request, update_id):
    update_instance = Update.objects.get(pk=update_id)
    if request.method == 'POST':
        update_instance.delete()
        messages.success(request, "Update deleted successfully")
        return redirect('user_updates')
    return render(request, 'base/delete_update.html', {'update': update_instance})
