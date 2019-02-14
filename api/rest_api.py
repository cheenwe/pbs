# coding =utf-8
import  requests

import sys

sys.path.append('..')

from util.config import GetConfig

configs = GetConfig()

host = 'http://'+ str(configs.host_ip) +':'+ str(configs.host_port)

class RestApi:
  def create_record(self,name):
    d = {'name': name}
    r = requests.post(host + '/data_records', data=d)
    # print(r.text)

  def create_video(self, id, name):
    d = {'name': name, 'id': id}
    r = requests.post(host + '/data_videos', data=d)
    # print(r.text)

  def create_file(self, id, name):
    d = {'name': name, 'id': id}
    r = requests.post(host + '/data_files', data=d)
    # print(r.text)

  def create_user(self, data):
    r = requests.post(host + '/api/v1/dc/users', data=data)
    # print(r.text)

  def create_user_with_photos(self, data):
    r = requests.post(host + '/api/v1/dc/user/photos', data=data)
    # print(r.text)

  def create_video(self, id, name):
    d = {'name': name, 'id': id}
    r = requests.post(host + '/data_videos', data=d)
    # print(r.text)

  def check_info(self):
    r = requests.get(host + '/api/v1/dc/check_info')
    return(r.text)
 
  def demo(self):
    r = requests.get('http://127.0.0.1:3001/users.json')
    return(r.text)
 

  #获取爬虫爬取用户id
  def get_uid(self, data):
    r = requests.get(host + '/api/v1/uid', data=data)
    # print(r.text)
    return(r.text)
