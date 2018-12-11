from django.shortcuts import render

from accounts.forms import LoginForm, AdminLoginForm


def index_home(request):
    return render(request, 'home.html')

