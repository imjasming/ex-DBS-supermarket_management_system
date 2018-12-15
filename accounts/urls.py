from django.urls import path

from . import views

urlpatterns = [
     path('', views.index),
     path('login', views.user_login, name='login'),
     path('register', views.user_register, name='register'),
     path('data/product', views.send_goods),
     path('data/supply', views.supply_goods),
     path('home', views.index_home),
     path('logout', views.index_logout),
     path('buy', views.buy),
     path('add', views.add),
     path('supply', views.index_supply),
]
