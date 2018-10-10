# coding =utf-8

import requests
import json, sys
import random
from proxy.proxy import NewProxyIp

sys.path.append('..')

from util.log_handler import LogHandler

log = LogHandler('proxy')

# 
#2. 获取到代理后判断能否访问网站
# 

#获取ip,调用NewProxyIp()默认为在线获取，NewProxyIp("1")为本地代理获取
def GenNewIp(local):
	proxy = NewProxyIp(local) 
	return proxy

#验证IP地址是否能进入网站
#ValidIp('1','http://www.jiayuan.com' )
def ValidIp(local=True, valid_host='http://httpbin.org/ip'):
	#调用获取ip方法
	proxy = GenNewIp(local)
	# print(proxy)
	
	retry_count = 5
	# url = 'https://www.jiayuan.com'
	# url = "http://google.com/"
	timeout = 1
	headers = ""
	while retry_count > 0:
		try:
			# html = requests.get(url, headers=headers, timeout=timeout)#, proxies=proxy)
			html = requests.get(valid_host, headers=headers, timeout=timeout, proxies=proxy[0])
			# print(html.status_code)
			#判断是否拿到网页数据
			if html.status_code != 200:
				#数据获取失败再次请求
				res = ValidIp() 
				log.error("代理ip校验失败：%s", proxy[0])

			else:
				#数据获取成功返回ip
				# print(proxy)
				log.info(" ip校验成功")
				retry_count = -1
				return proxy
		except Exception:
			# print("visit count: %s", retry_count)

			retry_count -= 1
			log.error("代理ip校验失败, 重新获取代理ip，剩余次数：%s", retry_count)
			proxy = GenNewIp(local)
	# 出错5次, 删除代理池中代理
	return None

# print(ValidIp())
# res = ValidIp('1','http://www.jiayuan.com' )
# print(res)