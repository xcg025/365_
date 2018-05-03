import urllib.request
import urllib.parse
import urllib.error
import json
import logging
import http.cookiejar

# #不带参数的请求
# response = urllib.request.urlopen('http://www.baidu.com')
# print(response.read().decode('utf-8'))

# #带参数的请求
# data = bytes(urllib.parse.urlencode({'word':'hello'}), encoding='utf-8')
# response = urllib.request.urlopen('http://httpbin.org/post', data=data)
# print(response.read().decode('utf-8'))

#超时请求
# try:
#     response = urllib.request.urlopen('http://httpbin.org/get', timeout=1)
#     print(response.read().decode('utf-8'))
# except urllib.error.URLError as e:
#     print(e.reason)
#     logging.exception(e)

# #状态码和响应头
# response = urllib.request.urlopen('https://www.baidu.com')
# print(response.status)
# print(response.getheaders())
# print(response.getheader('Server'))

# #完整的参数请求
# url = 'http://httpbin.org/post'
# headers = {
#     'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
#     'Host': 'httpbin.org'
# }
# dict = {'name':'germy'}
# data = bytes(urllib.parse.urlencode(dict), encoding='utf-8')
# #构建Request对象
# # request = urllib.request.Request(url, data, headers,method='POST')
# #也可以这样写
# request = urllib.request.Request(url, data, method='POST')
# request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
#
# #请求request对象
# response = urllib.request.urlopen(request)
# print(response.read().decode('utf-8'))

# #代理
# proxy_handler = urllib.request.ProxyHandler({
#     'http': 'http://27.215.99.59:8888',
#     'https': 'https://111.230.24.24:3128'
# })
#
# opener = urllib.request.build_opener(proxy_handler)
# response = opener.open('http://www.baidu.com')
# print(response.read().decode('utf-8'))

# #cookie
# cookie = http.cookiejar.CookieJar()
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# opener.open('http://www.baidu.com')
# for item in cookie:
#     print(item.name + '=' + item.value)

# #cookie 文件
# filename = 'cookie.txt'
# cookie = http.cookiejar.MozillaCookieJar(filename)
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# opener.open('http://www.baidu.com')
# cookie.save(ignore_discard=False, ignore_expires=False)

#异常处理
try:
    response = urllib.request.urlopen('http://cuiqingcai.com/index.htm')
except urllib.error.URLError as e:
    if hasattr(e, 'code'):
        print(e.code)
    if hasattr(e, 'reason'):
        print(e.reason)
# except urllib.error.HTTPError as e:
#     print('HTTPError')
#     print(e.reason, e.code, e.headers, sep='\n')
# except urllib.error.URLError as e:
#     print('URLError')
#     print(e.reason)
# else:
#     print('what')
