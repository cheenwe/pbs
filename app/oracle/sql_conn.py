# -*- coding: utf-8 -*-
# python  with oracle
# https://github.com/oracle/odpi


import cx_Oracle
#引用模块cx_Oracle
import os

def conn_sql():

    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

    db_user ="trff_zjk"
    db_passwd ="trff_zjk"
    db_host ="192.168.50.10:1521"

    # 数据库表名
    table_name = 'WX_ZPXX_20181227_02'

    # 数据库链接信息
    conn_info = db_user+"/"+ db_passwd +"@"+ db_host +"/orcl"
    conn=cx_Oracle.connect(conn_info)

    #连接数据库
    c=conn.cursor()
    return c


