# -*- coding: UTF-8 -*-

from Binder.sc_proxy import get_active_data_binder
from Utils.sc_func import Common

class DataTemplate(object):
    _data = None

    def init(self, d):
        self._data = d

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, d):
        self._data = d
        get_active_data_binder().notify(self)

class DataCreater(object):

    def __init__(self, data_template):
        self._instance = data_template()

    def get_provider(self):
        return self._instance

    def set_data(self, data, asynccall=False):
        def func(args=None):
            self._instance.data = data
        if asynccall:
            Common.create_thread(func=func)
        else:
            func()

    def get_data(self):
        """ 返回数据副本, 避免原数据被修改的可能
        注意, 使用copy.deepcopy()深拷贝会有问题
        """
        real = self._instance.data
        if isinstance(real, dict):
            new = {}
            new.update(real)
        elif isinstance(real, list):
            new = []
            new = new + real
        else:
            new = real
        return new
