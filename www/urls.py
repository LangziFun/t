# coding:utf-8

from django.urls import path
from .views import index,check_login,login,search,show,change,add_url,add_ip,login_out
from . import views

urlpatterns = [
path('',index,name='index'),
path('login/',login,name='login'),
path('check_login/',check_login,name='check_login'),
path('search/',search,name='search'),
path('show/',show,name='show'),
path('change/',change,name='change'),
path('add_url/',add_url,name='add_url'),
path('add_ip/',add_ip,name='add_ip'),
path('login_out/',login_out,name='login_out'),


]
