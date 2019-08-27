# -*- encoding: utf-8 -*- 
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/6 9:55
@file: Subdomain_Crawl.py
"""

import requests
import re
requests.packages.urllib3.disable_warnings()
import time

import django
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
django.setup()
from app.models import Setting

Set = Setting.objects.all()[0]
processes = int(Set.processes)
Alive_Status = eval(Set.Alive_Code)
childconcurrency = int(Set.childconcurrency)

Dicts = os.path.join('Auxiliary','Black_Url.list')

black_list = list(set([x.strip() for x in open(Dicts, 'r', encoding='utf-8').readlines()]))
def check_black(url):
    res = [True if x in url else False for x in black_list]
    if True in res:
        return True
    else:
        return False

from urllib.parse import urlparse
from bs4 import BeautifulSoup


# @from JSFinder
def extract_URL(JS):
    pattern_raw = r"""
	  (?:"|')                               # Start newline delimiter
	  (
	    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
	    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
	    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
	    |
	    ((?:/|\.\./|\./)                    # Start with /,../,./
	    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
	    [^"'><,;|()]{1,})                   # Rest of the characters can't be
	    |
	    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
	    [a-zA-Z0-9_\-/]{1,}                 # Resource name
	    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
	    (?:[\?|/][^"|']{0,}|))              # ? mark with parameters
	    |
	    ([a-zA-Z0-9_\-]{1,}                 # filename
	    \.(?:php|asp|aspx|jsp|json|
	         action|html|js|txt|xml)             # . + extension
	    (?:\?[^"|']{0,}|))                  # ? mark with parameters
	  )
	  (?:"|')                               # End newline delimiter
	"""
    pattern = re.compile(pattern_raw, re.VERBOSE)
    result = re.finditer(pattern, str(JS))
    if result == None:
        return None
    js_url = []
    for match in result:
        if match.group() not in js_url:
            js_url.append(match.group().strip('"').strip("'"))
    return js_url


# Get the page source
def Extract_html(URL):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"}
    try:
        re = requests.get(URL, headers=header, timeout=3, verify=False)
        raw = re.content.decode("utf-8", "ignore")
        return raw
    except:
        return None
def process_url(URL, re_URL):
    black_url = ["javascript:"]  # Add some keyword for filter url.
    URL_raw = urlparse(URL)
    ab_URL = URL_raw.netloc
    host_URL = URL_raw.scheme
    if re_URL[0:2] == "//":
        result = host_URL + ":" + re_URL
    elif re_URL[0:4] == "http":
        result = re_URL
    elif re_URL[0:2] != "//" and re_URL not in black_url:
        if re_URL[0:1] == "/":
            result = host_URL + "://" + ab_URL + re_URL
        else:
            if re_URL[0:1] == ".":
                if re_URL[0:2] == "..":
                    result = host_URL + "://" + ab_URL + re_URL[2:]
                else:
                    result = host_URL + "://" + ab_URL + re_URL[1:]
            else:
                result = host_URL + "://" + ab_URL + "/" + re_URL
    else:
        result = URL
    return result

def find_last(string, str):
    positions = []
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1: break
        last_position = position
        positions.append(position)
    return positions

def find_by_url(url, js=False):
    if js == False:
        html_raw = Extract_html(url)
        if html_raw == None:
            # print("Fail to access " + url)
            return None
        # print(html_raw)
        html = BeautifulSoup(html_raw, "html.parser")
        html_scripts = html.findAll("script")
        script_array = {}
        script_temp = ""
        for html_script in html_scripts:
            script_src = html_script.get("src")
            if script_src == None:
                script_temp += html_script.get_text() + "\n"
            else:
                purl = process_url(url, script_src)
                script_array[purl] = Extract_html(purl)
        script_array[url] = script_temp
        allurls = []
        for script in script_array:
            # print(script)
            temp_urls = extract_URL(script_array[script])
            if len(temp_urls) == 0: continue
            for temp_url in temp_urls:
                allurls.append(process_url(script, temp_url))
        result = []
        for singerurl in allurls:
            url_raw = urlparse(url)
            domain = url_raw.netloc
            positions = find_last(domain, ".")
            miandomain = domain
            if len(positions) > 1: miandomain = domain[positions[-2] + 1:]
            # print(miandomain)
            suburl = urlparse(singerurl)
            subdomain = suburl.netloc
            # print(singerurl)
            if miandomain in subdomain or subdomain.strip() == "":
                if singerurl.strip() not in result:
                    result.append(singerurl)
        return result
    else:
        temp_urls = extract_URL(Extract_html(url))
        if len(temp_urls) == 0: return None
        result = []
        for temp_url in temp_urls:
            if temp_url not in result:
                result.append(temp_url)
        return result


def find_subdomain(urls, mainurl):
    url_raw = urlparse(mainurl)
    domain = url_raw.netloc
    miandomain = domain
    positions = find_last(domain, ".")
    if len(positions) > 1: miandomain = domain[positions[-2] + 1:]
    subdomains = []
    for url in urls:
        suburl = urlparse(url)
        subdomain = suburl.netloc
        # print(subdomain)
        if subdomain.strip() == "": continue
        if miandomain in subdomain:
            if subdomain not in subdomains:
                subdomains.append(subdomain)
    return subdomains

def Get_Subdomain(url):
    subdoi = []
    url_sche = urlparse(url).scheme+'://'
    b = find_by_url(url)
    for real_url in b:
        subdoi.append(urlparse(real_url).scheme + '://' + urlparse(real_url).netloc)
    e = find_subdomain(b,url)
    if e:
        for i in e:
            subdoi.append(url_sche + i)
    return subdoi


from bs4 import BeautifulSoup as bs
import random
requests.packages.urllib3.disable_warnings()
timeout = 5

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
first_cule = ['.com.cn', '.org.cn', '.net.cn', '.com', '.cn', '.cc', '.net', '.org', '.info', '.fun', '.one', '.xyz',
              '.name', '.io', '.top', '.me', '.club', '.tv']

def Crawl_Links(url):
    '''

    根据传入网址
    获取该网址页面中的网址
    需要进一步的判断
    '''
    result_list = []
    result_set = []
    try:
        UA = random.choice(headerss)
        headers = {'User-Agent': UA, 'Connection': 'close'}
        r = requests.get(url=url, headers=headers, verify=False, timeout=timeout)
        time.sleep(0.02)
        bp = bs(r.content, 'html.parser')
        for x in bp.select('li > a'):
            d = str(x)
            if 'nofollow' not in d and 'java' not in d and ';' not in d and '?' not in d and '#' not in d:
                try:
                    ddd = x['href']
                    for x in first_cule:
                        if x in ddd:
                            if 'http' in ddd:
                                # print ddd.split(x)[0] + x
                                result_list.append(ddd.split(x)[0] + x)
                except Exception as e:
                    #print(e)
                    pass
            else:
                pass
        for x in bp.select('td > a'):
            d = str(x)
            if 'nofollow' not in d and 'java' not in d and ';' not in d and '?' not in d and '#' not in d:
                try:
                    ddd = x['href']
                    for x in first_cule:
                        if x in ddd:
                            if 'http' in ddd:
                                # print ddd.split(x)[0] + x
                                result_list.append(ddd.split(x)[0] + x)
                except Exception as e:
                    #print(e)
                    pass
            else:
                pass
        for x in bp.select('p > a'):
            d = str(x)
            if 'nofollow' not in d and 'java' not in d and ';' not in d and '?' not in d and '#' not in d:
                try:
                    ddd = x['href']
                    for x in first_cule:
                        if x in ddd:
                            if 'http' in ddd:
                                # print ddd.split(x)[0] + x
                                result_list.append(ddd.split(x)[0] + x)
                except Exception as e:
                    #print(e)
                    pass
            else:
                pass
        for x in bp.select('div > a'):
            d = str(x)
            if 'nofollow' not in d and 'java' not in d and ';' not in d and '?' not in d and '#' not in d:
                try:
                    ddd = x['href']
                    for x in first_cule:
                        if x in ddd:
                            if 'http' in ddd:
                                # print ddd.split(x)[0] + x
                                result_list.append(ddd.split(x)[0] + x)
                except Exception as e:
                    pass
            else:
                pass
    except Exception as e:
        pass

    try:
        UA = random.choice(headerss)
        headers = {'User-Agent': UA, 'Connection': 'close'}
        r = requests.get(url=url, headers=headers, verify=False, timeout=timeout)
        time.sleep(0.02)
        pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.I)
        encoding = requests.utils.get_encodings_from_content(r.text)[0]
        res = r.content.decode(encoding, 'replace')
        urls = re.findall(pattern, res)
        for x in urls:
            a1, a2 = x.split('//')[0], x.split('//')[1].split('/')[0]
            a3 = ''.join(a1) + '//' + ''.join(a2)
            result_list.append(a3.replace("'", "").replace('>', '').replace('<', ''))
    except:
        pass

    result_list = list(set(result_list))
    subdomains = Get_Subdomain(url)
    if subdomains:
        result_list.extend(subdomains)
    result_list = list(set(result_list))
    success_list = []
    for real in result_list:
        # 对网址进行过滤
        if 'http' not in real:
            real_x = 'http://' + real
        else:
            real_x = real
        bla = check_black(real_x)
        if bla == False:
            success_list.append(urlparse(real_x).scheme + '://' + urlparse(real_x).netloc)
    success_list = list(set(success_list))


    # 返回数据是完整的url，并且经过了存活性检测

    returl_list = set()
    for u in success_list:
        try:
            UA = random.choice(headerss)
            headers = {'User-Agent': UA, 'Connection': 'close'}
            r = requests.get(url=u, headers=headers, verify=False, timeout=timeout)
            time.sleep(0.1)
            try:
                if b'Service Unavailable' not in r.content and b'The requested URL was not found on' not in r.content and b'The server encountered an internal error or miscon' not in r.content:
                    if r.status_code in Alive_Status:
                        real_url = r.url.rstrip('/')
                        returl_list.add(urlparse(real_url).scheme + '://' + urlparse(real_url).netloc)
            except:
                pass
        except:
            pass
    print('[+ Crawl UrlLinks] 爬行网址: {} 友链存活数量 : {}'.format(url,len(returl_list)))
    return list(returl_list)

def Crawl(url):
    result = Crawl_Links(url)
    if result == None or result == []:
        return []
    else:
        return result

if __name__ == '__main__':
    r = Crawl('http://www.langzi.fun')
    print(r)

