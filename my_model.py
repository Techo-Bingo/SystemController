# -*- coding: UTF-8 -*-
"""
Model板块，定义数据模型
"""
import my_global as Global
from my_base import Singleton


class Settings(Singleton):
    """ 用户设置类 """

    def __init__(self):
        pass

    def init(self, setting_map):
        try:
            Global.G_TOOL_NAMED = setting_map['tool_named']
            Global.G_VERSION = setting_map['tool_version']
            Global.G_LOG_LEVEL = setting_map['log_level']
            Global.G_LOG_SIZE = setting_map['log_size']
            Global.G_RETRY_TIMES = setting_map['retry_times']
            Global.G_PACKAGE_NAME = setting_map['package_name']
            _default = setting_map['passwords']
            Global.G_DEFAULT_PASSWORDS = [_default['username'],
                                          _default['userpassword'],
                                          _default['rootpassword']]
            Global.reload()
            return True
        except:
            return False


class Cache(Singleton):
    """ 数据处理类 """

    def __init__(self):
        self._screen_size = []
        self._infowin_flag = False
        self._sublogin_index = []
        self._logon_ssh = {}
        self._conf_image = {}
        self._treeview_data = []

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

    @property
    def treeview_data_list(self):
        return self._treeview_data

