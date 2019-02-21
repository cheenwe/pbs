# coding=utf-8
# 根据用户起始id去爬取数据并传入服务器

import requests
import os, sys,time, json, random, csv
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from tomorrow import threads 

#当前文件的路径
pwd = os.getcwd()
project_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
sys.path.append(project_path)
# print(project_path)

from login import GetUserCookie
from proxy.proxy_valid import ValidIp
from api.rest_api import RestApi
from util.util_function import CheckDir, DownloadFile, WriteInfo
from util.log_handler import LogHandler
from util.config import GetConfig

# change: 定义当前爬虫名字
app = "uid4"

# change: 每次请求 uid 数量
req_nums = 200

log = LogHandler(app)

# 初始化
api = RestApi()
configs = GetConfig()

url_address = 'http://www.jiayuan.com/'

#当前文件的路径
csv_path = project_path+'\logs\csv\\'

#输出文件夹
out_dir = './download.new'

# cookie = GetUserCookie()

error_num = 0

# proxies = ValidIp(True,'https://www.jiayuan.com')

# 写csv文件
def WriteCsv(data):
	with open("need_check.csv", 'a+') as f:
		writer = f.write(data+'\n')
		#先写入columns_name
	pass

# # 请求代理 ip
# def RequestIp():
# 	global proxies
# 	proxies = ValidIp(True,'https://www.jiayuan.com')

# RequestIp()

# print(proxies)


# 请求Cookie
def GetCookie():
	global cookies
	cookies = GetUserCookie()

GetCookie()

# 下载文件
@threads(8)
def DownloadPicFile(url, folder_name, file_name):
	DownloadFile(url, folder_name, file_name)


def CreateUserPhoto(data):
	try:
		api.create_user_with_photos(data)
	except Exception as e:
		log.error("api request fail: %s", format(e)) # 接口请求失败


#=> 4.处理照片的网页,下载数据
# @threads(2)
def CheckPhotoHtml(photo_hash, data, folder_name):
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
				DownloadPicFile(url, folder_name, file_name)
			photo = url + ","
			photo_list += photo

		folder_info = folder_name.split('/')
		# print(folder_info)
		uid = folder_info[-1]
		photo_num = folder_info[-2]

		log.info("download  success:  " + str(photo_num)  + "/" + str(uid)  )

		if  int(configs.open_save_online) == 1:
			data = {'uid': uid, 'photo_num': photo_num, 'photo_hash': photo_hash, 'sign': 1, 'base_info': base_info, 'photos': photo_list }
			CreateUserPhoto(data)

	except Exception as e:
		log.error("check photo error: " + photo_hash)

		data = str(photo_hash) + "," + str(folder_name)

		WriteCsv(data)

		# RequestIp() #ValidIp(True,'https://www.jiayuan.com')

		# print(" x     .       .   .   x", format(e))  # 账户已关闭

#=> 3.访问指定带有照片的网页

# @threads(2)
def VisitPhotoPage(photo_hash, download_folder):

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
 
	try:
		rs = requests.get(photo_hash,   headers=headers, cookies=cookies, verify=False)
		rs.encoding = 'utf-8'
		# print(rs.text)
		data = BeautifulSoup(rs.text, "lxml")
		# print(data)
		CheckPhotoHtml(photo_hash, data, folder_name)
	except Exception as e:
		print(e)

#=> 2.分析html页面中是否存在照片信息,判断照片数大于n开始爬取页面照片
@threads(2)
def CheckUidHtml(data, uid):
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
					data = str(num) + "," + str(uid) + "," + photo_lik
					# print (num)
					photo_hash_key = photo_lik.split('uid_hash=')[1].split('&')[0]
					photo_hash = "http://photo.jiayuan.com/showphoto.php?uid_hash="+photo_hash_key
					# https://photo.jiayuan.com/showphoto.php?uid_hash=97513ed75d4ee0b49977540cc28adeea&tid=0&cache_key=
					#调用接口
					# print( uid + "========================================")
					download_folder = str(num) + "/" + str(uid)
					# print(photo_hash)
					# print(download_folder)

					# print(proxy_ip)
					VisitPhotoPage(photo_hash, download_folder)
					# d = {'uid': uid, 'photo_num': num, 'photo_hash': photo_hash_key, 'sign': 1, }
					# create_user(d)
					# #写文件
					# WriteCsv(data)

		except Exception as e:
			# print("no photo.          .       .       .               . ", format(e))  # 没有照片
			log.info("没有照片 %s", uid)
	except Exception as e:
		# print(" x           .               .       .       x", format(e))  # 账户已关闭
		log.info("uid:  %s  count: %s", str(uid), str(error_num) )
		error_num = error_num + 1
		# 錯誤次數超过xx次后更换cookie及代理ip
		if error_num%1000 == 0:
			# RequestIp()
			GetCookie()
			# ValidIp(True,'https://www.jiayuan.com')
			log.info("获取新ip %s")

#=> 1.批量检查uid,获取页面数据

# @threads(3)
def CheckUidPage(uid):
	url = url_address + str(uid)
	s = requests.session()
	headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Referer': url
	}
	print(url)
	try:
		rs = requests.get(url,   headers=headers, cookies=cookies, verify=False)
		rs.encoding = 'utf-8'
		# print(rs.text)
		data = BeautifulSoup(rs.text, "lxml")
		# print(data)
		# print(proxy_ip)
		CheckUidHtml(data, uid)
	except Exception as e:
			time.sleep(600)

			rs = requests.get(url,   headers=headers, cookies=cookies, verify=False)
			rs.encoding = 'utf-8'
			# print(rs.text)
			data = BeautifulSoup(rs.text, "lxml")
			# print(data)
			# print(proxy_ip)
			CheckUidHtml(data, uid)
		log.warning("访问页面失败,开始更换代理ip及cookie:", e)

		# RequestIp()
		GetCookie()
		# proxies = ValidIp(True,'https://www.jiayuan.com')
		try:
			rs = requests.get(url,   headers=headers, cookies=cookies, verify=False)
			rs.encoding = 'utf-8'
			# print(rs.text)
			data = BeautifulSoup(rs.text, "lxml")
			# print(data)
			# print(proxy_ip)
			CheckUidHtml(data, uid)
		except Exception as e:
			log.warning("访问页面失败*2,我也没办法了", e)

# 自动获取需要爬取用户id
def GetUid(data):
	try:
		r = api.get_uid(data)
		return (json.loads(r)["data"])
	except Exception as e:
		log.error("api request fail: %s", format(e))

while True:
	# 定义需要爬取的文件个数及爬虫名字
	data = {'need': req_nums, 'remark': app}

	uid = GetUid(data)

	log.info(uid)

	s_id = uid[0]
	e_id = uid[1]
	
	o_id = 0
	for i in range(s_id, e_id):
		CheckUidPage(i)
