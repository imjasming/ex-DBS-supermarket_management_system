from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseBadRequest

from accounts import db_manuplate
from accounts.db_manuplate import buy_goods, change_goods_price, request_fire_staff, request_add_goods, \
    response_add_goods, response_fire_staff, add_to_shopping_cart, remove_cart_item_by_id
from accounts.db_query import get_supply_goods_json, get_goods_json, get_staff_json, get_branch_goods_json, \
    get_add_goods_request_json, get_staff_fire_request_json, get_customer_record_json, get_all_record_json, \
    get_branch_record_json, get_user_shopping_cart_json
from accounts.forms import LoginForm
from accounts.admin import UserCreationForm
from accounts.models import Customer, Goods, Staff, MyBaseUser
from django.contrib import auth

User = get_user_model()


@login_required
def send_supply_goods(request):
    return HttpResponse(get_supply_goods_json(), content_type="application/json")


def send_goods(request):
    return HttpResponse(get_goods_json(), content_type="application/json")


@login_required
def send_goods_branch(request):
    if request.user.id is None:
        return HttpResponseBadRequest()
    return HttpResponse(get_branch_goods_json(request.user.id), content_type="application/json")


@login_required
def send_staff(request):
    user = request.user
    if user.right == 'smanager':
        return HttpResponse(get_staff_json(user.id, True), content_type="application/json")
    elif user.right == 'manager':
        return HttpResponse(get_staff_json(user.id, False))
    else:
        return HttpResponseNotAllowed('')


@login_required
def send_request_goods(request):
    user = request.user
    if user.right == 'smanager':
        return HttpResponse(get_add_goods_request_json(), content_type="application/json")
    else:
        return HttpResponseNotAllowed('')


@login_required
def send_record(request):
    user = request.user
    if user.right == 'customer':
        return HttpResponse(get_customer_record_json(user.id))
    elif user.right == 'smanager':
        return HttpResponse(get_all_record_json())
    else:
        return HttpResponse(get_branch_record_json(user.id))


@login_required
def send_request_staff(request):
    user = request.user
    if user.right == 'smanager':
        return HttpResponse(get_staff_fire_request_json(), content_type="application/json")
    else:
        return HttpResponseNotAllowed('')


@login_required
def send_user_shopping_cart(request):
    if request.user.id is None:
        return HttpResponseNotAllowed('/home')
    else:
        return HttpResponse(get_user_shopping_cart_json(request.user.id))


@login_required
def buy(request):
    if request.method == 'GET':
        if request.user.id is None:
            return HttpResponseNotAllowed('/home')
        else:
            uid = request.user.id
            pid = request.GET['pid']
            bname = request.GET['bname']
            num = request.GET['num']
            try:
                buy_goods(pid, bname, num, uid)
                return HttpResponse(get_goods_json())
            except Exception as e:
                raise e


@login_required
def add(request):
    user = request.user
    if user.right == 'customer':
        return HttpResponseNotAllowed('change staff')
    else:
        try:
            pid = request.GET['pid']
            sid = request.GET['sid']
            num = request.GET['num']
            request_add_goods(pid, user.id, num, sid)
            return HttpResponse(get_supply_goods_json())
        except Exception as e:
            raise e


@login_required
def add_to_cart(request):
    if request.method == 'GET':
        if request.user.id is None:
            return HttpResponseNotAllowed('change_price')
        else:
            try:
                uid = request.user.id
                pid = request.GET['pid']
                pname = request.GET['pname']
                bname = request.GET['bname']
                num = request.GET['num']
                price = request.GET['price']
                add_to_shopping_cart(uid, pid, pname, bname, num, price)
                return HttpResponse(get_goods_json())
            except Exception as e:
                raise e


@login_required
def remove_cart_item(request):
    if request.method == 'GET':
        if request.user.id is None:
            return HttpResponseNotAllowed('change_price')
        else:
            try:
                rid = request.GET['rid']
                remove_cart_item_by_id(rid)
                return HttpResponse(get_user_shopping_cart_json(request.user.id))
            except Exception as e:
                raise e


@login_required
def change_price(request):
    if request.user.id is None:
        return HttpResponseNotAllowed('change_price')
    else:
        pid = request.GET['pid']
        bname = request.GET['bname']
        price = request.GET['price']
        try:
            change_goods_price(bname, pid, price)
            return HttpResponse(get_branch_goods_json(request.user.id), content_type="application/json")
        except Exception as e:
            raise e


@login_required
def change_staff(request):
    user = request.user
    if user.right == 'customer':
        return HttpResponseNotAllowed('change staff')
    else:
        try:
            request_fire_staff(user.id, request.GET['sid'])
            return HttpResponse(get_staff_json(request.user.id), content_type="application/json")
        except Exception as e:
            raise e


@login_required
def response_goods(request):
    user = request.user
    rid = request.GET['rid']
    status = request.GET['status']
    if user.right == 'smanager':
        response_add_goods(rid, user.id, status)
        return HttpResponse(get_add_goods_request_json(), content_type="application/json")
    else:
        return HttpResponseNotAllowed('')


@login_required
def response_staff(request):
    user = request.user
    rid = request.GET['rid']
    status = request.GET['status']
    if user.right == 'smanager':
        response_fire_staff(rid, status)
        return HttpResponse(get_staff_fire_request_json(), content_type="application/json")
    else:
        return HttpResponseNotAllowed('')


def index(request):
    user = request.user
    if user is None or user is AnonymousUser:
        return render(request, 'home.html', {'user': None})
    else:
        return render(request, 'home.html', {'user': user, 'title': "商品列表"})


@login_required
def index_home(request):
    return render(request, 'home.html', {'user': request.user, 'title': "商品列表"})


@login_required
def index_supply(request):
    return render(request, 'index_supply.html', {'user': request.user, 'title': "进货列表"})


@login_required
def index_product_manage(request):
    user = request.user
    if user.right == 'manager':
        return render(request, 'index_product_op.html', {'user': user, 'title': "价格改动"})
    elif user.right == 'customer':
        return HttpResponseNotAllowed('')


@login_required
def index_staff(request):
    user = request.user
    if user.right == 'manager':
        return render(request, 'index_staff.html', {'user': user, "title": "员工变动"})
    elif user.right == 'customer':
        return HttpResponseNotAllowed('')


@login_required
def index_request(request):
    user = request.user
    if user.right == 'customer':
        return HttpResponseNotAllowed('request method')
    else:
        return render(request, 'index_request.html', {'user': user, 'title': "进货申请"})


@login_required
def index_record(request):
    user = request.user
    return render(request, 'index_record.html', {'user': user, 'title': '历史纪录'})


@login_required
def index_cart(request):
    user = request.user
    return render(request, 'index_cart.html', {'user': user, 'title': '购物车'})


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

            right = None
            try:
                right = request.POST["type"]
            except Exception as e:
                pass

            if right is None:
                right = 'customer'

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
