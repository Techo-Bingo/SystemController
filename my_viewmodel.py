# -*- coding: UTF-8 -*-
"""
ViewModel板块，用于View和Model之间数据交互
"""
from my_model import Cache, Settings


class ViewModel:
    """ ViewModel """
    _cache_map = {}
    _setting_map = {}
    _cache = None
    _setting = None

    @classmethod
    def init(cls, modelmap, settingmap):
        cls._cache_map = modelmap['Cache']
        cls._setting_map = modelmap['Setting']
        cls._cache = Cache()
        cls._setting = Settings()
        return cls._setting.init(settingmap)

    @classmethod
    def cache(cls, message, type=None, data=None):
        """
        数据操作；
        根据消息字串映射成具体的model函数名
        """
        if message not in cls._cache_map:
            return None
        func_str = "cls._cache.%s" % cls._cache_map[message]
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

    @classmethod
    def setting(cls, message, type=None, data=None):
        func_str = "cls._setting.%s" % cls._setting_map[message]
        func = eval(func_str)

        if type == 'QUE':
            return func

