# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
from util.util_class import ConfigParse
from util.util_class import LazyProperty


class GetConfig(object):
    """
    to get config from config.ini
    """

    def __init__(self):
        self.pwd = os.path.split(os.path.realpath(__file__))[0]
        self.config_path = os.path.join(os.path.split(self.pwd)[0], 'config.ini')
        self.config_file = ConfigParse()
        self.config_file.read(self.config_path)

    @LazyProperty
    def db_adapter(self):
        return self.config_file.get('DB', 'adapter')

    @LazyProperty
    def db_encoding(self):
        return self.config_file.get('DB', 'encoding')

    @LazyProperty
    def db_database(self):
        return self.config_file.get('DB', 'database')

    @LazyProperty
    def db_pool(self):
        return self.config_file.get('DB', 'pool')

    @LazyProperty
    def db_username(self):
        return self.config_file.get('DB', 'username')

    @LazyProperty
    def db_password(self):
        return self.config_file.get('DB', 'password')

    #Host config

    @LazyProperty
    def host_ip(self):
        return self.config_file.get('HOST','ip')

    @LazyProperty
    def host_port(self):
        return int(self.config_file.get('HOST', 'port'))

if __name__ == '__main__':
    gg = GetConfig()
    print(gg.db_type)
    print(gg.db_name)
    print(gg.db_host)
    print(gg.db_port)
    print(gg.proxy_getter_functions)
    print(gg.host_ip)
    print(gg.host_port)
