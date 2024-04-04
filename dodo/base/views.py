from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def say_hello(request):
    context = {"first_name": "Rylan en Semih"}
    return render(request, "base/hello.html", context)
