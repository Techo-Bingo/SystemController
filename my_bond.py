# -*- coding: UTF-8 -*-
"""
ViewModel板块
使用发布者/订阅者设计模式实现View板块的回调
"""
from collections import defaultdict
from my_logger import Logger


class _MultiEvent:
    events = defaultdict(dict)

    @classmethod
    def deal(cls, event, msg):
        for name, callback in cls.events[event].items():
            # Logger.debug('{} callback _MultiEvent: {} {}'.format(
            #    name, event, callback))
            callback(msg)

    @classmethod
    def register(cls, event, handler):
        cls.events[event][handler.name] = handler.callback
        # Logger.debug('{} register _MultiEvent: {} with {}'.format(
        #    handler.name,event, handler.callback))
        # Logger.debug('ALL Evt: {}'.format(cls.events))

    @classmethod
    def unregister(cls, event, handler):
        try:
            Logger.debug('{} unregister _MultiEvent: {}'.format(
                handler.name, event))
            del cls.events[event][handler.name]
        except:
            pass


class _EventCaller:
    @classmethod
    def call(self, event, msg=None):
        _MultiEvent.deal(event, msg)


class _EventHandler(object):
    def __init__(self, name):
        self.name = name
        self.callback = None

    def register(self, event, callback):
        self.callback = callback
        _MultiEvent.register(event, self)

    def unregister(self, event):
        _MultiEvent.unregister(event, self)


class Bonder(object):
    """
    Bonder和Packer分别为事件的绑定（订阅）和布局（发布）
    Bonder和_EventHandler均不可为单例，否则去注册将会出问题（去注册了的不是自己的事件）
    """

    def __init__(self, name):
        self.handler = _EventHandler(name)

    def bond(self, event, callback):
        self.handler.register(event, callback)

    def unbond(self, event):
        self.handler.unregister(event)


class _SingleEvent:
    events = {}

    @classmethod
    def deal(cls, event, msg):
        callback = cls.events[event]
        # Logger.debug('{} callback _SingleEvent: {} {}'.format(
        #    name, event, callback))
        return callback(msg)

    @classmethod
    def define(cls, event, callback):
        cls.events[event] = callback
        # Logger.debug('{} define _SingleEvent: {} {}'.format(
        #    name, event, callback))

    @classmethod
    def undefine(cls, event):
        # Logger.debug('{} undefine _SingleEvent: {} '.format(
        #    name, event))
        try:
            del cls.events[event]
        except:
            pass


class Define(object):
    """ 定义事件 """

    @classmethod
    def define(cls, event, callback):
        _SingleEvent.define(event, callback)

    @classmethod
    def undefine(cls, event):
        _SingleEvent.undefine(event)


class Caller:
    """
    Caller注重事件处理 （一对一关系——一个调用、一个回调）
    一般只在handler中使用
    """
    @classmethod
    def call(cls, event, msg=None):
        return _SingleEvent.deal(event, msg)


"""
Packer注重布局变化 （一对多关系——一个调用、多个回调） 
只在View板块中使用
"""
Packer = _EventCaller


