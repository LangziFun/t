# -*- encoding: utf-8 -*-
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/6 8:03
@file: models.py
"""
from django.db import models


class IP(models.Model):
    uid = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=15,unique=True,verbose_name='IP地址',)
    servers = models.TextField(verbose_name='端口服务')
    host_type = models.CharField(max_length=10,verbose_name='操作系统')
    alive_urls = models.TextField(verbose_name='部署网站')
    area = models.CharField(max_length=400,verbose_name='IP归属')
    cs = models.CharField(max_length=20,default='暂无信息',verbose_name='隶属C段')
    get = models.CharField(max_length=1,default='否',verbose_name='是否校验')
    change_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    

    class Meta:
        db_table = 'IP'
        verbose_name = '主机端口'
        verbose_name_plural = verbose_name


class Domains(models.Model):
    uid = models.AutoField(primary_key=True)
    url = models.CharField(max_length=30, unique=True, verbose_name='域名')
    BA_sex = models.CharField(max_length=50,default='企业', verbose_name='性质')
    BA_name = models.CharField(max_length=50, verbose_name='名称')
    BA_id = models.CharField(max_length=50, verbose_name='编号')
    counts = models.CharField(max_length=8, default=0, verbose_name='捕获数量')
    change_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')

    class Meta:
        db_table = 'Domains'
        verbose_name = '监控域名'
        verbose_name_plural = verbose_name

class Content(models.Model):
    uid = models.AutoField(primary_key=True)
    url = models.CharField(max_length=50,unique=True,verbose_name='索引网址')
    content = models.TextField(verbose_name='网页内容')
    change_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    class Meta:
        db_table = 'Content'
        verbose_name = '网页内容'
        verbose_name_plural = verbose_name

class URL(models.Model):
    uid = models.AutoField(primary_key=True)
    url = models.CharField(max_length=50,unique=True,verbose_name='索引网址')
    get = models.CharField(max_length=1,default='否',verbose_name='是否爬行')
    ip = models.CharField(max_length=15,verbose_name='IP地址')
    change_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    class Meta:
        db_table = 'URL'
        verbose_name = '网址索引'
        verbose_name_plural = verbose_name

class Other_Url(models.Model):
    uid = models.AutoField(primary_key=True)
    url = models.CharField(max_length=100,unique=True,verbose_name='爬行网址')
    title = models.CharField(max_length=220, default='None',verbose_name='网站标题')
    power = models.CharField(max_length=200, default='None',verbose_name='容器/语言')
    server = models.CharField(max_length=100, default='None',verbose_name='服务器类型')
    status = models.CharField(max_length=4,default='None',verbose_name='请求响应')
    ip = models.CharField(max_length=15,verbose_name='IP地址')
    change_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    class Meta:
        db_table = 'Other_Url'
        verbose_name = '网络资产'
        verbose_name_plural = verbose_name

class Setting(models.Model):
    name = models.CharField(max_length=30,default='萌萌哒屎壳郎一号方案',verbose_name='配置方案')
    Alive_Code = models.CharField(max_length=250,default='[200,204,206,301,302,304,401,402,403,404,500,501,502,503]',verbose_name='允许入库状态码')
    Thread = models.CharField(max_length=4,default='2', verbose_name='线程数量')
    Pool = models.CharField(max_length=4,default='4',  verbose_name='线程池量')
    processes = models.CharField(max_length=4,default='4',  verbose_name='进程数量')
    childconcurrency = models.CharField(max_length=4,default='8',  verbose_name='子协程数量')
    change_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    class Meta:
        db_table = 'Setting'
        verbose_name = '配置信息'
        verbose_name_plural = verbose_name

class Show_Data(models.Model):
    uid = models.AutoField(primary_key=True)
    url = models.CharField(max_length=50,unique=True,verbose_name='展示网址')
    title = models.CharField(max_length=200,default='None',verbose_name='网站标题')
    power = models.CharField(max_length=150,default='None',verbose_name='容器/语言')
    server = models.CharField(max_length=150,default='None',verbose_name='服务器类型')
    status = models.CharField(max_length=4,default='None',verbose_name='请求响应')
    content = models.ForeignKey('Content',on_delete=models.DO_NOTHING,verbose_name='网页内容')

    ip = models.CharField(max_length=15,verbose_name='IP地址')
    cs = models.CharField(max_length=20,default='暂无信息',verbose_name='隶属C段')

    servers = models.TextField(default='None',verbose_name='端口服务')
    alive_urls = models.TextField(default='None',verbose_name='部署网站')
    host_type = models.CharField(max_length=10,default='None',verbose_name='操作系统')
    #baidu_url = models.TextField(verbose_name='百度搜索捕获网址')
    area = models.CharField(max_length=400,default='None',verbose_name='IP归属')
    belong_domain = models.CharField(max_length=15,db_index=True,default='None',verbose_name='所属域名')
    change_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    success = models.CharField(max_length=1,default='否',verbose_name='监控齐全')
    check = models.CharField(max_length=1,default='否',verbose_name='是否检测')
    class Meta:
        db_table = 'Show_Data'
        verbose_name = '数据展示'
        verbose_name_plural = verbose_name

class Error_Log(models.Model):
    uid = models.AutoField(primary_key=True)
    url = models.CharField(max_length=100,verbose_name='异常网址')
    error = models.TextField(verbose_name='报错内容')
    change_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    class Meta:
        db_table = 'Error_Log'
        verbose_name = '错误日志'
        verbose_name_plural = verbose_name


class Cpu_Min(models.Model):
    uid = models.AutoField(primary_key=True)
    cpu = models.CharField(max_length=15,verbose_name='CPU使用率')
    menory = models.CharField(max_length=15,verbose_name='内存使用率')
    network_send = models.CharField(max_length=20,verbose_name='上传流量Mb/小时')
    network_recv = models.CharField(max_length=20,verbose_name='接收流量Mb/小时')
    change_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    class Meta:
        db_table = 'Cpu_Min'
        verbose_name = '资源消耗'
        verbose_name_plural = verbose_name