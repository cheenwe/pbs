# coding =utf-8
import  requests

import sys

sys.path.append('..')

from util.config import GetConfig

gg = GetConfig()

host = 'http://'+ str(gg.host_ip) +':'+ str(gg.host_port)

class RestApi:
  def create_record(self,name):
    d = {'name': name}
    r = requests.post(host + '/data_records', data=d)
    print(r.text)

  def create_video(self, id, name):
    d = {'name': name, 'id': id}
    r = requests.post(host + '/data_videos', data=d)
    print(r.text)

  def create_file(self, id, name):
    d = {'name': name, 'id': id}
    r = requests.post(host + '/data_files', data=d)
    print(r.text)
