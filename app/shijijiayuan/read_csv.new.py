# coding=utf-8

import requests
import csv
import os, sys,time, json
from bs4 import BeautifulSoup
from login import GetUserCookie
#当前文件的路径
pwd = os.getcwd()
project_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
sys.path.append(project_path)

from util.config import GetConfig

configs = GetConfig()

from proxy.proxy_valid import ValidIp
from api.rest_api import RestApi
from util.util_function import CheckDir, DownloadFile, WriteInfo

from util.log_handler import LogHandler

log = LogHandler('read_csv')

api = RestApi()


# proxies = ValidIp('1','http://www.jiayuan.com')
proxies = ValidIp(True,'http://www.jiayuan.com')

#当前文件的路径

# csv_path = project_path+'\logs\csv\\'
csv_path = project_path+'/app/shijijiayuan/need_check.new.csv'

#输出文件夹
out_dir = './download.new'

# def GetUserCookie():
#   img_url=str(configs.user_img_url) #'http://www.jiayuan.com/18126809'
#   s=requests.session()
#   # print(s.cookies.get_dict())#先打印一下，此时一般应该是空的。
#   res=s.get(img_url,proxies=proxies[0], stream=True)
#   data= {
#     'name':str(configs.user_name),
#     'password':str(configs.user_password),
#     'remem_pass':'on',
#     'ajaxsubmit':1,
#     'ljg_login':1,
#   }

#   rs=s.post(login_url,data)
#   c=requests.cookies.RequestsCookieJar()#利用RequestsCookieJar获取
#   # c.set('cookie-name','cookie-value')
#   s.cookies.update(c)
#   return s.cookies.get_dict()

MYCOOKIE = GetUserCookie(proxies)
print(MYCOOKIE)


def create_user_with_photos(data):
	try:
		api.create_user_with_photos(data)
	except Exception as e:

		log.error("api request fail: %s", format(e)) # 接口请求失败

def check_html(photo_hash, data, folder_name):

	try:
		#判断性别
		photo_list_text = data.find_all('li', class_="cur")[0].get_text()  # .find_all("a").get_text()
		info_list = data.find_all('p', class_="yh")[0].get_text()
		sex_text = photo_list_text.split("的")[0]
		# print(photo_list_text.split("的")[0])
		if sex_text == "他":
			sex_text = "男"
		else:
			sex_text = "女"
		base_info = sex_text + ", " + info_list
		# print(base_info)
		WriteInfo(folder_name, base_info)

		# log.info("write csv succss: " + base_info)
		#

		# 检查图片并下载
		dls = data.find(id='phoBig').find("ul").find_all('img')
		# print(dls)
		i = 1

		photo_list = ''
		for target_list in dls:
			url = target_list.get('src')
			print(str(i) + ", " + url)
			i = i + 1
			file_name= str(i) + ".jpg"
			# print(folder_name.split("/")[-1])
			DownloadFile(url, folder_name, file_name)

			photo = url + ","
			photo_list += photo

		folder_info = folder_name.split('/')
		uid = folder_info[-1]
		photo_num = folder_info[-2]

		log.info("download  success:  " + photo_num  + "/" + uid   + "uid:  " + uid )
		data = {'uid': uid, 'photo_num': photo_num, 'photo_hash': photo_hash, 'sign': 1, 'base_info': base_info, 'photos': photo_list }

		create_user_with_photos(data)


	except Exception as e:
		log.error("check photo error: " + photo_hash)

		# proxies = ValidIp(True,'http://www.jiayuan.com')

		# print(" x		.		. 	. 	x", format(e))  # 账户已关闭

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

	try:
		rs = requests.get(photo_hash, headers=headers, cookies=MYCOOKIE, verify=False)
		rs.encoding = 'utf-8'
		# print(rs.text)
		data = BeautifulSoup(rs.text, "lxml")
		# log.info(data)
		check_html(photo_hash, data, folder_name)
	except Exception as e:
		proxies = ValidIp(True,'http://www.jiayuan.com')
		VisitPage(photo_hash, download_folder, proxies[0])
		print(e)

# print(csv_path)
# csv_files = os.listdir(csv_path)
# for file in csv_files:
# 	print(file)
csv_file = csv.reader(open(csv_path,'r'))
# # 遍历文件内容
o_id = 0
for line in csv_file:
	# print(proxies[0])
	# u_num = line[0]
	# u_id = line[1].strip(' ')
	photo_hash = line[0]
	# print(photo_hash)
	o_id  += 1

	download_folder = "new" + "/" + str(o_id)
	# print(photo_hash)
	# print(download_folder)
	VisitPage(photo_hash, download_folder, proxies[0])
	# o_id  += 1

	# if o_id % 500 == 0:
	# 	proxies = ValidIp(True,'http://www.jiayuan.com')

