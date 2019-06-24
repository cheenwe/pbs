
# -*- coding: utf-8 -*-
# python  with oracle
# https://github.com/oracle/odpi


import cx_Oracle
#引用模块cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

conn=cx_Oracle.connect("trff_zjk/trff_zjk@192.168.50.10:1521/orcl")

#连接数据库
c=conn.cursor()

sql="SELECT * FROM ( SELECT A.*, ROWNUM RN FROM (SELECT * FROM WX_ZPXX_20181227) A WHERE ROWNUM <= 40 ) WHERE RN >= 21"
#获取cursor
x=c.execute(sql)

root_path = "/home/ubuntu/python/upgrade_dir/"

def write_file(data, filename):

  # file_1 =root_path  str(item[0])+'.jpg'
  file = open(filename, "wb")
  file.write(data)
  file.close()
  pass

#使用cursor进行各种操作
list=x.fetchall()
for item in list:

  hpzl = item[0]
  hphm = item[1]

  cjjg = item[5]
  cjjgmc = item[6]
  wfsj = item[7]
  wfdd = item[8]
  wfxw = item[9]

  print(hpzl)
  print(hphm)

  photo1_data = item[3].read()

  if len(photo1_data) > 0:
    photo1_url = root_path + str(item[0])+'_1.jpg'
    write_file(photo1_data, photo1_url)
  else:
    photo1_url=''

  photo2_data = item[3].read()

  if len(photo2_data) > 0:
    photo2_url = root_path + str(item[0])+'_2.jpg'
    write_file(photo2_data, photo2_url)
  else:
    photo2_url=''

  photo3_data = item[4].read()

  if len(photo3_data) > 0:
    photo3_url = root_path + str(item[0])+'_3.jpg'
    write_file(photo3_data, photo3_url)
  else:
    photo3_url=''

c.close()
#关闭cursor
conn.close()
#关闭连接
