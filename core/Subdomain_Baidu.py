# -*- encoding: utf-8 -*- 
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/6 9:43
@file: Subdomain_Baidu.py
"""

import requests
import re
import time
from urllib.parse import quote,urlparse
requests.packages.urllib3.disable_warnings()
timeout = 15

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

servers = ['220.181.112.244','123.125.114.144','180.97.33.107','180.97.33.108','61.135.169.121','14.215.177.38','183.232.231.172','61.135.169.125']


def check_black(url):
    res = [True if x in url else False for x in black_list]
    if True in res:
        return True
    else:
        return False

headerss = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]


def Get_Resp(url):
    #headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7',  'Cookie': 'BAIDUID=832CF61CDAEF34C68E7CA06F591DF82A:FG=1; BIDUPSID=832CF61CDAEF34C68E7CA06F591DF82A; PSTM=1544962484; BD_UPN=12314753; __cfduid=db8c5e5983dc88b6b6b050ae548fbb7691556284097; H_WISE_SIDS=126125_127760_100807_135112_132060_135375_132550_120124_134719_132909_131247_122155_132439_130763_132378_131518_118879_118863_118856_118831_118792_107318_132783_134391_133351_132553_129652_132250_124893_128967_135346_133472_133838_133847_132552_134460_134319_134752_129645_131423_134665_134614_134029_134710_110085_134525_134155_127969_131951_131296_127417_134151_132468; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; sug=3; sugstore=1; ORIGIN=2; bdime=0; H_PS_PSSID=1453_21088_29523_29520_29098_29568_29221; delPer=0; BD_CK_SAM=1; PSINO=3; H_PS_645EC=4dbarFQevDh8Ep8JI9ziasOWlwrzN0L51q7gbGWsv5qAc10DvcdI%2F%2BQtcWo; BDSVRTM=151; COOKIE_SESSION=43_0_8_7_4_9_0_4_7_4_1_0_686925_0_0_0_1564749230_0_1566535736%7C9%230_1_1559812936%7C1', 'Host': 'www.baidu.com', 'is_pbs': 'site%3Abaidu.com', 'is_referer': 'https://www.baidu.com/s?wd=site%3Abaidu.com&pn=10&oq=site%3Abaidu.com&ie=utf-8&usm=1&rsv_idx=1&rsv_pq=e30afae6000592c2&rsv_t=6982O0bJr85Gwx%2Fqgo8X7V94%2FHfetEfbyNDSih3hJgDF40LXKT6zHLFdbyw&bs=site%3Abaidu.com', 'is_xhr': '1', 'Referer': 'https://www.baidu.com/s?wd=site%3Abaidu.com&pn=20&oq=site%3Abaidu.com&ie=utf-8&usm=1&rsv_idx=1&rsv_pq=993ebd5c00000988&rsv_t=4dbarFQevDh8Ep8JI9ziasOWlwrzN0L51q7gbGWsv5qAc10DvcdI%2F%2BQtcWo', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'}
    try:
        r = requests.get(url,timeout=10,verify=False)
        #print(r.content)
        return r.content
    except Exception as e:
        #print(e)
        baidu_url = url.split('//')[1].split('/')[0]
        baidu_server = random.choice(servers)
        url = url.replace(baidu_url,baidu_server)
        # print('替换地址:'+str(url))
        Get_Resp(url)


# def Get_Resp(url):
#     headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7', 'Connection': 'keep-alive', 'Cookie': 'BAIDUID=832CF61CDAEF34C68E7CA06F591DF82A:FG=1; BIDUPSID=832CF61CDAEF34C68E7CA06F591DF82A; PSTM=1544962484; BD_UPN=12314753; __cfduid=db8c5e5983dc88b6b6b050ae548fbb7691556284097; H_WISE_SIDS=126125_127760_100807_135112_132060_135375_132550_120124_134719_132909_131247_122155_132439_130763_132378_131518_118879_118863_118856_118831_118792_107318_132783_134391_133351_132553_129652_132250_124893_128967_135346_133472_133838_133847_132552_134460_134319_134752_129645_131423_134665_134614_134029_134710_110085_134525_134155_127969_131951_131296_127417_134151_132468; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; sug=3; sugstore=1; ORIGIN=2; bdime=0; H_PS_PSSID=1453_21088_29523_29520_29098_29568_29221; delPer=0; BD_CK_SAM=1; PSINO=3; H_PS_645EC=4dbarFQevDh8Ep8JI9ziasOWlwrzN0L51q7gbGWsv5qAc10DvcdI%2F%2BQtcWo; BDSVRTM=151; COOKIE_SESSION=43_0_8_7_4_9_0_4_7_4_1_0_686925_0_0_0_1564749230_0_1566535736%7C9%230_1_1559812936%7C1', 'Host': 'www.baidu.com', 'is_pbs': 'site%3Abaidu.com', 'is_referer': 'https://www.baidu.com/s?wd=site%3Abaidu.com&pn=10&oq=site%3Abaidu.com&ie=utf-8&usm=1&rsv_idx=1&rsv_pq=e30afae6000592c2&rsv_t=6982O0bJr85Gwx%2Fqgo8X7V94%2FHfetEfbyNDSih3hJgDF40LXKT6zHLFdbyw&bs=site%3Abaidu.com', 'is_xhr': '1', 'Referer': 'https://www.baidu.com/s?wd=site%3Abaidu.com&pn=20&oq=site%3Abaidu.com&ie=utf-8&usm=1&rsv_idx=1&rsv_pq=993ebd5c00000988&rsv_t=4dbarFQevDh8Ep8JI9ziasOWlwrzN0L51q7gbGWsv5qAc10DvcdI%2F%2BQtcWo', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'}
#     try:
#         r = requests.get(url,headers=headers,timeout=20,verify=False)
#         #print(r.content)
#         return r.content
#     except Exception as e:
#         #print(e)
#         return None

def Crawl_Bing(domain):
    result = set()
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-language": "zh-CN,zh;q=0.9",
        "alexatoolbar-alx_ns_ph": "AlexaToolbar/alx-4.0.3",
        "cache-control": "max-age=0",
        "upgrade-insecure-requests": "1",
        "cookie": "DUP=Q=axt7L5GANVktBKOinLxGuw2&T=361645079&A=2&IG=8C06CAB921F44B4E8AFF611F53B03799; _EDGE_V=1; MUID=0E843E808BEA618D13AC33FD8A716092; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=CADDA53D4AD041148FEB9D0BF646063A&dmnchg=1; MUIDB=0E843E808BEA618D13AC33FD8A716092; ISSW=1; ENSEARCH=BENVER=1; SerpPWA=reg=1; _EDGE_S=mkt=zh-cn&ui=zh-cn&SID=252EBA59AC756D480F67B727AD5B6C22; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; SRCHUSR=DOB=20190616&T=1560789192000; _FP=hta=on; BPF=X=1; SRCHHPGUSR=CW=1341&CH=293&DPR=1&UTC=480&WTS=63696385992; ipv6=hit=1560792905533&t=4; _SS=SID=252EBA59AC756D480F67B727AD5B6C22&HV=1560790599",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    for i in range(0,1000,10):
        time.sleep(random.randint(2,6))
        url = "https://cn.bing.com/search?q={}&ensearch=1&first={}".format('site:'+domain, i)
        try:
            r = requests.get(url,headers=headers,timeout=10,verify=False)
            urls = re.findall(b'<h2><a.*?href=\"(.*?)" h="ID=',r.content)
            for i in urls:
                deal_url = urlparse(i.decode())
                if domain in i.decode():
                    result.add(deal_url.scheme + '://' + deal_url.netloc)
               # print('bing:'+deal_url.scheme + '://' + deal_url.netloc)
        except Exception as e:
            #print('bing:'+str(e))
            pass
    print('[+ Bing Search] 必应搜索 : {} 捕获子域名总数 : {}'.format(domain,len(result)))
    return list(result)
        
def Crawl_Sougou(domain):
    result = set()
    for i in range(1,50):
        time.sleep(random.randint(2,6))
        url = "https://www.sogou.com/sogou?query={}&page={}".format('site:'+domain, i)
        u_quert = '/sogou?query=site:{}&page={}'.format(domain,i)
        try:
            headers = {'authority': 'www.sogou.com', 'method': 'GET', 'path': u_quert, 'scheme': 'https', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7', 'cookie': 'SUV=1545365636161081; SMYUV=1545365636162598; CXID=00BEDBD52384CAA240287B8117915D4C; SUID=7636BA753865860A5C289DDF000F3BB7; usid=meBNHqDlm_fUMnfS; ABTEST=0|1565523728|v17; SNUID=A1E230DE848613454C4960E38445C9AF; browerV=3; osV=1; taspeed=taspeedexist; pgv_pvi=7918682112; pgv_si=s90726400; sct=7; sst0=695; IPLOC=CN3100; ld=Hyllllllll2NF@DylllllVCKNK1lllll1PBvEyllllylllllVZlll5@@@@@@@@@@', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
            r = requests.get(url=url,headers=headers,timeout=10,verify=False)
            urls = re.findall(b'http://snapshot.sogoucdn.com/websnapshot\?ie=utf8&url=(.*?)%2F&did=',r.content)
            for i in urls:
                if domain in i.decode():
                    deal_url = urlparse(i.decode().replace('%3A%2F%2F','://'))
                    if '%2F' in deal_url.netloc:
                        result.add(deal_url.scheme + '://' + deal_url.netloc.split('%2F')[0])
                        #print(deal_url.scheme + '://' + deal_url.netloc.split('%2F')[0])
                    else:
                        result.add(deal_url.scheme + '://' + deal_url.netloc)
                        #print('sougou:'+deal_url.scheme + '://' + deal_url.netloc)
        except Exception as e:
            #print('sougou:'+str(e))
            pass
    print('[+ Sougou Search] 搜狗搜索 : {} 捕获子域名总数 : {}'.format(domain,len(result)))
    return list(result)

def Cralw_Baidu(domainkey):
    '''
    传递参数为子域名
    返回的是存在存在子域名的完整网址
    '''
    result = set()
    domain = domainkey.encode()
    for page in range(0,500,10):
        #time.sleep(random.randint(2,6))
        url = 'http://www.baidu.com/s?wd=site%3A{}&pn={}'.format(quote(domainkey),page)
        #print(url)
        try:
            resp = Get_Resp(url)
            # if not resp:
            #     resp = Get_Resp(url)
            if resp:
                subdomain = re.findall(b'-decoration:none;">(.*?)/&nbsp',resp)
                for x in subdomain:
                    #print(b'1111111:'+x)
                    if domain in x:
                        if b'http' in x:
                            if b'..' in x:
                                result.add(x.decode().split('..')[0].rstrip('/'))
                            else:
                                result.add(x.decode().rstrip('/'))
                            if b'&' in x:
                                result.add(x.decode().split('&')[0].rstrip('/'))
                            else:
                                result.add(x.decode().rstrip('/'))

                        else:
                            if b'..' in x:
                                result.add('http://'+x.decode().split('..')[0].rstrip('/'))
                            else:
                                result.add('http://'+x.decode().rstrip('/'))
                            if b'&' in x:
                                result.add('http://'+x.decode().split('&')[0].rstrip('/'))
                            else:
                                result.add('http://'+x.decode().rstrip('/'))

                subdomain = re.findall(b'style="text-decoration:none;">(.*?)/.*?class="c-tools',resp)
                for x in subdomain:
                    #print(b'2222222:'+x)
                    if domain in x:
                        if b'http' in x:
                            if b'..' in x:
                                result.add(x.decode().split('..')[0].rstrip('/'))
                            else:
                                result.add(x.decode().rstrip('/'))
                        else:
                            if b'..' in x:
                                result.add('http://' + x.decode().split('..')[0].rstrip('/'))
                            else:
                                result.add('http://' + x.decode().rstrip('/'))
        except Exception as e:
            #print(e)
            pass
    res = (list(set(result)))
    #print(res)
    print('[+ Baidu Search] 百度搜索 : {} 捕获子域名总数 : {}'.format(domainkey,len(res)))
    return res


def Baidu(domain):
    Baidu_Res = Cralw_Baidu(domain)
    Bing_Res = Crawl_Bing(domain)
    Sougou_Res = Crawl_Sougou(domain)
    res = []
    returl_result = set()
    res.extend(Baidu_Res)
    res.extend(Bing_Res)
    res.extend(Sougou_Res)

    for real in res:
        try:
            UA = random.choice(headerss)
            headers = {'User-Agent': UA, 'Connection': 'close'}
            r = requests.get(url=real, headers=headers, verify=False, timeout=timeout)
            time.sleep(0.5)
            if b'Service Unavailable' not in r.content and b'The requested URL was not found on' not in r.content and b'The server encountered an internal error or miscon' not in r.content:
                if r.status_code in Alive_Status:
                # 这里读取验证码即可
                    real_url = r.url.rstrip('/')
                    bla = check_black(real_url)
                    if bla == False:
                        returl_result.add(urlparse(real_url).scheme + '://' + urlparse(real_url).netloc)
        except Exception as e:
            # print(e)
            pass
    return list(set(returl_result))
    # 返回数据是完整的url，进过存活检测

if __name__ == '__main__':
    print(Baidu('baidu.com'))