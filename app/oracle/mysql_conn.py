
import pymysql

# 打开数据库连接
db = pymysql.connect("192.168.50.100","root","root","wf_yancheng" )
 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
 
# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS inputdata")
 
# 使用预处理语句创建表
sql = """CREATE TABLE `inputdata` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一识别号id',
  `sbbh` varchar(50) DEFAULT '' COMMENT '设备编号',  
  `hpzl` varchar(120) DEFAULT '' COMMENT '号牌种类',
  `hphm` varchar(200) DEFAULT '' COMMENT '号牌号码',  
  `wfdz` varchar(200) DEFAULT '' COMMENT '违法地址',
  `wfsj` datetime DEFAULT NULL COMMENT '违法时间', 
  `wfxw` varchar(32) NOT NULL DEFAULT '' COMMENT '违法行为', 
  `cjjg` varchar(32) NOT NULL DEFAULT '' COMMENT '', 
  `cjjgmc` varchar(32) NOT NULL DEFAULT '' COMMENT 'jiguanming', 
  `zpsl` int(6) NOT NULL DEFAULT '1' COMMENT '照片数量', 
  `zpstr1` varchar(255) DEFAULT NULL COMMENT '照片1',
  `zpstr2` varchar(255) DEFAULT NULL COMMENT '照片2',
  `zpstr3` varchar(255) DEFAULT NULL COMMENT '照片3',
  `zpstr4` varchar(255) DEFAULT NULL COMMENT '照片4',  
  `createtime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',   
  PRIMARY KEY (`id`) USING BTREE
) """
 
cursor.execute(sql)
 
# 关闭数据库连接
db.close()

