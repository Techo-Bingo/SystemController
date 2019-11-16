# -*- coding: UTF-8 -*-
"""
Model板块，定义数据模型
"""
import my_global as Global
from my_base import Singleton


class Settings(Singleton):
    """ 用户设置类 """

    def __init__(self):
        self._default_passwd = None

    def init(self, maps):
        try:
            Global.G_LOG_LEVEL = maps['loglevel']
            _default = maps['defaults']
            self._default_passwd = [_default['username'],
                                    _default['userpassword'],
                                    _default['rootpassword']
                                    ]
            Global.G_RETRY_TIMES = maps['retry_times']
            return True
        except:
            return False

    @property
    def default_passwd(self):
        return self._default_passwd


class Cache(Singleton):
    """ 数据处理类 """

    def __init__(self):
        self._screen_size = []
        self._infowin_flag = False
        self._sublogin_index = []
        self._logon_ssh = {}
        self._conf_image = {}

    @property
    def screen_size_list(self):
        return self._screen_size

    @property
    def logon_ssh_dict(self):
        return self._logon_ssh

    @property
    def conf_image_dict(self):
        return self._conf_image

    @property
    def sublogin_index_list(self):
        return self._sublogin_index

    def get_infowin_flag(self, data=None):
        return self._infowin_flag

    def set_infowin_flag(self, data=None):
        self._infowin_flag = True

