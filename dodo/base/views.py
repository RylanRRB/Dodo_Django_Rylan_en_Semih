from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render
from django.db.models import Min
from .models import Distance, Time
from django.shortcuts import get_object_or_404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Distance, Time, Profile
from .forms import NameForm, TimeForm
from .forms import DistanceForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.


def say_hello(request):
    context = {"first_name": "Rylan en Semih"}
    return render(request, "base/hello.html", context)



def index(request):
    return render(request, "base/index.html")

def nameform(requests):
    form = NameForm()
    context = {"form": form}

    if requests.method == "POST":
        name = requests.POST.get("your_name")
        context["greeting"] = f"Welcome {name}!"

    return render(requests, "base/nameform.html", context)


def distanceform(requests):
    if requests.method == "POST":
        form = DistanceForm(requests.POST)
        length = requests.POST.get("length")
        does_length_exists = Distance.objects.filter(length=length).exists()
        if does_length_exists:
            form.add_error("length", "This length already exists")

        if form.is_valid():
            form.save()
            messages.success(requests, "Distance added successfully")
            return redirect("distance")
    else:
        form = DistanceForm()

    context = {"form": form}
    return render(requests, "base/distanceform.html", context)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()

    context = {"form": form}
    return render(request, "registration/register.html", context)
def new_time(request):
    if request.method == "POST":
        form = TimeForm(request.POST)
        if form.is_valid():
            time = form.save(commit=False)
            time.user = request.user
            time.save()
            messages.success(request, "Time added succesfully")
            return redirect("newtime")
    else:
        form = TimeForm()

    context = {"form": form}
    return render(request, "base/newtime.html", context)


def logoutview(request):
    logout(request)
    return redirect("index")


def unapproved_times(request):
    times = Time.objects.filter(approved=False)
    context = {"times": times}
    return render(request, "base/unapproved_times.html", context)


@staff_member_required
def approve_time(request, pk):
    time = Time.objects.get(pk=pk)
    time.approved = True
    time.approved_by = request.user
    time.save()
    messages.success(request, "Times approved.")
    return redirect("unapproved_times")


@staff_member_required
def deny_time(request, pk):
    time = Time.objects.get(pk=pk)
    time.delete()
    messages.success(request, "Times denied.")
    return redirect("unapproved_times")

@login_required
def all_user_times(request):
    user_times = Time.objects.filter(user=request.user)
    context = {"user_times": user_times}
    return render(request, "base/all_user_times.html", context)

@login_required
def edit_distance(request, pk):
    distance = get_object_or_404(Distance, pk=pk)
    if request.method == "POST":
        form = DistanceForm(request.POST, instance=distance)
        if request.POST.get("delete"):
            if request.user.is_staff:
                distance.delete()
                messages.success(request, "Distance deleted")
                return redirect("distance")
            else:
                messages.error(
                    request, "You are not authorized to delete distances.")
                return redirect("distance")
        if form.is_valid():
            form.save()
            length = form.cleaned_data['length']
            if Distance.objects.exclude(pk=pk).filter(length=length).exists():
                form.add_error('length', 'This length is already in use.')
            else:
                form.save()
                messages.success(request, "Distance updated successfully!")
                return redirect("distance")
    else:
        form = DistanceForm(instance=distance)
    context = {"form": form, "edit": True}
    return render(request, "base/distanceform.html", context)
