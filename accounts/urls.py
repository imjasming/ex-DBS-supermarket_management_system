from django.conf.urls import url
from accounts import views

urlpattern=[
    url(r'`$',views.index),
]
