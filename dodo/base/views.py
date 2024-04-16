from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("base/startpagina.html")
    else:
        form = UserCreationForm()
    
    context = {"form": form}
    return render(request, "registration/register.html", context)


def say_firstname(request):
    context = {"first_name": "Rylan en Semih"}
    return render(request, "base/startpagina.html", context)

def say_lastname(request):
    context = {"last_name": "Baboelal en Sener"}
    return render(request, "base/pagina_twee.html", context)