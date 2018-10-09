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
    gg = GetConfig()
    print(gg.host_ip)

    # assert isinstance(gg.proxy_getter_functions, list)
    # print(gg.proxy_getter_functions)

if __name__ == '__main__':
    testGetConfig()
