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
# https://github.com/qiyeboy/IPProxyPool
def GetLocalIp():
	r = requests.get(proxy_local_host)
	ip_ports = json.loads(r.text)
	num = random.randint(0,80)
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
# https://github.com/jhao104/proxy_pool
def GetOnlineIp():

	url = proxy_online_host + "/get"
	ip = str(requests.get(url).content)
	ip_port = ip.split("'")[1]
	proxies = {
		'http': 'http://%s' % ip_port
	}
	return [proxies, ip_port]


#选择不同代理获取ip方法
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

# print(NewProxyIp("1"))
#
#2. 获取到代理后判断能否访问网站
#

# #获取ip,调用NewProxyIp()默认为在线获取，NewProxyIp("local")为本地代理获取
# def GenNewIp(proxy_by):
#   proxy = NewProxyIp(proxy_by)
#   return proxy

def testValid():

  proxy = NewProxyIp()
  proxies = proxy[0]

  url = 'http://www.jiayuan.com'
  req = requests.get(url,  proxies=proxies, timeout=10, verify=False)
  #判断是否拿到网页数据
  if req.status_code != 200:
    #数据获取失败再次请求
    proxy = NewProxyIp()
    res = ValidIp()
    print("代理ip校验失败：%s", proxy[0])

  else:
    #数据获取成功返回ip
    # print(proxy)
    print(" ip校验成功, ip地址：%s", proxy[0])


    return proxy

#验证IP地址是否能进入网站
#ValidIp("online",'http://www.jiayuan.com' )
def ValidIp(proxy_by="local", valid_host='http://httpbin.org/ip'):
  #调用获取ip方法
  proxy = NewProxyIp(proxy_by)
  # print(proxy)

  retry_count = int(configs.proxy_max_retry_count)
  # url = 'https://www.jiayuan.com'
  # url = "http://google.com/"
  timeout = 1
  headers={
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  }

  while retry_count > 0:
    try:
      # html = requests.get(url, headers=headers, timeout=timeout)#, proxies=proxy)
      # html = requests.get(valid_host, headers=headers, timeout=timeout, proxies=proxy[0])

      req = requests.get(valid_host, headers=headers, proxies=proxy[0], timeout=timeout, verify=False)
      # print(html.status_code)
      #判断是否拿到网页数据
      if req.status_code != 200:
        #数据获取失败再次请求
        proxy = NewProxyIp(proxy_by)
        res = ValidIp()
        log.error("代理ip校验失败：%s", proxy[0])

      else:
        #数据获取成功返回ip
        # print(proxy)
        loger.info(" ip校验成功, ip地址：%s", proxy[0])
        retry_count = -1
        return proxy
    except Exception:
      # print("visit count: %s", retry_count)

      retry_count -= 1
      log.error("代理ip校验失败, 重新获取代理ip，剩余次数：%s", retry_count)
      proxy = NewProxyIp(proxy_by)
      res = ValidIp()

  # 出错5次, 删除代理池中代理
  return None


