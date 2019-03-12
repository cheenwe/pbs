
import pymysql


def WriteInfo(folder_name, data):
    with open(folder_name, 'a+') as f:
        writer = f.write(data)



def InsertMysql(sql):
   
    # print(sql)
    # 打开数据库连接
    db = pymysql.connect("192.168.50.100","root","root","wf_yancheng" )
    
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    data = list(map(tuple, sql))

    print(">>>>>>>>>>>>>>>>>>>>>")
    print(data)

    print(">>>>>>>>>>>>>>>>>>>>>")
    # SQL 插入语句
    # sql =  "INSERT INTO inputdata VALUE" + sql.tolist()

    sql_inert =  "INSERT INTO inputdata(id) VALUE (%s)"  
    list = []
    for i in range(0, len(sql)): 
        # list.append((sql[i][0], sql[i][1], sql[i][2], sql[i][3], sql[i][4], sql[i][5], sql[i][6], sql[i][7], sql[i][8], sql[i][9], sql[i][10], sql[i][11], sql[i][12], sql[i][13], sql[i][14]))
        list.append((sql[i][0], sql[i][1] ) )


    # print(sql)

    try:
        # 执行sql语句
        cursor.executemany("INSERT INTO inputdata(id, sbbh)  VALUE %s",  list)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()   
    
    cursor.execute(sql)
    
    # 关闭数据库连接
    db.close()


# def InsertMysql(sql):
#     folder_name = './inputdata.sql'

#     # sql_inert =  "INSERT INTO inputdata(id) VALUE (%s)"  
#     WriteInfo(folder_name, str(sql))



