# test.py
#
# coding=utf-8
import requests
import os, sys,time, json, random, datetime
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

# 清输入你的 cookie
MY_COOKIE = "xxxxxxxxxxxx"


# 当前文件的路径
pwd = os.getcwd()
project_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
sys.path.append(project_path)

from api.rest_api import RestApi
from proxy.proxy import NewProxyIp

import urllib3
urllib3.disable_warnings()
api = RestApi()

headers={
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/,webp,image/apng,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate, br",
		"Accept-Language":"zh-CN,zh;q=0.9",
		"Cache-Control":"max-age=0",
		"Connection":"keep-alive",
		"Cookie":MY_COOKIE,
		"Host":"www.tianyancha.com",
		"Upgrade-Insecure-Requests":"1",
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like ,Gecko) Chrome/72.0.3626.96 Safari/537.36",
	}


def create_tyc_cid(data):
	try:
		api.tyc_cid(data)
	except Exception as e:
		print (" api request fail 	. 	.		. ", format(e)) # 接口请求失败


file_name_load = "./company_url/new/"

def write_file(data_list,company_url_id,city,page,count,search_url):

	file_name = file_name_load+str(count)+"_"+city+".csv"
	with open(file_name, 'a+', encoding='utf-8') as f:
		writer = f.write(company_url_id+","+search_url+'\n')

# 进入每个城市
def open_city_list_page_url(search_url):
	s=requests.session()
	rs = requests.get(search_url, headers=headers, verify=False)
	rs.encoding = 'utf-8'
	data_list_city = BeautifulSoup(rs.text, "lxml")
	# print(data_list_city)
	return data_list_city

# url = "https://www.tianyancha.com/search?base=bj"

# open_city_list_page_url(url)


# 拿到各个公司的url city url
def check_company_cid(list_city_urls,city,page,search_url):
	# list_city_url = company_list.select('div.content>div.header')
	cids = ''
	for company_one_url in list_city_urls:
		company_url = company_one_url.find_all('a')[0].get('href')
		company_url_id = company_url.split("company/")[1]
		# print(company_url+"=="+city+"===="+page)

		# write_file(company_url,company_url_id,city,page,count,search_url)

		# search_one_company(company_url, city)
		#
		cids = cids + ','+ company_url_id

	data = {'city': city, 'cids': cids, 'url': search_url}

	create_tyc_cid(data)

# 拿到各个城市url
#
def check_one_city(city_name, city_abbr):
	code = [110108,110109,110111,110112,110113,110114,110115,110116,110117,110118,110119,110228,110229]
	# company_city_urls_new = x.get('href')
	# city_name = x.getText()
	for x_code in code:
		x_code_str = "?"+"&base="+str(city_abbr)+"&areaCode="+str(x_code)
		for x_ot in range(3,12):
		# for x_ot in range(2,3):
			url_strff = "https://www.tianyancha.com/search/os1-ot"+str(x_ot)
			nex_url = url_strff + "/p1/" + x_code_str

			print("========================== 即将爬取新的数据 ==========================")
			print(nex_url)
			print("请输入总本次数据总页数, page=====")

			page_size = input("");
			for x_page in range(1,int(page_size)):
				page = str(x_page)
				# https://www.tianyancha.com/search/os1-ot2/p2?base=bj&areaCode=110101
				search_url = url_strff +"/p"+page+ x_code_str
				print(search_url)

				company_list_text = open_city_list_page_url(search_url)

				company_urls = company_list_text.select('div.content>div.header')
				# print(company_urls)
				print(len(company_urls))

				if len(company_urls)> 2:
					check_company_cid(company_urls,city_name,page, search_url)
				else:
					current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
					print(current_time)
					print("页数进度："+ str(x_page) +"/"+ str(page_size) + "需要手工验证, 1: 继续爬取; 0: 该页已爬取完成，跳出。")
					input_str = input("");
					if input_str == "1":
						print("Received input is : ", input_str  )
					elif input_str == "0":
						print("Received input is : ", input_str  )
						# continue
						break
						# check_company_cid(company_urls,city_name,page, search_url)
				time.sleep(random.randint(2,3))

city_name = "北京"
city_abbr = "bj"
check_one_city(city_name, city_abbr)
