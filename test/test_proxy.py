import sys
import logging
import requests

sys.path.append('..')

from proxy.proxy import *

# noinspection PyPep8Naming
def test_1():
    """
    test function LogHandler  in Util/LogHandler
    :return:
    """
    # mm=GetLocalIp()
    # print(mm)
    ValidIp()
    # mm=ValidIp("local",'http://www.jiayuan.com' )
    # print(mm)
def test_2():
    proxies = {'http': 'http://120.198.76.45:52798'}
    url = 'http://www.baidu.com'
    req = requests.get(url,  proxies=proxies, timeout=10, verify=False)

if __name__ == '__main__':
    test_1()
