# -*- encoding: utf-8 -*- 
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/6 9:14
@file: Brute.py
"""
import asyncio
import aiodns
import aiomultiprocess
import aiohttp
from urllib.parse import urlparse
import multiprocessing
import random

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

import django
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
django.setup()
from app.models import Setting,Domains

Set = Setting.objects.all()[0]
processes = int(Set.processes)
Alive_Status = eval(Set.Alive_Code)
childconcurrency = int(Set.childconcurrency)

Dicts = os.path.join('Auxiliary','SubDomainDict.list')
#Dicts = 'SubDomainDict.list'
sub_lists = list(set([x.strip() for x in open(Dicts,'r').readlines()]))


cert_path = os.path.join('Auxiliary','cacert.pem')
#cert_path = 'cacert.pem'
import aiodns,asyncio,socket,os,ssl
import socket
def get_host(url):
    try:
        s = socket.gethostbyname(url)
        return s
    except Exception as e:
        return None

def Get_Domain_From_Cert(domain):
    try:
        ip = get_host('www.'+domain)
        if ip == None:
            return None
        s = socket.socket()
        s.settimeout(2)
        connect = ssl.wrap_socket(s, cert_reqs=ssl.CERT_REQUIRED, ca_certs=cert_path)
        connect.settimeout(2)
        connect.connect((ip, 443))
        cert_data = connect.getpeercert().get('subjectAltName')
        res = [x[1] for x in cert_data if not x[1].startswith('*.') and x[1].endswith(domain)]
        if res != []:
            return res
        else:
            return None
    except Exception as e:
        return None



def Get_Url_Ip(domain):
    try:
        loop = asyncio.get_event_loop()
        resolver = aiodns.DNSResolver(loop=loop)
        f = resolver.query(domain, 'A')
        result = loop.run_until_complete(f)
        return result[0].host
    except Exception as e:
        return None


class Brute:
    def __init__(self,domain):
        self.domain = domain
        self.dicts = list(set([subdoma.strip() + '.' + self.domain for subdoma in sub_lists]))
        self.FakeDomain_IP = Get_Url_Ip('langzi.'+self.domain)

    async def check_url_alive(self,url):
        # print('Scan:'+url)
        async with asyncio.Semaphore(1000):
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                try:
                    async with session.get('http://'+url,timeout=15) as resp:
                        if resp.status in Alive_Status:
                            content = await resp.read()
                            #print(content)
                            if b'Service Unavailable' not in content and b'The requested URL was not found on' not in content and b'The server encountered an internal error or miscon' not in content:
                                u = urlparse(str(resp.url))
                                return u.scheme+'://'+u.netloc
                except Exception as e:
                    #print(e)
                    pass
                try:
                    async with session.get('https://' + url,timeout=15) as resp:
                        if resp.status in Alive_Status:
                            content = await resp.read()
                            #print(content)
                            if b'Service Unavailable' not in content and b'The requested URL was not found on' not in content and b'The server encountered an internal error or miscon' not in content:
                                u = urlparse(str(resp.url))
                                return u.scheme+'://'+u.netloc
                except Exception as e:
                    #print(e)
                    pass

    async def Aio_Subdomain(self,subdomain):
        # 传入参数为 xx.xx.com 返回结果为 xx.xx.com [解析结果]
        # 不存在则返回 NONE NOEN
        resolver = aiodns.DNSResolver(timeout=3)
        try:
            result = await resolver.query(subdomain, 'A')
            return subdomain, result[0].host
        except Exception as e:
            return None, None

    async def get_result_from_dns(self,subhosts):
        res = set()
        async with aiomultiprocess.Pool(processes=processes,childconcurrency=childconcurrency) as pool:
            # 如果你想跑满CPU 修改上面的线程和协程数量即可
            results = await pool.map(self.Aio_Subdomain, subhosts)
        for result in results:
            subdomain, answers = result
            if answers != None and subdomain != None:
                # res.add(subdomain)
                if answers != self.FakeDomain_IP:
                    # 这里则确认不存在泛解析,可以，但是没必要
                    res.add(subdomain)
                else:
                    res.add(self.FakeDomain_IP)
        return list(res)

    def get_result_from_dns_result(self,loop):
        # 返回结果是通过DNS查询获取的子域名
        result = loop.run_until_complete(self.get_result_from_dns(self.dicts))
        return result
        # if len(result) > 1329: # 泛解析
        #     return random.sample(result,10)
        # else:
        #     return result

    async def main(self,urls):
        async with aiomultiprocess.Pool(processes=processes,childconcurrency=childconcurrency) as pool:
            result = await pool.map(self.check_url_alive,urls)
        return [x for x in result if x is not None]


    def start(self):
        multiprocessing.freeze_support()
        loop = asyncio.get_event_loop()
        brute_domains = self.get_result_from_dns_result(loop)
        Cert_Domain_Counts = Get_Domain_From_Cert(self.domain)
        if Cert_Domain_Counts != None:
            print('[+ Cert Search] 查询 : {} SSL证书查询获取总子域名数量 : {}'.format(self.domain, len(Cert_Domain_Counts)))
            brute_domains.extend(Cert_Domain_Counts)
        print('[+ Brute Subdomain] 爆破 : {} 暴力破解获取总子域名数量 : {}'.format(self.domain,len(brute_domains)))
        alive_urls = loop.run_until_complete(self.main(brute_domains))
        print('[+ Alive Subdomain] 存活 : {} 暴力破解获取子域存活数量 : {}'.format(self.domain,len(alive_urls)))
        return alive_urls


if __name__ == '__main__':
    r = Brute('qq.com')
    res = r.start()
    print(res)