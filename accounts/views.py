from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect

from accounts.db_query import get_products
from accounts.forms import LoginForm
from accounts.admin import UserCreationForm
from accounts.models import Customer, Goods, Staff, MyBaseUser
from django.contrib import auth

User = get_user_model()


def send_goods(request):
    # ？branch=...&
    # 传 good 所有属性和store的库存
    # 'PID', 'PName', 'price', 'num', 'branch'
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
    return render(request, 'home.html', )


# 用户注册方法
def user_register(request):
    Method = request.method
    if Method == 'POST':
        # 如果有post提交的动作，就将post中的数据赋值给uf，供该函数使用
        uf = UserCreationForm(request.POST)
        if uf.is_valid():
            # 读取表单值
            username = uf.cleaned_data['a_username']
            tel = request.POST["tel"]
            a_password = request.POST["a_password"]
            right = request.POST["type"]
            # 注册系统表
            user = User.objects.create_user(username=username, password=a_password, )
            # 注册用户表
            user = MyBaseUser.objects.create_user(username=username, password=a_password, right=right)
            # userID = MyBaseUser.objects.get(username=username)
            if right == 'customer':
                Customer.objects.create(CID=user.id, name=username, tel=tel)
            else:
                Staff.objects.create(StaNO=user.id, StaName=username, tel=tel, Position=right)
            auth.login(request, user)
            return HttpResponseRedirect('/home')

        else:
            form = UserCreationForm()
            return render(request, 'register.html', {'form': form, 'error': uf.errors})

    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})


# 用户登录
def user_login(req):
    if req.method == 'POST':
        form = LoginForm(req.POST)
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                # 成功登录
                login(req, user)
                return HttpResponseRedirect('/home')
            else:
                return render(req, 'login.html', {'title': 'Login',
                                                  'form': form, "error": "Your Rango account is disabled."})

        else:
            form = LoginForm()
            return render(req, 'login.html', {'title': 'Login', 'form': form, "error": "password is invalid."})

    else:
        form = LoginForm()
        return render(req, 'login.html', {'title': 'Login', 'form': form})


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
