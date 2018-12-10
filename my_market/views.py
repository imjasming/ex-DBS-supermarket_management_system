from django.shortcuts import render

from accounts.forms import LoginForm, AdminLoginForm


def index_home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html',
                      {'title': 'Login', 'form': form})
