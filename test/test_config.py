# -*- coding: utf-8 -*-
import sys

sys.path.append('..')

from util.config import GetConfig


# noinspection PyPep8Naming
def testGetConfig():
    """
    test class GetConfig in Util/GetConfig
    :return:
    """
    configs = GetConfig()
    # print(configs.host_ip)
    # print(configs.proxy_local)
    
    # print(configs.proxy_online)
    # print(configs.user_img_url)
    # print(configs.user_login_url)
    print(configs.user_start_id)

    # assert isinstance(configs.proxy_getter_functions, list)
    # print(configs.proxy_getter_functions)

if __name__ == '__main__':
    testGetConfig()
