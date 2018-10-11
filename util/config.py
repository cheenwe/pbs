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

    #proxy ip config
    @LazyProperty
    def proxy_local(self):
        return self.config_file.get('proxy','local')
 
    @LazyProperty
    def proxy_online(self):
        return self.config_file.get('proxy', 'online')

    #shijijiayuan ip config
    @LazyProperty
    def user_img_url(self):
        return self.config_file.get('shijijiayuan','img_url')
 
    @LazyProperty
    def user_login_url(self):
        return self.config_file.get('shijijiayuan', 'login_url')

    @LazyProperty
    def user_name(self):
        return self.config_file.get('shijijiayuan', 'name')

    @LazyProperty
    def user_password(self):
        return self.config_file.get('shijijiayuan', 'password')

    @LazyProperty
    def user_start_id(self):
        return self.config_file.get('shijijiayuan', 'start_id')

    @LazyProperty
    def user_end_id(self):
        return self.config_file.get('shijijiayuan', 'end_id')
        
    @LazyProperty
    def open_download(self):
        return self.config_file.get('shijijiayuan', 'open_download')

    @LazyProperty
    def open_save_online(self):
        return self.config_file.get('shijijiayuan', 'open_save_online')


if __name__ == '__main__':
    configs = GetConfig()
    print(configs.db_type)
    print(configs.db_name)
    print(configs.db_host)
    print(configs.db_port)
    print(configs.proxy_getter_functions)
    print(configs.host_ip)
    print(configs.host_port)
    