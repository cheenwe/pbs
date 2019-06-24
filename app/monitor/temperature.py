# coding=utf-8
# 检测 cpu 温度 temperature
# sudo apt  install lm-sensors #cpu
# 使用 nvidia-smi  命令获取温度,计算平均值 #cpu
# install :
# sudo apt  install lm-sensors && pip3 install requests

import  os
import  requests

current_ip="192.168.30.31"

host_ip="192.168.50.69:3000/"

host = 'http://'+ str(host_ip)

def send_monitor_data(ip, data):
    d = {'ip': ip, 'data': data}
    print(d)
    r = requests.post(host + 'api/v1/monitor', data=d)

def send_data(data):
    print(data)
    try:
        send_monitor_data(current_ip, data)
    except Exception as e:
        print("api request fail: %s", format(e)) # 接口请求失败

def dete_cpu_temperature():
    output = os.popen("printf '%d' $(sensors | grep 'id 0:' | awk '{ print $4 }') ")
    tmp = output.read()
    return  "cpu:"+str(tmp)

def dete_gpu_temperature():
    output = os.popen("nvidia-smi -q | grep 'GPU Current Temp' |cut -d ' ' -f 24 | awk '{print $1}' | awk '{sum+=$1}END{print sum}'|awk '{print $1/8}'")
    tmp = output.read()
    return "gpu:"+str(tmp)

list =""
list = list + dete_cpu_temperature()+";"
list = list + dete_gpu_temperature()

send_data(list)

