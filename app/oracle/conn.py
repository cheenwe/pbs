# -*- coding: utf-8 -*-
# python  with oracle
# https://github.com/oracle/odpi


from tomorrow import threads 
import cx_Oracle
#引用模块cx_Oracle
import os, time

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
 
conn=cx_Oracle.connect("trff_zjk/trff_zjk@192.168.50.10:1521/orcl")

# 连接数据库
c=conn.cursor()

down_path = "/tmp/test/"

@threads(16)
def write_file(data, filename):

  # file_1 = "/Users/chenwei/workspace/python/upgrade_dir/"+ str(item[0])+'.jpg'
  file = open(filename, "wb")
  file.write(data)
  file.close()
  pass

 
  
def RunInDb(c,sql):
  
  list_a = []
  # sql="SELECT * FROM ( SELECT A.*, ROWNUM RN FROM (SELECT * FROM WX_ZPXX_20181227) A WHERE ROWNUM <= 40 ) WHERE RN >= 21"
  print(sql)
  #获取cursor 
  x=c.execute(sql)

  #使用cursor进行各种操作
  list=x.fetchall()
  for item in list:
    hpzl = item[1]
    hphm = item[2]

    cjjg = item[6]
    cjjgmc = item[7]
    wfsj = item[8].strftime("%Y-%m-%d %H:%M:%S") 
    wfdd = item[9]
    wfxw = item[10]
    id = item[11]
    # print(item)

    photo1_data = item[3].read()

    if len(photo1_data) > 0:
      photo1_url = "/violation/20190312/"  + str(item[0])+'_1.jpg'
      photo1_path = down_path  + photo1_url
      write_file(photo1_data, photo1_path)
    else:
      photo1_url=''

    photo2_data = item[4].read()

    if len(photo2_data) > 0:
      photo2_url =  "/violation/20190312/"  +str(item[0])+'_2.jpg'
      
      photo2_path = down_path  + photo2_url
      write_file(photo2_data, photo2_path)
    else:
      photo2_url=''

    photo3_data = item[5].read()

    if len(photo3_data) > 0:
      
      photo3_url =  "/violation/20190312/"  +str(item[0])+'_3.jpg'
      photo3_path = down_path  + photo3_url
      write_file(photo3_data, photo3_path)
    else:
      photo3_url=''
 
    a = (id, '', hpzl, hphm, wfdd, wfsj, wfxw, cjjg, cjjgmc, 1, photo1_url, photo2_url, photo3_url,  "", "2019-03-12")
    # print(a)
    list_a.append(a)
  return list_a

c.close()
#关闭cursor
conn.close()
#关闭连接
