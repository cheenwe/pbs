#coding=utf-8
import sys
import logging

sys.path.append('..')

from util.log_handler import LogHandler

# 引入模块
from api.rest_api import RestApi

# 初始化
api = RestApi()

#  创建处理记录
#  api.create_record(name)
#    传入参数:
#         name:  2018-04-09 晴 上午
#     返回参数 : 14
api.create_record(100)


#  创建视频记录
#  api.create_video(id, name)
#
#    传入参数:
#         id: 处理记录 返回 id
#         name:  视频处理后文件夹名
#     返回参数 : 11
api.create_video(1, "上方视频")

