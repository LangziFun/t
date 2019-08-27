# coding:utf-8
from django.contrib import admin
from .models import User,LoginLog
admin.site.register(User)
admin.site.register(LoginLog)

from xadmin import views
import xadmin


class x_user(object):
    list_display = ['uid','username','password','userkey','privileges','last_login_time','last_login_ip','change_time']
    model_icon = 'fa fa-user'
    search_fields =['username','password','userkey','last_login_time','last_login_ip','change_time']
    refresh_times = (30, 60)


xadmin.site.register(User,x_user)



class x_log(object):
    list_display = ['login_username','login_password','login_userkey','login_status','login_time','login_ip']
    model_icon = 'fa fa-book'
    search_fields =['login_username','login_password','login_userkey','login_status','login_time','login_ip']
    refresh_times = (30, 60)


xadmin.site.register(LoginLog,x_log)

