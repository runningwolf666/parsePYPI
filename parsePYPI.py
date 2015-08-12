#!/usr/bin/env python3
#-*- coding:utf-8 -*-
请在Python3下运行此程序='Please run this program with Python3'

from pyquery import PyQuery as pq  # API: http://pythonhosted.org/pyquery/api.html
import requests  # 快速上手： http://cn.python-requests.org/zh_CN/latest/user/quickstart.html 本页内容为如何入门Requests提供了很好的指引。
import time
import random


def calc_download(url):
    headers = {
        'Host': 'pypi.python.org',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.5',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:33.0) Gecko/20100101 Firefox/33.0',
        'Referer': 'https://pypi.python.org/pypi?:action=browse&c=533&show=all'
    }

    try:
        page = requests.get(url, headers=headers)
        content = page.content
        # print(content)
        d = pq(content)
        # for item in d('.nodot li:eq(3) span'):
        #     print(d(item).text())
        month_download = d('div.section ul.nodot:eq(0) li:eq(3) span').text()
        time.sleep(random.uniform(0.5, 1.0))  #wait a moment
        return month_download

    # requests.exceptions.ConnectionError: HTTPSConnectionPool(host='pypi.python.org', port=443): Max retries exceeded with url: /pypi/pybencoder/1.0 (Caused by <class 'ConnectionResetError'>: [Errno 104] Connection reset by peer)
    # 经常出现的Connection reset by peer: 原因可能是多方面的，不过更常见的原因是：①：服务器的并发连接数超过了其承载量，服务器会将其中一些连接Down掉；②：客户关掉了浏览器，而服务器还在给客户端发送数据；③：浏览器端按了Stop
    except requests.exceptions.ConnectionError as e:
        print('ERROR ---> {}'.format(e))
        time.sleep(3*60)
        return None
    except Exception as e:
        print('ERROR ---> {}'.format(e))
        time.sleep(3*60)
        return None

def parse_pypi():
    url = 'https://pypi.python.org/pypi?:action=browse&c=533&show=all'
    headers = {
        'Host': 'pypi.python.org',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:33.0) Gecko/20100101 Firefox/33.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://pypi.python.org/pypi'
    }

    try:
        page = requests.get(url, headers=headers)
        # content = page.content.decode('utf8')
        content = page.content
        # print(content)
        d = pq(content)
        for item in d('td a')[1:]: # 丢掉第一项
            href = d(item).attr('href')
            # href = '/pypi/elasticutils/0.10.3'
            url_prefix = 'https://pypi.python.org'
            hreflist.append(url_prefix + href)

            hrefname = href[len('/py/pi'):]
            hrefname = hrefname.replace('/', '_', 1)
            # hrefname = 'elasticutils_0.10.3'
            namelist.append(hrefname)

    # requests.exceptions.ConnectionError: HTTPSConnectionPool(host='pypi.python.org', port=443): Max retries exceeded with url: /pypi/pybencoder/1.0 (Caused by <class 'ConnectionResetError'>: [Errno 104] Connection reset by peer)
    # 经常出现的Connection reset by peer: 原因可能是多方面的，不过更常见的原因是：①：服务器的并发连接数超过了其承载量，服务器会将其中一些连接Down掉；②：客户关掉了浏览器，而服务器还在给客户端发送数据；③：浏览器端按了Stop
    except requests.exceptions.ConnectionError as e:
        print('ERROR ---> {}'.format(e))
        time.sleep(3*60)
        pass
    except Exception as e:
        print('ERROR ---> {}'.format(e))
        time.sleep(3*60)
        pass

# 初始化变量
hreflist = []
namelist = []
timestyle = time.strftime('%H%M%S')

# 获取包名字及链接，存入列表
parse_pypi()

# 写入结果，全部要分析的包名字及其链接
PPIlist = 'PPIlist_{}.txt'.format(timestyle)
for index,url in enumerate(hreflist):
    key = namelist[index]
    val = url
    s = "'{}':'{}', \n".format(key, val)
    with open(PPIlist, 'a') as f:
        f.write(s)

# 写入结果，包名字及其上月下载量
tongji = 'tongji_{}.txt'.format(timestyle)
for index,url in enumerate(hreflist):
    key = namelist[index]
    val = calc_download(url)
    s = "'{}':'{}', ".format(key, val)
    with open(tongji, 'a') as f:
        f.write(s)
    # print(key, val)





