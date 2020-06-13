# coding=utf-8
import requests
import os, sys,time, json, random, datetime, csv
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq


# 当前文件的路径
pwd = os.getcwd()
project_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
sys.path.append(project_path)

from api.rest_api import RestApi

import urllib3
urllib3.disable_warnings()
api = RestApi()

def check_text_by_title(data_text, css):
	return data_text.select(css)[0].get('title')

def check_by_text(data_text, css):
	return data_text.select(css)[0].getText()

def WriteInfo(folder_name, data):
    folder_name = folder_name + "/" + "info.csv"
    with open(folder_name, 'a+') as f:
        writer = f.write(data)


# 进入每个公司详情页面
def search_one_company(company_url):
	rs = requests.get(company_url, verify=False)
	rs.encoding = 'utf-8'
	data_text = BeautifulSoup(rs.text, "lxml")

	# c_log = data_text.find_all('img', class_="com_icon bgs")[0].get("src")
	# print(c_log)

	# 公司名     com_name      date
	try:
		job_name = data_text.find_all('div', class_="new_job_name")[0].get('title').replace("\n","enter")
		print(job_name)
	except:
		job_name=""
	
	try:
		date =  data_text.find_all('span', class_="job_money cutom_font")[0].getText().replace("\n","enter")
		print(date)
	except:
		date=""

	try:
		com_name =  data_text.find_all('a', class_="com-name")[0].getText().replace("\n","enter")
		print(com_name)
	except:
		com_name=""

	try:
		com_desc =  data_text.find_all('div', class_="com-desc")[0].getText().replace("\n","enter")
		print(com_desc)
	except:
		com_desc=""

	try:
		com_detail =  data_text.find_all('div', class_="com-detail")[0].getText().replace("\n","enter")
		print(com_detail)
	except:
		com_detail=""
	
	# try:
	# 	com_name =  data_text.find_all('a', class_="com-name")[0].getText()
	# 	print(com_name)
	# except:
	# 	com_name=""
	
	try:
		job_position =  data_text.find_all('span', class_="job_position")[0].get('title').replace("\n","enter")
		print(job_position)
	except:
		job_position=""

	try:
		com_position =  data_text.find_all('span', class_="com_position")[0].getText().replace("\n","enter")
		print(com_position)
	except:
		com_position=""

	try:
		academic =  data_text.find_all('span', class_="job_academic")[0].getText().replace("\n","enter")
		print(academic)
	except:
		academic=""

	try:
		content =  data_text.find_all('div', class_="job_detail")[0].getText().replace("\n","enter")
		print(content)
	except:
		content=""

	res = job_name+","+date+","+com_name+","+com_desc+","+com_detail+","+job_position+","+com_position+","+academic+","+content+"\n"

	WriteInfo("/home/em/", res)

csv_path ="/home/em/0.csv"

csv_file = csv.reader(open(csv_path,'r'))
# # 遍历文件内容
o_id = 0
for line in csv_file:
	time.sleep(3)
	o_id = o_id  + 1
	print(o_id)
	u_num = line[0]
	url = line[1]
	print(url)
	# url ="https://www.shixiseng.com/com/com_5shpd9rng9pj?mxa=asdd.0eqlx1._.$3"
	search_one_company(url)

# url ="https://www.shixiseng.com/intern/inn_lpx7ettb7kfc?pcm=pc_SearchList"
# search_one_company(url)