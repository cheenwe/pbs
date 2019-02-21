# coding=utf-8
import requests
import time, sys, os

#当前文件的路径
pwd = os.getcwd()
project_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
sys.path.append(project_path)

from proxy.proxy_valid import ValidIp

from util.config import GetConfig

configs = GetConfig()

# print(configs.user_img_url)
# print(configs.user_login_url)
# print(configs.user_name)
# print(configs.user_password)

# res = ValidIp('1','https://www.jiayuan.com' )
#获取ip

proxies = ValidIp(True,'http://www.jiayuan.com' )

# proxies = ValidIp('1' , 'http://www.jiayuan.com' )

def GetUserCookie():
  img_url=str(configs.user_img_url) #'https://www.jiayuan.com/18126809'
  s=requests.session()
  # print(s.cookies.get_dict())#先打印一下，此时一般应该是空的。

  # res=s.get(img_url, stream=True)
  res=s.get(img_url,proxies=proxies[0], stream=True)


  login_url=str(configs.user_login_url) #'httpss://passport.jiayuan.com/dologin.php?host=www.jiayuan.com&pre_url='
  data= {
    'name':str(configs.user_name),
    'password':str(configs.user_password),
    'remem_pass':'on',
    'ajaxsubmit':1,
    'ljg_login':1,
  }

  rs=s.post(login_url,data)
  c=requests.cookies.RequestsCookieJar()#利用RequestsCookieJar获取
  # c.set('cookie-name','cookie-value')
  s.cookies.update(c)
  return s.cookies.get_dict()

print(GetUserCookie())