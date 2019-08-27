# coding:utf-8
from django.contrib import admin
from .models import Show_Data,IP,URL,Other_Url,Error_Log,Cpu_Min,Domains,Setting,Content
admin.site.register(Show_Data)
admin.site.register(IP)
admin.site.register(URL)
admin.site.register(Other_Url)
admin.site.register(Error_Log)
admin.site.register(Cpu_Min)
admin.site.register(Domains)
admin.site.register(Content)
# Register your models here.
from xadmin import views
import xadmin

class GlobalSetting(object):
    # 设置后台顶部标题
    site_title ='LangSrc资产监控系统'
    # 设置后台底部标题
    site_footer ='Powered By LangziFun'
    menu_style = "accordion"
    # # 设置左侧菜单可折叠
xadmin.site.register(views.CommAdminView, GlobalSetting)

class BaseSetting(object):
     """主题配置"""
     enable_themes = True
     use_bootswatch = True
xadmin.site.register(views.BaseAdminView, BaseSetting)

class x_show_data(object):
    """设置显示字段"""
    list_display = ['uid','url','title','power','server','status','ip','cs','area','servers','alive_urls','host_type','belong_domain','success','check','change_time']
    model_icon = 'fa fa-flag'
    search_fields = ['url','title','power','server','status','ip','cs','area','servers','alive_urls','host_type','belong_domain','success','check','change_time']
    refresh_times = (30, 60)
    # list_bookmarks = [{
    #     'title': "北京",  # 书签的名称, 显示在书签菜单中
    #     'query': {'area__contains': '北京'},  # 过滤参数, 是标准的 queryset 过滤
    #     'order': ("uid"),  # 排序参数
    #     'cols': ('url','title','power','server','status','content','ip','area','servers','alive_urls','host_type','belong_domain','success','check','change_time'),  # 显示的列
    # }]
    #
    # data_charts = {
    #     "chart1": {'title': "地区数据", "x-field": "change_time", "y-field": ("area",),
    #                    "order": ('change_time',)},
    #     "chart2": {'title': "监控报表", "x-field": "change_time", "y-field": ('belong_domain',),
    #                   "order": ('change_time',)}
    # }

    # title : 图表的显示名称
    # x-field : 图表的 X 轴数据列, 一般是日期, 时间等
    # y-field : 图表的 Y 轴数据列, 该项是一个list, 可以同时设定多个列, 这样多个列的数据会在同一个图表中显示
    # order : 排序信息, 如果不写则使用数据列表的排序

xadmin.site.register(Show_Data,x_show_data)

class x_domains(object):
    list_display = ['uid','url','BA_id','BA_sex','BA_name','counts','change_time']
    model_icon = 'fa fa-camera-retro'
    search_fields = ["url",'BA_id','BA_sex','BA_name','counts','change_time']
    refresh_times = (30, 60)
    # list_bookmarks = [{
    #     'title': "京东数据",  # 书签的名称, 显示在书签菜单中
    #     'query': {'BA_name__startswith': '北京'},  # 过滤参数, 是标准的 queryset 过滤
    #     'order': ("uid"),  # 排序参数
    #     'cols': ("url",'BA_id','BA_sex','BA_name','counts','change_time'),  # 显示的列
    # }]

    # data_charts = {
    #
    #     "chart2": {'title': u"监控报表", "x-field": "url", "y-field": ('counts',),
    #                   "order": ('uid',)}
    # }


xadmin.site.register(Domains,x_domains)

class x_ip(object):
    list_display = ['uid','ip','servers','host_type','alive_urls','area','cs','get','change_time']
    model_icon = 'fa fa-linux'

    search_fields = ['uid','ip','servers','host_type','alive_urls','area','cs','get','change_time']
    refresh_times = (30, 60)

    # data_charts = {
    #     "AREA": {'title': "IP归属地", "x-field": "area", "y-field": ("ip","area",),
    #                    "order": ('change_time',)},
    #     "SERVERS": {'title': "端口服务", "x-field": "change_time", "y-field": ('ip','servers',),
    #                   "order": ('change_time',)}
    # }


xadmin.site.register(IP,x_ip)

class x_url(object):
    list_display = ['uid','url','ip','get','change_time']
    model_icon = 'fa fa-book'
    search_fields =['url','ip','get','change_time']
    refresh_times = (30, 60)


xadmin.site.register(URL,x_url)

class x_other(object):
    list_display = ['uid','url','title','power','server','status','ip','change_time']
    model_icon = 'fa fa-cloud'
    search_fields =['url','title','power','server','status','ip','change_time']
    refresh_times = (30, 60)


xadmin.site.register(Other_Url,x_other)
class x_content(object):
    list_display = ['url','content','change_time']
    model_icon = 'fa fa-book'
    search_fields =['url','content','change_time']
    refresh_times = (30, 60)


xadmin.site.register(Content,x_content)
class x_cpu(object):
    list_display = ['uid','cpu','menory','network_send','network_recv','change_time']
    model_icon = 'fa fa-spinner fa-spin'
    search_fields =['cpu','menory','network_send','network_recv','change_time']
    refresh_times = (30, 60)


xadmin.site.register(Cpu_Min,x_cpu)



class x_error(object):
    list_display = ['uid','url','error','change_time']
    model_icon = 'fa fa-shield'
    search_fields = ['url','error','change_time']
    refresh_times = (30, 60)


xadmin.site.register(Error_Log,x_error)



class x_setting(object):
    list_display = ['name','Alive_Code','Thread','Pool','processes','childconcurrency','change_time']
    model_icon = 'fa fa-pencil'
    search_fields =['name','Alive_Code','Thread','Pool','processes','childconcurrency','change_time']
    refresh_times = (30, 60)

xadmin.site.register(Setting,x_setting)





