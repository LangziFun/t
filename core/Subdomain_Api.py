# -*- encoding: utf-8 -*- 
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/6 9:43
@file: Subdomain_Baidu.py
"""
import configparser
cfg = configparser.ConfigParser()
cfg.read('config.ini')
seckey = cfg.get("API", "securitytrails")
import requests
import re
import time
from urllib.parse import quote,urlparse
requests.packages.urllib3.disable_warnings()
timeout = 15
from concurrent.futures import ThreadPoolExecutor
import random
import django
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
django.setup()
from app.models import Setting,URL

Set = Setting.objects.all()[0]
pool_count = int(Set.Pool)
Alive_Status = eval(Set.Alive_Code)

Dicts = os.path.join('Auxiliary','Black_Url.list')

black_list = list(set([x.strip() for x in open(Dicts, 'r', encoding='utf-8').readlines()]))




def check_black(url):
    res = [True if x in url else False for x in black_list]
    if True in res:
        return True
    else:
        return False

def Requests(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    try:
        r = requests.get(url=url,headers=headers,timeout=10)
        if b'Service Unavailable' not in r.content and b'The requested URL was not found on' not in r.content and b'The server encountered an internal error or miscon' not in r.content:
            if r.status_code in Alive_Status:
                u = urlparse(str(r.url))
                return u.scheme+'://'+u.netloc
    except:
        pass
    try:
        r = requests.get(url=url.replace('http://','https://'), headers=headers, verify=False, timeout=10)
        if b'Service Unavailable' not in r.content and b'The requested URL was not found on' not in r.content and b'The server encountered an internal error or miscon' not in r.content:
            if r.status_code in Alive_Status:
                u = urlparse(str(r.url))
                return u.scheme + '://' + u.netloc
    except:
        return None


def Get_Alive_Url(urls):
    with ThreadPoolExecutor(max_workers=pool_count*4) as p:
        future_tasks = [p.submit(Requests, i) for i in urls]
    result = [obj.result() for obj in future_tasks if obj.result() is not None]
    return result

def Baidu_Api(domain):
    result = set()
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7',
               'Cache-Control': 'max-age=0', 'Connection': 'keep-alive',
               'Host': 'ce.baidu.com', 'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    url = 'http://ce.baidu.com/index/getRelatedSites?site_address=' + domain
    try:
        r = requests.get(url, headers=headers, timeout=10, verify=False)
        content = r.json()
        data = content.get('data')
        for u in data:
            if u.get('domain') != None:
                result.add(u.get('domain'))
    except Exception as e:
        pass
    print('[+ BaiDu API] 百度接口 : {} 捕获子域名总数 : {}'.format(domain, len(result)))
    return list(result)


def CertSh_Api(domain):
    domain_links = set()
    result = set()
    try:
        url = 'https://crt.sh/?q='+domain
        r = requests.get(url=url,timeout=20, verify=False)
        links = re.findall(b'<A href="(\?id=\d.+)">',r.content)
        for link in links:
            domain_links.add('https://crt.sh/'+link.decode())
        for domain_link in domain_links:
            try:
                r1 = requests.get(url=domain_link,timeout=20, verify=False)
                if b'Subject&nbsp;Alternative&nbsp;Name:&nbsp;' in r1.content:
                    domains = re.findall(b'DNS:(.*?)<BR>', r1.content)
                    for domain_ in domains:
                        if domain in domain_.decode():
                            result.add(domain_.decode().replace('*.', ''))
            except Exception as e:
                pass
    except Exception as e:
        pass
    print('[+ CertSh API] CertSh接口 : {} 捕获子域名总数 : {}'.format(domain, len(result)))
    return list(result)

def Sec_Api(domain):
    result = set()
    try:
        url = "https://api.securitytrails.com/v1/domain/{}/subdomains".format(domain)
        querystring = {"apikey":seckey}
        response = requests.request("GET", url, params=querystring)
        rest = (response.json())
        subdomains = rest['subdomains']
        for s in subdomains:
            result.add(s+'.'+domain)
    except:
        pass
    print('[+ SecurityTrails API] SecTra接口 : {} 捕获子域名总数 : {}'.format(domain, len(result)))
    return list(result)

def Api(domain):
    result = set()
    mid = set()
    Baidu_res = Baidu_Api(domain)
    CertSh = CertSh_Api(domain)
    SecTra = Sec_Api(domain)
    Baidu_res.extend(CertSh)
    Baidu_res.extend(SecTra)
    if Baidu_res != [] and Baidu_res != None:
        for u in Baidu_res:
            bla = check_black(u)
            if bla == False:
                mid.add('http://'+u)
    if mid != {}:
        result = Get_Alive_Url(list(mid))
        print('[+ BaiDu CertSh SecTra API] 接口 : {} 捕获子域名存活总数 : {}'.format(domain, len(result)))
    if result != []:
        return result

if __name__ == '__main__':
    print(Api('baidu.com'))