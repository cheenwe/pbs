# test.py
# 
# coding=utf-8
import requests
import os, sys,time, json, random
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq


# 当前文件的路径
pwd = os.getcwd()
project_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
sys.path.append(project_path)

from api.rest_api import RestApi
from proxy.proxy import NewProxyIp

headers={
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/,webp,image/apng,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate, br",
		"Accept-Language":"zh-CN,zh;q=0.9",
		"Cache-Control":"max-age=0",
		"Connection":"keep-alive",
		"Cookie":"TYCID=c1218cf02e9f11e9911c9dc4171947d6; ,undefined=c1218cf02e9f11e9911c9dc4171947d6; ssuid=2545690930; _ga=GA1.2.839871124.1549931133; aliyungf_tc=AQAAALdRhyeTWg0AFtfsdApA+ym8okvy; csrfToken=tC9P9mGPi86zs6wcWSbBE3Xf; bannerFlag=true; _gid=GA1.2.813379865.1550451708; cloud_token=629d73a37efc4df4b742b255f992b5cc; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1550131133,1550194180,1550208148,1550627582; token=219713728f904d8385d1796db9871e23; _utm=1bad2f89116a436cbf61dd19daad0dbc; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%25BB%25BA%25E5%25AE%2581%25E5%2585%25AC%25E4%25B8%25BB%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25225%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522surday%2522%253A%2522365%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25221%2522%252C%2522monitorUnreadCount%2522%253A%25221%2522%252C%2522onum%2522%253A%25222%2522%252C%2522isExpired%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODk3OTY4NTI3OSIsImlhdCI6MTU1MDYyODc3NywiZXhwIjoxNTY2MTgwNzc3fQ.AKVA1JeEgwQskIOsMdL4P9sm97A5gWnk129kFEs0-C83lLj6N99nTb9rjXv_fnS0uQMKi7SJh5spUvPbSFGPuw%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%252220%2522%252C%2522mobile%2522%253A%252218979685279%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODk3OTY4NTI3OSIsImlhdCI6MTU1MDYyODc3NywiZXhwIjoxNTY2MTgwNzc3fQ.AKVA1JeEgwQskIOsMdL4P9sm97A5gWnk129kFEs0-C83lLj6N99nTb9rjXv_fnS0uQMKi7SJh5spUvPbSFGPuw; _gat_gtag_UA_123487620_1=1; __insp_wid=677961980; __insp_nv=true; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20v; __insp_targlpt=5aSp55y85p_lLeWVhuS4muWuieWFqOW3peWFt1%2FkvIHkuJrkv6Hmga%2Fmn6Xor6Jf5YWs5Y_45p_l6K_iX_W3peWVhuafpeivol%2FkvIHkuJrkv6HnlKjkv6Hmga%2Fns7vnu58%3D; __insp_ss=1550635432129; __insp_norec_sess=true; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1550635436; __insp_slim=1550635436417",
		"Host":"www.tianyancha.com",
		"Upgrade-Insecure-Requests":"1",
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like ,Gecko) Chrome/72.0.3626.96 Safari/537.36",
	}


# 进入每个城市
def search_company_list(serach_url):

	s=requests.session()
	
	rs = requests.get(serach_url, headers=headers, verify=False)
	rs.encoding = 'utf-8'
	data_list_city = BeautifulSoup(rs.text, "lxml")
	print(data_list_city)

url = "https://www.tianyancha.com/search?base=bj"

search_company_list(url)
