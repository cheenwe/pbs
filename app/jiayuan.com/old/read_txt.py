
# coding=utf-8

import csv
import os, sys,time, json
#当前文件的路径
pwd = os.getcwd()
project_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
sys.path.append(project_path)
from util.util_function import CheckDir, DownloadFile, WriteInfo


#输出文件夹
out_dir = './photo_new'
# print(project_path)

def download_file(url, folder_name,  id):

    new_url = url.split("_thumbnail")[0]+".png"
    file_name = str(id) + ".png"
    DownloadFile(new_url, folder_name, file_name)


csv_path = "/home/chenwei/文档/1031-徐汇滨江.txt"
print(csv_path)
csv_file = csv.reader(open(csv_path,'r'))

i = 0
for line in csv_file: 
    # print(line)

    folder_name = out_dir + "/" + str(i) + "/"
    CheckDir(folder_name)
    file_name = str(i) + ".png" 

    download_file(line[0], folder_name,  "1")
    download_file(line[1], folder_name,  "2")

    print(i)

    i = i+1