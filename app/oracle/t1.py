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

sql="SELECT count(*) FROM WX_ZPXX_20181227"
#获取cursor
x=c.execute(sql)
 

#使用cursor进行各种操作
list=x.fetchone()
  
print(list[0]) 
 

c.close()
#关闭cursor
conn.close()
#关闭连接
