# -*- coding: utf-8 -*-
# python  with oracle
# https://github.com/oracle/odpi

from conn import RunInDb
from mysql_insert import InsertMysql

import cx_Oracle
#引用模块cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
 
# 每次处理的条数
page_size = 5000

db_user ="trff_zjk"
db_passwd ="trff_zjk"
db_host ="192.168.50.10:1521"

# 数据库表名
table_name = 'WX_ZPXX_20181227'

# 数据库链接信息
conn_info = db_user+"/"+ db_passwd +"@"+ db_host +"/orcl"
conn=cx_Oracle.connect(conn_info)

#连接数据库
c=conn.cursor()


count_sql="SELECT count(*) FROM " + table_name
#获取cursor
x=c.execute(count_sql)
 
#使用cursor进行各种操作
res=x.fetchone()
  
print("total: ", res[0]) 
# 总条数
all_count = res[0]

# sql="SELECT * FROM ( SELECT A.*, ROWNUM RN FROM (SELECT * FROM WX_ZPXX_20181227) A WHERE ROWNUM <= 5001 ) WHERE RN >= 1"
total_page = int(all_count/page_size)

def sql_info(start_no, end_no=0):
    if end_no == 0:
        end_no = str(int(start_no) + page_size-1)
    else:
        str(end_no)
    return "SELECT * FROM ( SELECT A.*, ROWNUM RN FROM (SELECT * FROM "+ table_name +") A WHERE ROWNUM <= "+ end_no +" ) WHERE RN >= "+ start_no


for i in range(1,total_page+1):
    start_no = str((i-1)*page_size+1)
    end_no = str(i*page_size)
    sql = sql_info(start_no)
    # sql="SELECT * FROM ( SELECT A.*, ROWNUM RN FROM (SELECT * FROM "+ table_name +") A WHERE ROWNUM <= "+ end_no +" ) WHERE RN >= "+start_no
    # print(sql)
    a = RunInDb(c,sql)
    # print(a)
    InsertMysql(a)


last_page = total_page*page_size

start_no = str(last_page+1)
end_no = str(all_count)
sql = sql_info(start_no,end_no)

RunInDb(c,sql)
# sql="SELECT * FROM ( SELECT A.*, ROWNUM RN FROM (SELECT * FROM "+ table_name +") A WHERE ROWNUM <= "+ end_no +" ) WHERE RN >= "+start_no
# print(sql)



c.close()
#关闭cursor
conn.close()
#关闭连接
