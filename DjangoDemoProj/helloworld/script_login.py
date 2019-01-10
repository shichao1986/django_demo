# coding: utf-8

import sys
import urllib3
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count, Process, Manager

http = urllib3.PoolManager()

HOST = '10.6.3.29:8001'
URI = '/admin/login/'

def login(host, uri, debug=False):

    url = 'http://{}{}'.format(host, uri)
    request_heads = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': '{}'.format(host),
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    response = http.request('GET', url, headers=request_heads)
    cookies = response.headers['Set-Cookie'].split(';')

    cookie_dict = {}
    for item in cookies:
        item = item.strip()
        key = item.split('=')[0]
        value = item.split('=')[1]
        cookie_dict[key] = value

    if debug:
        print('receive csrftoken={}'.format(cookie_dict['csrftoken']))

    csrftoken = cookie_dict['csrftoken']
    soup = BeautifulSoup(response.data.decode(), features='html.parser')
    csrfmiddlewaretoken = soup.form.input['value']

    if debug:
        print('receive csrfmiddlewaretoken={}'.format(csrfmiddlewaretoken))

    request_heads = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': 138,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'csrftoken={}'.format(csrftoken),
        'Host': '{}'.format(host),
        'Origin': 'http://{}'.format(host),
        'Pragma': 'no-cache',
        'Referer': '{}'.format(url),
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    if debug:
        print('send cookie={}'.format(request_heads['Cookie']))

    fields = {
        'csrfmiddlewaretoken': '{}'.format(csrfmiddlewaretoken),
        'username': 'admin',
        'password': 'password2018',
        'next': '/admin/',
    }
    if debug:
        print('send csrfmiddlewaretoken={}'.format(fields['csrfmiddlewaretoken']))
        print('fields={}'.format(fields))

    response = http.request('POST', url, headers=request_heads, fields=fields, encode_multipart=False, redirect=False)

    return response.status

def foo():
    try:
        while True:
            login(HOST, URI)
    except Exception as e:
        print(e)


def main(argv=None):
    if argv == None:
        argv = sys.argv
    # try:
    #     for i in range(1000):
    #         login(HOST, URI)
    # except Exception as e:
    #     print(e)
    #     return -1

    task_num = cpu_count() * 4
    pool = Pool(processes=task_num)
    for i in range(task_num):
        pool.apply_async(foo)

    pool.close()
    pool.join()

    return 0

if __name__ == '__main__':
    sys.exit(main())





