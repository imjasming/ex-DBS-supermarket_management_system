from django.contrib.auth import authenticate, login
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from accounts.forms import LoginForm
from accounts.admin import UserCreationForm
from accounts.models import Customer


def index(request):
    return render(request, 'home.html')


# 用户注册方法
def user_register(request):
    Method = request.method
    if Method == 'POST':
        # 如果有post提交的动作，就将post中的数据赋值给uf，供该函数使用
        uf = UserCreationForm(request.POST)
        if uf.is_valid():
            # 读取表单值
            username = uf.cleaned_data['username']
            email = uf.cleaned_data['email']
            password = uf.cleaned_data['password']
            user = Customer.objects.create_user(username=username, email=email, password=password)
            return render(request, 'login.html', {'error': 'create success'})
        else:
            return render(request, 'register.html', {'error': uf.errors})
    else:
        form = UserCreationForm()
        return render(request, 'register.html',
                      {'form': form})


# 用户登录
def user_login(req):
    if req.method == 'POST':
        email = req.POST.get('email')
        password = req.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                # 成功登录
                login(req, user)
                return HttpResponseRedirect('/profile')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:

            return render(req, 'login.html', {"error": "password is invalid."})
    else:
        form = LoginForm()
        return render(req, 'login.html',
                      {'title': 'Login', 'form': form})


def change_Goods(request):
    pass


def change_Supplier(request):
    pass


def change_repository(request):
    pass


def change_store(request):
    pass


def change_Supply(request):
    pass


def change_Record(request):
    pass


def change_sell(request):
    pass
