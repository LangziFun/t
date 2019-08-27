# coding:utf-8
from __future__ import unicode_literals


from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import User,LoginLog
from pyecharts.charts import Bar,Line
from pyecharts.globals import ThemeType

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType
from pyecharts.charts import Scatter3D

import django
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
django.setup()
from app.models import Other_Url,IP,URL,Show_Data,Error_Log,Cpu_Min,Domains,Setting,Content

from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(request):
        if 'login' in request.session:
            if request.session['login'] == True:
                return func(request)
            else:
                return render(request,'login.html')
        else:
            return render(request,'login.html')
    return wrapper





def bar_base() -> Bar:
    bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.WALDEN))
    Dom = Domains.objects.all()
    jk_domains = [x.get('url') for x in Dom.values()]
    jd_count = [x.get('counts') for x in Dom.values()]
    bar.add_xaxis(jk_domains)
    bar.add_yaxis("监控域名存活数", jd_count)
    return bar

def line_base() -> Line:
    line = Line(init_opts=opts.InitOpts(theme=ThemeType.WONDERLAND))
    Dom = Domains.objects.all()
    jk_domains = [x.get('url') for x in Dom.values()]
    jd_count = [x.get('counts') for x in Dom.values()]
    line.add_xaxis(jk_domains)
    line.add_yaxis("监控域名存活数", jd_count)
    return line

def Get_City_Nmae(area):
    # 北京  广东省
    citys = ['泸州','桂林','廊坊','山西','上海','蓬莱','玉溪','杭州','攀枝花','澳门','淮安','太原','内蒙古','韶关','海口','兰州','广东','江门','乌鲁木齐','邯郸','赤峰','莱西','湖州','石家庄','宜宾','秦皇岛','哈尔滨','吴江','南京','湛江','日照','聊城','洛阳','荆州','河南','盘锦','常德','云浮','惠州','香港','茂名','金昌','舟山','福建','延安','文登','荣成','肇庆','济宁','石嘴山','北京','大同','宁波','汕尾','寿光','郑州','潍坊','合肥','长沙','渭南','胶州','大连','三门峡','昆明','河北','常州','嘉峪关','西宁','湘潭','南宁','山东','金华','溧阳','咸阳','芜湖','丽水','南通','绵阳','锦州','沧州','章丘','牡丹江','克拉玛依','青海','北海','江阴','葫芦岛','张家界','台州','德阳','邢台','衢州','苏州','西藏','贵州','宿迁','浙江','中山','营口','鞍山','临沂','重庆','黑龙江','温州','威海','丹东','阳泉','招远','武汉','广西','淄博','义乌','拉萨','马鞍山','株洲','盐城','枣庄','德州','东营','唐山','张家港','扬州','镇江','宁夏','长治','沈阳','湖南','呼和浩特','临安','泉州','遵义','云南','嘉兴','九江','西安','辽宁','莱芜','银川','佛山','莱州','自贡','江苏','句容','河源','包头','开封','即墨','厦门','抚顺','成都','承德','东莞','瓦房店','福州','常熟','梅州','海南','三亚','宜昌','安徽','无锡','宜兴','珠海','青岛','陕西','新疆','太仓','焦作','绍兴','汕头','齐齐哈尔','潮州','深圳','南充','天津','临汾','江西','鄂尔多斯','长春','柳州','宝鸡','库尔勒','济南','张家口','泰州','清远','海门','四川','南昌','大庆','平顶山','贵阳','揭阳','台湾','胶南','滨州','吉林','安阳','富阳','菏泽','泰安','诸暨','徐州','岳阳','昆山','湖北','保定','广州','本溪','甘肃','烟台','平度','衡水','连云港','乳山','金坛','曲靖','铜川','阳江']
    city = [x for x in citys if x in area]
    if city == []:
        return 'None'
    else:
        return city[0]

def geo_base() -> Geo:
    Areas = set()
    areas = []
    Ip_Data = IP.objects.all().values()
    for k in Ip_Data:
        area = eval(k.get('area'))[0]
        city = Get_City_Nmae(area)
        if city != 'None':
            Areas.add(city)
            areas.append(city)

    data = dict.fromkeys(Areas,0)
    for k in areas:
        data[k] = data[k]+1

    result = list(zip(data.keys(),data.values()))

    c = (
        Geo()
        .add_schema(maptype="china")
        .add("IP归属地统计", result)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(),
        )
    )
    # c = (
    #     Geo()
    #     .add_schema(maptype="china")
    #     .add(
    #         "IP归属地统计", result,
    #         type_=ChartType.HEATMAP,
    #     )
    #     .set_series_opts(label_opts=opts.LabelOpts(is_show=False,))
    #     .set_global_opts(
    #         visualmap_opts=opts.VisualMapOpts(),
    #         title_opts=opts.TitleOpts(),
    #     )
    # )

    return c

# def Cpu_() -> Liquid:
#     # c = (
#     #     Liquid()
#     #     .add()
#     #     .set_global_opts(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
#     #
#     # )
#     # return c
#     cpu = Liquid(init_opts=opts.InitOpts(theme=ThemeType.LIGHT,width='250px',height='100px'))
#     cpu.add("lq", [0.3, 0.7],  shape=SymbolType.ARROW)
#
#     return cpu



def scatter3d_base() -> Scatter3D:
    Oth = Other_Url.objects.exclude(power='获取失败').exclude(server='获取失败').values()
    data = []
    for o in Oth:
        data.append([o.get('power'),o.get('server'),o.get('status')])
    c = (
        Scatter3D()
        .add("请求响应数据统计", data)
        .set_global_opts(
            title_opts=opts.TitleOpts(),
            visualmap_opts=opts.VisualMapOpts(range_color=["#313695","#4575b4","#74add1","#abd9e9","#e0f3f8","#ffffbf","#fee090","#fdae61","#f46d43","#d73027","#a50026",]),
        )
    )
    return c

import socket
def get_host(url):
    url = url.split('//')[1]
    if ':' in url:
        url = url.split(':')[0]
    try:
        s = socket.gethostbyname(url)
        return s
    except Exception as e:
        print('错误代码 [25] {}'.format(str(e)))
        Error_Log.objects.create(url=url,error='错误代码 [25] {}'.format(str(e)))
        return '获取失败'

@login_required
def login_out(request):
    request.session.clear()
    return HttpResponse('<script>alert("退出成功~")</script>')

@login_required
def add_url(request):
    user = request.session['user']
    privi = User.objects.filter(username=user)[0]
    if privi.privileges == 'no':
        return HttpResponse('<script>alert("当前账户没有添加资产数据权限")</script>')
    domain = request.GET.get('url')
    BA = Domains.objects.all()
    Sub_Domains = [x.get('url') for x in BA.values()]
    Show_belong_domain = [x for x in Sub_Domains if x in domain]
    try:
        if Show_belong_domain == []:
            return HttpResponse('<script>alert("该网址不隶属于任何受监控域名下")</script>')
        else:
            url_t = list(URL.objects.filter(url=domain))
            if url_t != []:
                return HttpResponse('<script>alert("数据库已存在该网址数据 请勿重复添加")</script>')
            else:
                URL.objects.create(url=domain,ip=get_host(domain))
                return request(request,'add_data.html',{'domain':Show_belong_domain[0]})
    except:
        return HttpResponse('<script>alert("发生错误 确保网址带 http:// 并且网址可访问")</script>')

@login_required
def add_ip(request):
    user = request.session['user']
    privi = User.objects.filter(username=user)[0]
    if privi.privileges == 'no':
        return HttpResponse('<script>alert("当前账户没有添加资产数据权限")</script>')
    domain = request.GET.get('ip')
    ip_res = list(IP.objects.filter(ip=domain))
    if ip_res == []:
        IP.objects.create(ip=domain, servers='None', host_type='None', alive_urls='None', area="('北京','北京')")
        return render(request,'add_ip.html',{'domain':domain})
    else:
        return HttpResponse('<script>alert("数据库已存在该IP数据，请勿重复添加")</script>')



@login_required
def index(request):
    # 可视化展示页面
    bar_img = bar_base()
    bar_ech = bar_img.render_embed()

    line_img = line_base()
    line_ech = line_img.render_embed()

    geo_img = geo_base()
    geo_ech = geo_img.render_embed()

    ddd_img = scatter3d_base()
    ddd_ech = ddd_img.render_embed()

    # cpu_img = Cpu_()
    # cpu_ech = cpu_img.render_embed()

    ip_counts = len(IP.objects.exclude(area='None').values())
    user = request.session['user']
    return render(request, "index.html", {"bar_ech": bar_ech,
                                          'line_ech':line_ech,
                                          'geo_ech':geo_ech,
                                          'ddd_ech':ddd_ech,
                                          'domain_counts':int(URL.objects.count()),
                                          'ip_counts':ip_counts,
                                          'user':user})

# def G_ip(request):
#     # 该函数用来接受 ip，然后返回

    # 'cpu_ech':cpu_ech,
@login_required
def change(request):
    # 修改数据未已经渗透测试完成
    KEY = list(request.GET.keys())[1]
    # url
    VALUE = request.GET.get(KEY)
    if KEY == 'url':
        Res = Show_Data.objects.filter(url=VALUE)[0]
        Res.check = '是'
        Res.save()
    if KEY == 'ip':
        Res = Show_Data.objects.filter(url=VALUE)[0]
        Res.check = '否'
        Res.save()
    return HttpResponse('<script>alert("设置成功")</script>')

@login_required
def show(request):
    KEY = list(request.GET.keys())[1]
    # url
    VALUE = request.GET.get(KEY)
    try:
        if KEY == 'url':
            Res = Show_Data.objects.filter(url=VALUE)[0]
            ip_counts = len(Other_Url.objects.filter(ip=Res.ip))
            c_counts = len(IP.objects.filter(cs=Res.cs))

            check = Res.check
            if check == '否':
                total = '1'
                return render(request, 'result.html', {'bea_list': Res,'totla':total,'ip_counts':ip_counts,'c_counts':c_counts})
            else:
                return render(request, 'result.html', {'bea_list': Res,'ip_counts':ip_counts,'c_counts':c_counts})
        if KEY == 'ip':
            Res = Show_Data.objects.filter(ip=VALUE)[0]
            ip_counts = len(Other_Url.objects.filter(ip=Res.ip))
            c_counts = len(IP.objects.filter(cs=Res.cs))

            check = Res.check
            if check == '否':
                total = '1'
                return render(request, 'result.html', {'bea_list': Res,'totla':total,'ip_counts':ip_counts,'c_counts':c_counts})
            else:
                return render(request, 'result.html', {'bea_list': Res,'ip_counts':ip_counts,'c_counts':c_counts})
    except:
        return render(request, 'nodata.html')

@login_required
def search(request):
    if request.method == 'GET':
        KEY = list(request.GET.keys())[1]
        # url
        VALUE = request.GET.get(KEY)
        # qq.com
        if KEY == 'url':
            Res = Other_Url.objects.filter(url__contains=VALUE).values()
            counts = len(Res)

            paginator = Paginator(Res, 5)
            page = request.GET.get('page')
            try:
                beatles_list = paginator.page(page)
            except PageNotAnInteger:
                beatles_list = paginator.page(1)
            except EmptyPage:
                beatles_list = paginator.page(paginator.num_pages)
            return render(request, 'show.html', {'bea_list': beatles_list,
                                                 'counts':counts,
                                                 'dbname':'网络资产',
                                                 'key':KEY,
                                                 'value':VALUE})

        if KEY == 'title':
            Res = Other_Url.objects.filter(title__contains=VALUE).values()
            counts = len(Res)

            paginator = Paginator(Res, 5)
            page = request.GET.get('page')
            try:
                beatles_list = paginator.page(page)
            except PageNotAnInteger:
                beatles_list = paginator.page(1)
            except EmptyPage:
                beatles_list = paginator.page(paginator.num_pages)
            return render(request, 'show.html', {'bea_list': beatles_list,
                                                 'counts':counts,
                                                 'dbname':'网络资产',
                                                 'key':KEY,
                                                 'value':VALUE})

        if KEY == 'content':
            Res = Content.objects.filter(content__contains=VALUE).values()
            counts = len(Res)

            paginator = Paginator(Res, 5)
            page = request.GET.get('page')
            try:
                beatles_list = paginator.page(page)
            except PageNotAnInteger:
                beatles_list = paginator.page(1)
            except EmptyPage:
                beatles_list = paginator.page(paginator.num_pages)
            return render(request, 'show.html', {'bea_list': beatles_list,
                                                 'counts':counts,
                                                 'dbname':'网页内容',
                                                 'key':KEY,
                                                 'value':VALUE})
        if KEY == 'ip':
            Res = IP.objects.filter(ip=VALUE).values()
            counts = len(Res)

            paginator = Paginator(Res, 5)
            page = request.GET.get('page')
            try:
                beatles_list = paginator.page(page)
            except PageNotAnInteger:
                beatles_list = paginator.page(1)
            except EmptyPage:
                beatles_list = paginator.page(paginator.num_pages)
            return render(request, 'show.html', {'bea_list': beatles_list,
                                                 'counts':counts,
                                                 'dbname':'主机端口',
                                                 'key':KEY,
                                                 'value':VALUE})
        if KEY == 'port':
            Res = IP.objects.filter(servers__contains=VALUE).values()
            counts = len(Res)

            paginator = Paginator(Res, 5)
            page = request.GET.get('page')
            try:
                beatles_list = paginator.page(page)
            except PageNotAnInteger:
                beatles_list = paginator.page(1)
            except EmptyPage:
                beatles_list = paginator.page(paginator.num_pages)
            return render(request, 'show.html', {'bea_list': beatles_list,
                                                 'counts':counts,
                                                 'dbname':'主机端口',
                                                 'key':KEY,
                                                 'value':VALUE})
        if KEY == 'server':
            Res = IP.objects.filter(servers__contains=VALUE).values()
            counts = len(Res)

            paginator = Paginator(Res, 5)
            page = request.GET.get('page')
            try:
                beatles_list = paginator.page(page)
            except PageNotAnInteger:
                beatles_list = paginator.page(1)
            except EmptyPage:
                beatles_list = paginator.page(paginator.num_pages)
            return render(request, 'show.html', {'bea_list': beatles_list,
                                                 'counts':counts,
                                                 'dbname':'主机端口',
                                                 'key':KEY,
                                                 'value':VALUE})
        if KEY == 'gip':
            Res = Other_Url.objects.filter(ip__contains=VALUE).values()
            counts = len(Res)

            paginator = Paginator(Res, 5)
            page = request.GET.get('page')
            try:
                beatles_list = paginator.page(page)
            except PageNotAnInteger:
                beatles_list = paginator.page(1)
            except EmptyPage:
                beatles_list = paginator.page(paginator.num_pages)
            return render(request, 'show.html', {'bea_list': beatles_list,
                                                 'counts':counts,
                                                 'dbname':'网络资产',
                                                 'key':KEY,
                                                 'value':VALUE})
        if KEY == 'cip':
            Res = IP.objects.filter(cs=VALUE).values()
            counts = len(Res)

            paginator = Paginator(Res, 5)
            page = request.GET.get('page')
            try:
                beatles_list = paginator.page(page)
            except PageNotAnInteger:
                beatles_list = paginator.page(1)
            except EmptyPage:
                beatles_list = paginator.page(paginator.num_pages)
            return render(request, 'show.html', {'bea_list': beatles_list,
                                                 'counts':counts,
                                                 'dbname':'主机端口',
                                                 'key':KEY,
                                                 'value':VALUE})

        if KEY == 'area':
            Res = IP.objects.filter(area__contains=VALUE).values()
            counts = len(Res)

            paginator = Paginator(Res, 5)
            page = request.GET.get('page')
            try:
                beatles_list = paginator.page(page)
            except PageNotAnInteger:
                beatles_list = paginator.page(1)
            except EmptyPage:
                beatles_list = paginator.page(paginator.num_pages)
            return render(request, 'show.html', {'bea_list': beatles_list,
                                                 'counts':counts,
                                                 'dbname':'主机端口',
                                                 'key':KEY,
                                                 'value':VALUE})
        if KEY == 'status':
            Res = Other_Url.objects.filter(status=VALUE).values()
            counts = len(Res)

            paginator = Paginator(Res, 5)
            page = request.GET.get('page')
            try:
                beatles_list = paginator.page(page)
            except PageNotAnInteger:
                beatles_list = paginator.page(1)
            except EmptyPage:
                beatles_list = paginator.page(paginator.num_pages)
            return render(request, 'show.html', {'bea_list': beatles_list,
                                                 'counts':counts,
                                                 'dbname':'网络资产',
                                                 'key':KEY,
                                                 'value':VALUE})

    else:
        return render(request, '404.html')


def login(request):
    return render(request,'login.html')

def check_login(request):
    if request.method == 'POST':
        login_username = request.POST.get('username','None')
        login_password = request.POST.get('password','None')
        login_userkey = request.POST.get('userkey','None')
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            login_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            login_ip = request.META.get('REMOTE_ADDR','None')
        login_status = '失败'
        try:
            UserData = User.objects.filter(username=login_username)[0]
            if login_username == UserData.username and login_password == UserData.password and login_userkey == UserData.userkey:
                request.session["login"] = True
                request.session["user"] = login_username
                request.session.set_expiry(0)
                login_status = '成功'
                UserData.last_login_ip = login_ip
                UserData.save()

                LoginLog.objects.create(login_username=login_username,login_password=login_password,login_userkey=login_userkey,login_ip=login_ip,login_status=login_status)
                return render(request,'index.html')
            else:
                LoginLog.objects.create(login_username=login_username, login_password=login_password,
                                    login_userkey=login_userkey, login_ip=login_ip, login_status=login_status)
                return HttpResponseRedirect('index')

        except Exception as e:
            LoginLog.objects.create(login_username=login_username, login_password=login_password,
                                    login_userkey=login_userkey, login_ip=login_ip, login_status=login_status)
            return render(request, '404.html')
    else:
        return render(request, '404.html')




