import requests
import json
from requests.packages import urllib3
from requests.exceptions import ReadTimeout, ConnectTimeout

# #实例
# response = requests.get('http://www.baidu.com')
# print(type(response))
# print(response.status_code)
# print(type(response.text))
# print(response.text)
# print(response.cookies)

# #带参数的get请求
# data = {
#     'name' : 'zhangsan',
#     'age' : 18
# }
# response = requests.get(url='http://httpbin.org/get', params=data)
# print(response.text)

# #解析json
# response = requests.get('http://httpbin.org/get')
# print(type(response.text))
# print(response.text)
# print(type(json.loads(response.text)))
# print(json.loads(response.text))
# print(type(response.json()))
# print(response.json())
# print(type(response.content))
# print(response.content)

# #二进制
# response = requests.get('https://github.com/favicon.ico')
# with open('favicon.ico', 'wb') as f:
#     f.write(response.content)

# #添加headers
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
# }
# response = requests.get('https://www.zhihu.com/explore', headers=headers)
# # print(response.text)
# print(response.headers)
# print(requests.codes.not_found)

#会话维持
# requests.get('http://httpbin.org/cookies/set/number/123456789')
# response = requests.get('http://httpbin.org/cookies')
# print(response.text)

# s = requests.Session()
# s.get('http://httpbin.org/cookies/set/number/123456789')
# response = s.get('http://httpbin.org/cookies')
# print(response.text)

# #证书验证
# # response = requests.get('https://www.12306.cn')
# # print(response.status_code)
# urllib3.disable_warnings()
# response = requests.get('https://www.12306.cn', verify=False)
# print(response.status_code)

# #代理设置
# proxies = {
#     'http': 'http://27.215.99.59:8888',
#     'https': 'https://111.230.24.24:3128'
# }
# response = requests.get('http://www.baidu.com', proxies=proxies)
# print(response.status_code)

#超时设置
try:
    response = requests.get("http://httpbin.org/get", timeout=0.5)
    print(response.status_code)
except ReadTimeout:
    print('ReadTimeout')
except ConnectTimeout:
    print('ConnectTimeout')

