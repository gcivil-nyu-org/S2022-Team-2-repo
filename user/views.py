from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, "user/home.html")


def signup(request):
    return render(request, "user/signup.html")


def login(request):
    return render(request, "user/login.html")


def logout(request):
    pass
