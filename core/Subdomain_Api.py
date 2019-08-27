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
               'Cookie': 'BAIDUID=832CF61CDAEF34C68E7CA06F591DF82A:FG=1; BIDUPSID=832CF61CDAEF34C68E7CA06F591DF82A; PSTM=1544962484; __cfduid=db8c5e5983dc88b6b6b050ae548fbb7691556284097; H_WISE_SIDS=126125_127760_100807_131835_131364_132550_130510_132686_132799_120124_132313_132759_133016_132909_132460_132718_133044_131247_122155_132439_130763_132393_132379_132326_132212_131518_132261_118879_118863_131401_118856_118831_118792_131651_131575_132840_131534_131530_133159_131295_131871_132604_129565_107318_131795_132590_132783_131874_132709_131196_132565_132889_129652_124893_132557_132541_131035_131905_132293_132552_129835_128891_132307_129645_131423_131447_110085_127969_131506_123289_131297_127417_131549_131828_132626_132651_131959; BDUSS=VxWHlIYkk3eWdkaXpzaFE5QklnYTk2d0RPUVdnT3JmRjNZQ0ZUMGltVThDMFJkSVFBQUFBJCQAAAAAAAAAAAEAAADS9fNj0-~PxM600esAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADx-HF08fhxdRV; _ga=GA1.2.221138987.1565584366; cflag=13%3A3; locale=zh; PHPSESSID=iv5dan6nm0c86q3vurflinqho2; YII_CSRF_TOKEN=0d854bc5a5e97ef98ce2f158f6c9edc686850a7a; _pk_ses.1.a8c5=*; Hm_lvt_322d2c125c00316481e6b3696650e820=1566187278; _pk_id.1.a8c5=9a07802cbd7959bd.1566187278.1.1566187308.1566187278.; Hm_lpvt_322d2c125c00316481e6b3696650e820=1566187308; SERVERTAG=a9b40688f66d7a591cb72bd6826b65e5',
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