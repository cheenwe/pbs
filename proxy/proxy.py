# coding =utf-8

import json, random, sys
import requests

sys.path.append('..')

from util.config import GetConfig
from util.log_handler import LogHandler

configs = GetConfig()

log = LogHandler('proxy')

#本地ip
proxy_local_host = configs.proxy_local

#在线ip https://github.com/jhao104/proxy_pool
proxy_online_host = configs.proxy_online


# 
# 1.只调用一个方法，本地和网络均可用
#  
#  
#使用本地代理获取ip
def GetLocalIp():

	r = requests.get(proxy_local_host)
	ip_ports = json.loads(r.text)
	num = random.randint(0,10)
	# print("random num: %s", num)
	ip_ports = ip_ports[num]
	# ip_ports = random.choice(ip_ports)
	# print(ip_ports)
	ip = ip_ports[0]
	port = ip_ports[1]

	proxies = {
		'http': 'http://%s:%s' % (ip, port)
	}
	# print(proxies)
	return [proxies, ip]


#使用在线代理获取ip
def GetOnlineIp():

	url = proxy_online_host + "/get"
	ip = str(requests.get(url).content)
	ip_port = ip.split("'")[1]
	proxies = {
		'http': 'http://%s' % ip_port
	}
	return [proxies, ip_port]

 
#选择不同代理获取ip方法
def NewProxyIp(local=True):

	if local == True:
		#本地代理获取
		local_ip = GetLocalIp()
		# print(ip)
		log.info("获取本地代理ip成功,地址:  %s", local_ip[1])
		return local_ip

	elif local == "1":
		#在线代理获取
		online_ip = GetOnlineIp()
		log.info("获取在线代理ip成功,地址:  %s", online_ip[1])
		return online_ip

	else:
		log.error('获取ip失败')
		return -1

# print(NewProxyIp())


