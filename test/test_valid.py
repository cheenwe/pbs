#coding=utf-8
# 测试多次验证
import requests

max = 6

# 验证代理IP能否正常访问host
def vaildProxy(valid_host, proxy):
    proxies = {"http": "http://{proxy}".format(proxy=proxy)}
    print(proxies)
    try:
        r = requests.get(valid_host, proxies=proxies, timeout=1, verify=False)
        if r.status_code == 200:
            return True
        else:
            return False
    except Exception:
        return False

def getHtml():
    retry_count = 4
    # proxy = get_proxy()
    while retry_count > 0:
        v_res = vaildProxy("http://www.baidu.com", "117.127.0.202:8080")
        if v_res:
            print(retry_count)
            print("success!")
            return 0
        else:
            print(retry_count)
            print("contine!")
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    return None

# print(vaildProxy("http://www.baidu.com", "117.127.16.208:8080"))
getHtml()