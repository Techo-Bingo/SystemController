# -*- coding: UTF-8 -*-

from collections import defaultdict

class _ActiveDataBinder(object):

    def __init__(self):
        self.providers = {}

    def bind(self, provider, topic):
        self.providers[provider] = topic

    def unbind(self, provider):
        if provider in self.providers:
            del self.providers[provider]

    def notify(self, provider):
        if provider in self.providers:
            _passive_data_binder.notify(self.providers[provider], provider.data)

class _PassiveDataBinder(object):

    def __init__(self):
        self.topics = defaultdict(set)

    def bind(self, topic, handler):
        self.topics[topic].add(handler)

    def unbind(self, topic, handler):
        try:
            self.topics[topic].remove(handler)
        except:
            pass

    def notify(self, topic, data):
        for handler in self.topics[topic]:
            handler(data)

class _QueryDataBinder(object):

    def __init__(self):
        self.topics = {}

    def bind(self, topic, handler):
        self.topics[topic] = handler

    def unbind(self, topic):
        if topic in self.topics:
            del self.topics[topic]

    def query(self, topic, args=None):
        if topic in self.topics:
            handler = self.topics[topic]
            return handler(args)


_active_data_binder = _ActiveDataBinder()
_passive_data_binder = _PassiveDataBinder()
_query_data_binder = _QueryDataBinder()

def get_active_data_binder():
    return _active_data_binder


def get_passive_data_binder():
    return _passive_data_binder


def get_query_data_binder():
    return _query_data_binder

