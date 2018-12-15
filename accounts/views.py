from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect

from accounts.db_query import get_products, get_supply_goods
from accounts.forms import LoginForm
from accounts.admin import UserCreationForm
from accounts.models import Customer, Goods, Staff, MyBaseUser
from django.contrib import auth

User = get_user_model()


def supply_goods(request):
    goods = get_supply_goods()
    data = json.dumps(goods)
    return HttpResponse(data, content_type="application/json")


def send_goods(request):
    goods = get_products()
    data = json.dumps(goods)
    return HttpResponse(data, content_type="application/json")


def staff_send(request):
    pass


def get_product_from_supplier(request):
    pass


def buy(request):
    if request.method == 'GET':
        if request.user.id is None:
            return HttpResponseRedirect('/home')


@login_required
def index_home(request):
    user = request.user
    return render(request, 'home.html', {'user': user})


def index(request):
    # if user:
    #     print(user.right)
    return render(request, 'home.html', {'user': None})


@login_required
def index_supply(request):
    return render(request, 'index_supply.html')


# 用户注册方法
def user_register(request):
    if request.method == 'POST':
        # 如果有post提交的动作，就将post中的数据赋值给uf，供该函数使用
        uf = UserCreationForm(request.POST)
        if uf.is_valid():
            # 读取表单值
            username = uf.cleaned_data['a_username']
            tel = request.POST["tel"]
            a_password = request.POST["a_password"]
            right = request.POST["type"]
            # 注册用户表
            user = MyBaseUser.objects.create_user(username=username, password=a_password, right=right)
            # userID = MyBaseUser.objects.get(username=username)
            if right == 'customer':
                Customer.objects.create(CID=user, name=username, tel=tel)
            else:
                Staff.objects.create(StaNO=user, StaName=username, tel=tel, Position=right)
            auth.login(request, user)
            request.__setattr__('user', user)
            return HttpResponseRedirect('/home')

        else:
            return render(request, 'register.html', {'form': uf, 'error': uf.errors, 'user': None})

    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form, 'user': None})


# 用户登录
def user_login(req):
    if req.method == 'POST':
        form = LoginForm(req.POST)
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(request=req, username=username, password=password)
        if user:
            if user.is_active:
                # 成功登录
                user = MyBaseUser.objects.get(username=username)
                auth.login(req, user)
                req.__setattr__('user', user)
                return HttpResponseRedirect('/home')
            else:
                return render(req, 'login.html', {'title': 'Login', 'user': None,
                                                  'form': form, "error": "Your Rango account is disabled."})

        else:
            form = LoginForm()
            return render(req, 'login.html', {'title': 'Login', 'form': form, "error": "password is invalid."})

    else:
        form = LoginForm()
        return render(req, 'login.html', {'title': 'Login', 'form': form, 'user': None})


@login_required
def index_logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login")


def index_leader(request):
    if request.user.is_authenticated:
        # username=request.user.username
        # right=User.objects.filter(username='username')
        right = request.user.right
        if right == 'customer':
            render()
        elif right == 'manmager':
            pass
        elif right == 'stuff':
            pass
        else:
            print("unknow right")
    else:
        return HttpResponseRedirect('/login')


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
