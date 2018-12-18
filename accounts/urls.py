from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.user_login, name='login'),
    path('register', views.user_register, name='register'),
    path('data/product', views.send_goods),
    path('data/product-op', views.send_goods_branch),
    path('data/supply', views.send_supply_goods),
    path('data/staff', views.send_staff),
    path('data/request-goods', views.send_request_goods),
    path('data/request-staff', views.send_request_staff),
    path('data/record', views.send_record),
    path('response/goods', views.response_goods),
    path('response/staff', views.response_staff),
    path('home', views.index_home),
    path('logout', views.index_logout),
    path('buy', views.buy),
    path('change/price', views.change_price),
    path('change/staff', views.change_staff),
    path('add', views.add),
    path('index/supply', views.index_supply),
    path('index/staff', views.index_staff),
    path('index/product-manage', views.index_product_manage),
    path('index/request', views.index_request),
    path('index/record', views.index_record)
]
