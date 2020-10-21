# -*- coding: UTF-8 -*-
"""
ViewModel板块，用于View和Model之间数据交互
"""
from my_model import Cache, Settings


class ViewModel:
    """ ViewModel """
    _cache_map = {}
    _cache = None
    _setting = None
    _ModelMap = {"SCREEN_SIZE_LIST": "screen_size_list",
                 "CONF_IMAGE_DICT": "conf_image_dict",
                 "LOGON_SSH_DICT": "logon_ssh_dict",
                 "SUBLOGIN_INDEX_LIST": "sublogin_index_list",
                 "GET_INFOWIN_EVT_FLAG": "get_infowin_flag",
                 "SET_INFOWIN_EVT_FLAG": "set_infowin_flag",
                 "TREE_VIEW_DATA_LIST": "treeview_data_list",
                 "SERVER_CACHE_DICT": "server_cache_dict"}

    @classmethod
    def init(cls, settingmap):
        cls._cache = Cache()
        cls._setting = Settings()
        return cls._setting.init(settingmap)

    @classmethod
    def cache(cls, message, type=None, data=None):
        """
        数据操作；
        根据消息字串映射成具体的model函数名
        """
        if message not in cls._ModelMap:
            return None
        func_str = "cls._cache.%s" % cls._ModelMap[message]
        func = eval(func_str)

        if type == 'ADD':
            if isinstance(func, list):
                func.append(data)
            elif isinstance(func, dict):
                func.update(data)
        elif type == 'SUB':
            try:
                if isinstance(func, list):
                    func.remove(data)
                elif isinstance(func, dict):
                    func.pop(data)
            except:
                pass
        elif type == 'QUE':
            return func
        elif type == 'DEL':
            func.clear()
        else:
            return func(data)

