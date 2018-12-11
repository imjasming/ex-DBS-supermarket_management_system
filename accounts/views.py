from django.shortcuts import render
from django.http import HttpResponse
from accounts.forms import LoginForm
from accounts.admin import UserCreationForm


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html',
                      {'title': 'Login', 'form': form})


def register(request):
    if request.method == 'GET':
        form = UserCreationForm
        return render(request, 'register.html',
                      {'form': form})
