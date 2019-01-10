# coding: utf-8

import urllib3
from urllib.parse import urlencode
from bs4 import BeautifulSoup

http = urllib3.PoolManager()
response = http.request('GET', 'http://10.6.3.29:8001/admin/login/')
cookies = response.headers['Set-Cookie'].split(';')
cookie_dict = {}
for item in cookies:
    item = item.strip()
    key = item.split('=')[0]
    value = item.split('=')[1]
    cookie_dict[key] = value
print('receive csrftoken={}'.format(cookie_dict['csrftoken']))
csrftoken = cookie_dict['csrftoken']
soup = BeautifulSoup(response.data.decode(), features='html.parser')
csrfmiddlewaretoken = soup.form.input['value']
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
    'Host': '10.6.3.29:8001',
    'Origin': 'http://10.6.3.29:8001',
    'Pragma': 'no-cache',
    'Referer': 'http://10.6.3.29:8001/admin/login/',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}
print('send cookie={}'.format(request_heads['Cookie']))
fields = {
    'csrfmiddlewaretoken': '{}'.format(csrfmiddlewaretoken),
    'username': 'admin',
    'password': 'password2018',
    'next': '/admin/',
}
print('send csrfmiddlewaretoken={}'.format(fields['csrfmiddlewaretoken']))

# fields = urlencode(fields)

print('fields={}'.format(fields))

response = http.request('POST', 'http://10.6.3.29:8001/admin/login/', headers=request_heads, fields=fields,
                        encode_multipart=False, redirect=False)

# import pdb;pdb.set_trace()




