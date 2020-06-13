# coding=utf-8
import requests
import os, sys,time, json, random, datetime
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
    folder_name = folder_name + "/" + "0.csv"
    with open(folder_name, 'a+') as f:
        writer = f.write(data)


# 进入每个公司详情页面
def search_one_company(company_url):
	rs = requests.get(company_url, verify=False)
	rs.encoding = 'utf-8'
	data = BeautifulSoup(rs.text, "lxml")
	title_list = data.find_all('div', class_="intern-wrap intern-item")
	res = ""
	for title in title_list:
		# print(title)
		name = title.find_all('a', class_="title ellipsis font")[0].getText()
		url = title.find_all('a', class_="title ellipsis font")[0].get("href")
		print(name, url)
		res = res + name+","+url+"\n"

	WriteInfo("/home/em/", res)


for i in range(1, 36):
    url = "https://www.shixiseng.com/interns?page="+str(i)+"&keyword=%E4%BA%A7%E5%93%81%E5%8A%A9%E7%90%86"
    print(url)
    search_one_company(url)
