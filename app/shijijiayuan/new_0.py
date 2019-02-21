# coding=utf-8
# 根据用户起始id去爬取数据并传入服务器

import requests
import csv
import os, sys,time, json
from bs4 import BeautifulSoup
from login import GetUserCookie
from pyquery import PyQuery as pq
# from tomorrow import threads
import random
#当前文件的路径
pwd = os.getcwd()
project_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
sys.path.append(project_path)
print(project_path)
from proxy.proxy_valid import ValidIp
from api.rest_api import RestApi
from util.util_function import CheckDir, DownloadFile, WriteInfo

from util.log_handler import LogHandler

from util.config import GetConfig

# log = LogHandler('read_csv')
log = LogHandler('new_0')

api = RestApi()


configs = GetConfig()


# proxies = ValidIp(True,'http://www.jiayuan.com')


proxies = ValidIp(True,'http://www.jiayuan.com')

print(proxies)

url_address = 'http://www.jiayuan.com/'

#当前文件的路径

csv_path = project_path+'\logs\csv\\'

#输出文件夹
out_dir = './download_new'

MYCOOKIE = GetUserCookie()

error_num = 0

def create_user_with_photos(data):
	try:
		api.create_user_with_photos(data)
	except Exception as e:

		log.error("api request fail: %s", format(e)) # 接口请求失败

def check_html(photo_hash, data, folder_name):
	try:
		# photo info
		photo_list_text = data.find_all('li', class_="cur")[0].get_text()
		# person info
		info_list = data.find_all('p', class_="yh")[0].get_text()
		#判断性别
		sex_text = photo_list_text.split("的")[0]

		if sex_text == "他":
			sex_text = "男"
		else:
			sex_text = "女"

		base_info = sex_text + ", " + info_list
		# print(base_info)
		WriteInfo(folder_name, base_info)

		# log.info("write csv succss: " + base_info)
		# 检查图片并下载
		dls = data.find(id='phoBig').find("ul").find_all('img')
		# print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

		# print(dls)
		# print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

		i = 1
		photo_list = ''
		for target_list in dls:
			url = target_list.get('src')
			#print(str(i) + ", " + url)
			i = i + 1
			file_name= str(i) + ".jpg"
			# print(folder_name.split("/")[-1])
			#
			if  int(configs.open_download) == 1:
				DownloadFile(url, folder_name, file_name)

			photo = url + ","
			photo_list += photo


		folder_info = folder_name.split('/')
		# print(folder_info)
		uid = folder_info[-1]
		photo_num = folder_info[-2]

		log.info("download  success:  " + str(photo_num)  + "/" + str(uid)  )

		if  int(configs.open_save_online) == 1:
			data = {'uid': uid, 'photo_num': photo_num, 'photo_hash': photo_hash, 'sign': 1, 'base_info': base_info, 'photos': photo_list }
			create_user_with_photos(data)

	except Exception as e:
		log.error("check photo error: " + photo_hash)

		proxies = ValidIp(True,'http://www.jiayuan.com')

		# print(" x     .       .   .   x", format(e))  # 账户已关闭

# 访问指定的网页
def VisitPage(photo_hash, download_folder, proxy_ip):

	folder_name = out_dir + "/" + download_folder
	CheckDir(folder_name)

	s=requests.session()
	headers={
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	}

	cookies = MYCOOKIE
	try:
		rs = requests.get(photo_hash, proxies=proxy_ip,  headers=headers, cookies=cookies, verify=False)
		rs.encoding = 'utf-8'
		# print(rs.text)
		data = BeautifulSoup(rs.text, "lxml")
		# print(data)
		check_html(photo_hash, data, folder_name)
	except Exception as e:
		print(e)

# @threads(5)
def CheckHtml(data, sn, proxy_ip):
	global error_num
	try:
		nav_text = data.find_all('ul', class_="nav_l")[0]
		photo_text = nav_text.find_all('li')[1]
		photo_title = photo_text.text
		photo_lik = photo_text.find('a').get("href")

		# print(photo_title)
		# print(photo_lik)
		try:
			if "的照片" in photo_title:
				num = int(photo_title.split('(')[1].strip(")"))

				log.info (num)
				if num > 2:
					data = str(num) + "," + str(sn) + "," + photo_lik
					# print (num)
					photo_hash_key = photo_lik.split('uid_hash=')[1].split('&')[0]
					photo_hash = "http://photo.jiayuan.com/showphoto.php?uid_hash="+photo_hash_key
					# http://photo.jiayuan.com/showphoto.php?uid_hash=97513ed75d4ee0b49977540cc28adeea&tid=0&cache_key=
					#调用接口
					# print( sn + "========================================")
					#
					download_folder = str(num) + "/" + str(sn)
					# print(photo_hash)
					# print(download_folder)
					# print(proxy_ip)
					VisitPage(photo_hash, download_folder, proxy_ip)
					# d = {'uid': sn, 'photo_num': num, 'photo_hash': photo_hash_key, 'sign': 1, }
					# create_user(d)
					# #写文件
					# write_file(data)
		except Exception as e:
			# print("no photo.          .       .       .               . ", format(e))  # 没有照片
			log.info("没有照片 %s", sn)
	except Exception as e:
		# print(" x           .               .       .       x", format(e))  # 账户已关闭
		log.info("uid:  %s  count: %s", str(sn), str(error_num) )
		error_num = error_num + 1
		if error_num%1000 == 0:
			proxies = ValidIp(True,'http://www.jiayuan.com')
			log.info("获取新ip %s", proxies)



# @threads(5)
def visit_page(sn, proxy_ip):
	url = url_address + str(sn)
	s = requests.session()
	headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Referer': url
	}
	cookies = MYCOOKIE
	try:
		rs = requests.get(url, proxies=proxy_ip,  headers=headers, cookies=cookies, verify=False)
		rs.encoding = 'utf-8'
		# print(rs.text)
		data = BeautifulSoup(rs.text, "lxml")
		# print(data)
		# print(proxy_ip)
		CheckHtml(data, sn, proxy_ip)
	except Exception as e:
		print(e)


# print(csv_path)
# csv_files = os.listdir(csv_path)
# for file in csv_files:
#   print(file)
#   csv_file = csv.reader(open(csv_path+file,'r'))
#   # # 遍历文件内容
#   o_id = 0
#   for line in csv_file:
#       # print(proxies[0])
#       u_num = line[0]
#       u_id = line[1].strip(' ')
#       photo_hash = line[2]
#       # print(photo_hash)
#       download_folder = u_num + "/" + u_id
#       VisitPage(photo_hash, download_folder, proxies[0])
#       o_id  += 1

#       if o_id % 500 == 0:
#           proxies = ValidIp(True,'http://www.jiayuan.com')



s_id = 12423715
e_id = 12425715

o_id = 0
for i in range(s_id, e_id):
	# print(i)
	visit_page(i, proxies[0])
	# o_id  += 1
	# if o_id % 200 == 0:
	# 	proxies = ValidIp(True,'http://www.jiayuan.com')
