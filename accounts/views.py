from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect
from accounts.forms import LoginForm, RegistrationForm
from accounts.admin import UserCreationForm
from accounts.models import Customer, Goods

User = get_user_model()


def send_goods(request):
    goods = Goods.objects.all().values('PID', 'PName', 'price')
    data = json.dumps(list(goods))
    return HttpResponse(data, content_type="application/json")


def index(request):
    return render(request, 'home.html')


# 用户注册方法
def user_register(request):
    Method = request.method
    if Method == 'POST':
        # 如果有post提交的动作，就将post中的数据赋值给uf，供该函数使用
        uf = RegistrationForm(request.POST)
        if uf.is_valid():
            # 读取表单值
            username = uf.cleaned_data['username']
            tel = uf.cleaned_data['tel']
            password = uf.cleaned_data['password']
            user = User.objects.create_user(username=username, tel=tel, password=password)
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
        id = req.POST.get('id')
        password = req.POST.get('password')
        user = authenticate(id=id, password=password)
        if user:
            if user.is_active:
                # 成功登录
                login(req, user)
                return HttpResponseRedirect('/profile')
            else:
                return render(req, 'login.html', {"error": "Your Rango account is disabled."})

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
