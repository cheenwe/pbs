# coding=utf-8
# 根据用户起始id去爬取数据并传入服务器

import requests
import csv
import os, sys,time, json

from pyquery import PyQuery as pq
# from tomorrow import threads
import random
#当前文件的路径
pwd = os.getcwd()
project_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
sys.path.append(project_path)
print(project_path)
from api.rest_api import RestApi
from util.util_function import CheckDir, DownloadFile, WriteInfo

from util.log_handler import LogHandler

from util.config import GetConfig

# log = LogHandler('read_csv')
log = LogHandler('test_uid')

api = RestApi()

def get_uid(data):
	try:
		r = api.get_uid(data)
		return (json.loads(r)["data"])
	except Exception as e:
		log.error("api request fail: %s", format(e))


while True:
	data = {'need': 20000, 'remark': "im test"}
	
	uid = get_uid(data)

	log.info(uid)

	s_id = uid[0]
	e_id = uid[1]

	o_id = 0

	for i in range(s_id, e_id):
		print(i)
