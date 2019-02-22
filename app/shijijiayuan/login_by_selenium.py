# -*- coding: utf-8 -*-
# 调用浏览器自动登录获取Cookie
import requests,json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#当前文件的路径
pwd = os.getcwd()
project_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
sys.path.append(project_path)

# from login import GetUserCookie
# from proxy.proxy_valid import ValidIp
# from api.rest_api import RestApi
# from util.util_function import CheckDir, DownloadFile, WriteInfo
# from util.log_handler import LogHandler
from util.config import GetConfig

configs = GetConfig()
proxy = "121.61.2.252:9999"
ops = Options()
# ops.add_argument('--headless')
# ops.add_argument('--no-sandbox')
# ops.add_argument('--disable-dev-shm-usage')
# ops.add_argument('--disable-gpu')
print('--proxy-server=http://%s' % proxy)
# ops.add_argument('--user-agent=%s' % ua)
# ops.add_argument('--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data')
ops.add_argument('--proxy-server=http://%s' % proxy)
driver = webdriver.Chrome( chrome_options=ops)

driver.delete_all_cookies()

# driver.maximize_window()

login_url="http://login.jiayuan.com/"

driver.get(login_url)

driver.find_element_by_id("login_email").send_keys(str(configs.user_name))
driver.find_element_by_id("login_password").send_keys(str(configs.user_password))
driver.find_element_by_id("login_btn").click()

# 获取cookie信息
cookies = driver.get_cookies()

jsonCookies = json.dumps(cookies)
with open('/tmp/jiayuan.json', 'w') as f:
    f.write(jsonCookies)

with open('/tmp/jiayuan.json','r',encoding='utf-8') as f:
    listCookies=json.loads(f.read())
cookie = [item["name"] + "=" + item["value"] for item in listCookies]
cookiestr = '; '.join(item for item in cookie)
print(cookiestr)


driver.quit()