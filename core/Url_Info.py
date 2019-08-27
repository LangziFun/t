# -*- encoding: utf-8 -*- 
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/5 21:46
@file: 获取网址信息.py
"""
import requests
requests.packages.urllib3.disable_warnings()
import re
import random
import time

_Headers = [
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

class Get_Url_Info:
    def __init__(self,url):
        self.url = url
        self.timeout = 10
        self.title = '获取失败'
        self.power = '获取失败'
        self.server = '获取失败'
        self.content = 'Error'
        self.headers = '获取失败'
        self.status = '1'
        self.result = {}

    def Requests(self):
        try:
            r = requests.get(url=self.url,headers={'User-Agent':random.choice(_Headers)},verify=False,timeout=self.timeout)
            try:
                encoding = requests.utils.get_encodings_from_content(r.text)[0]
                #print(encoding)
                content = r.content.decode(encoding,'replace')
                #print(content)
                return (content, r.headers, r.status_code)
            except:
                return (self.content, r.headers, r.status_code)
        except Exception as e:
            #print(e)
            return (self.content,self.headers,self.status)

    def get_title(self,content):
        if content == 'Error':
            return self.title
        try:
            title_pattern = '<title>(.*?)</title>'
            title = re.search(title_pattern, content, re.S | re.I).group(1)
            return title.replace('\n', '').strip()
        except:
            return self.title

    def get_headers(self,headers):
        if headers == '获取失败':
            return (self.power,self.server)
        power,server=headers.get('Server'), headers.get('X-Powered-By')
        power = [power if power is not None else self.power][0]
        server = [server if server is not None else self.power][0]
        return (power,server)

    def get_info(self):
        req = self.Requests()
        content = req[0]
        headers = req[1]
        status = req[2]
        title = self.get_title(content)
        power,server = self.get_headers(headers)
        self.result = {
            'url':self.url,
            'title':title,
            'power':power,
            'server':server,
            'content':content,
            'status':status
        }
        #print(self.result)
        return self.result

if __name__ == '__main__':
    print(Get_Url_Info('http://t.wanmei.com/').Requests()[0])
    # a = Get_Url_Info('http://t.wanmei.com/')
    # print(a.get_info())
    # '''
    # 传入数据为 网址
    # 返回数据为
    # {
    # url 网址
    # title 标题
    # power WEB容器
    # server 服务器
    # content 网页内容
    # status 状态码
    # }
    # '''