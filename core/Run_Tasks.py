# coding:utf-8
from .main import Sub_Crawl,Sub_Baidu,Sub_Brute,Run_Cpu_Min,Sub_ChangeIp,Sub_ChangeInf,Sub_Api,Heartbeat
import pymysql
import contextlib
import configparser
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process

cfg = configparser.ConfigParser()
cfg.read('config.ini')

host = cfg.get("Server", "host")
username = cfg.get("Server", "username")
password = cfg.get("Server", "password")
Dbname = cfg.get("Server","dbname").lower()
port = int(cfg.get("Server","port"))

@contextlib.contextmanager
def co_mysql(db='mysql'):
    conn = pymysql.connect(host=host,user=username,password=password,port=port,db=db,charset='utf8')
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    try:
        yield cursor
    except Exception as e:
        print(e)
        print('\n[警告] 数据库连接失败 请检查mysql数据库是否正确安装并开启\n\n')
    finally:
        conn.commit()
        cursor.close()
        conn.close()

import threading
import django
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
django.setup()
from app.models import Domains,Setting
import time
import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR,'ExtrApps'))


def start():
    print('''
    
             _                           _
            | |                         (_)
            | |     __ _ _ __   __ _ _____
            | |    / _` | '_ \ / _` |_  / |
            | |___| (_| | | | | (_| |/ /| |
            |______\__,_|_| |_|\__, /___|_|
                                __/ |      
                               |___/       
    
    ''')
    print('Main Console Start Running....')
    try:
        print('\n开始自检数据库配置文件数据')
        with co_mysql(db='mysql') as cursor:
            row_count = cursor.execute("show databases;")
            a = cursor.fetchall()

        Set = Setting.objects.all()[0]
        pool_count = int(Set.Pool)
        Alive_Status = eval(Set.Alive_Code)
        pax = range(int(Set.Thread))

        BA = Domains.objects.all()
        Sub_Domains = [x.get('url') for x in BA.values()]
        print('\n[成功] 数据库配置文件加载成功 请耐心等待数据持续收集整理\n\n')

    except Exception as e:
        print('\n[警告] 数据库配置文件加载失败 请在后台管理系统检查是否正确配置相关数据\n\n')
        time.sleep(60)
        time.sleep(60)
        time.sleep(60)

    # t2 = threading.Thread(target=Sub_Baidu,args=(Sub_Domains,))
    # t3 = threading.Thread(target=Sub_Crawl,args=(Sub_Domains,))
    # t4 = threading.Thread(target=Run_Cpu_Min)
    # t2.start()
    # t3.start()
    # t4.start()
    # while 1:
    #     Sub_Brute(Sub_Domains)
    #     time.sleep(3600*24)

    p1 = Process(target=Sub_Api,args=(Sub_Domains,))
    p2 = Process(target=Sub_Baidu,args=(Sub_Domains,))
    p3 = Process(target=Sub_Crawl,args=(pax,Sub_Domains,))
    p4 = Process(target=Run_Cpu_Min)
    p6 = Process(target=Sub_ChangeIp,args=(pax,))
    p7 = Process(target=Sub_ChangeInf,args=(Sub_Domains,))
    p5 = Process(target=Sub_Brute,args=(Sub_Domains,))
    p9 = Process(target=Heartbeat)
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p9.start()
    # 下面这两行注释，就不会扫描端口运行服务于部署web站点，这样做获取子域名更快，但是相关IP站点的资产更少
    # 酌情开启
    # p6.start()
    # p7.start()



if __name__ == '__main__':
    pass
