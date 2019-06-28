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

#使用本地代理获取ip
# https://github.com/qiyeboy/IPProxyPool
def GetLocalIp():
	r = requests.get(proxy_local_host)
	ip_ports = json.loads(r.text)
	num = random.randint(0, len(ip_ports))# 随机取一个数字
	# print("random num: %s", num)
	ip_ports = ip_ports[num]
	# ip_ports = random.choice(ip_ports)
	# print(len(ip_ports))
	ip = ip_ports[0]
	port = ip_ports[1]

	proxies = {
		'http': 'http://%s:%s' % (ip, port)
	}
	print(proxies)
	return [proxies, ip, len(ip_ports)]

#使用在线代理获取ip
# https://github.com/jhao104/proxy_pool
def GetOnlineIp():
	url = proxy_online_host + "/get"
	ip = str(requests.get(url).content)
	ip_port = ip.split("'")[1]
	proxies = {
		'http': 'http://%s' % "ip_port"
	}
	return [proxies, ip_port]

#
# 1.只调用一个方法，本地和网络均可用
def NewProxyIp(proxy_by="local"):

	if proxy_by == "local":
		#本地代理获取
		local_ip = GetLocalIp()
		# print(ip)
		log.info("获取本地代理ip成功,地址:  %s", local_ip)
		return local_ip

	elif proxy_by == "online":
		#在线代理获取
		online_ip = GetOnlineIp()
		log.info("获取在线代理ip成功,地址:  %s", online_ip)
		return online_ip
	else:
		log.error('获取ip失败')
		return -1

#
# 2.验证代理IP能否正常访问网站,返回 True/False
def vaildProxy(valid_host, proxies):
    # proxies = {"http": "http://{proxy}".format(proxy=proxy)}
    # print(proxies)
    headers={
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
      'Cache-Control': 'max-age=0',
      'Connection': 'keep-alive',
    }
    try:
        r = requests.get(valid_host, headers=headers, proxies=proxies, timeout=1, verify=False)
        if r.status_code == 200:
            log.info("ip校验成功")
            return True
        else:
            log.info("ip校验失败")
            return False
    except Exception:
        return False
        log.info("ip校验请求失败")


#
#3.验证请求能成功访问某网站的代理IP，N次请求到能访问的为至
#ValidIp("online",'http://www.jiayuan.com')
def ValidIp(proxy_by="local", valid_host='http://httpbin.org/ip'):
  #调用获取ip方法
  global proxy
  j=1
  retry_count = int(configs.proxy_max_retry_count)
  # print(retry_count)
  while retry_count > 0:
    log.info("校验次数剩余 %i", retry_count)
    proxy = NewProxyIp(proxy_by)[0]
    v_res = vaildProxy(valid_host, proxy)
    if v_res:
      return proxy
    else:
      proxy = NewProxyIp(proxy_by)[0]
      retry_count -= 1