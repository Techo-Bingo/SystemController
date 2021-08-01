# -*- coding: UTF-8 -*-

import time
from Model.sc_global import Global
from Utils.sc_func import Common

class Logger(object):

    def __init__(self):
        self.level_map = {'debug': 0, 'info': 1, 'warn': 2, 'error': 3}
        self.log_path = Global.G_LOG_PATH
        self.log_level = 'info'

    def change_level(self, level):
        if level not in self.level_map:
            return
        self.log_level = level

    def _get_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def _write_append(self, info):
        try:
            with open(self.log_path, 'a+') as f:
                f.write(info + '\n')
        except:
            pass

    def truncate(self, data=None):
        self.info('Bye...')
        Common.remove('{}.1'.format(self.log_path))
        Common.rename(self.log_path, '{}.1'.format(self.log_path))

    def info(self, info):
        if self.level_map[self.log_level] > self.level_map['info']:
            return
        self._write_append('[INFO ] %s: %s ' % (self._get_time(), info))

    def warn(self, info):
        if self.level_map[self.log_level] > self.level_map['warn']:
            return
        self._write_append('[WARN ] %s: %s' % (self._get_time(), info))

    def error(self, info):
        self._write_append('[ERROR] %s: %s' % (self._get_time(), info))

    def debug(self, info):
        if self.log_level != 'debug':
            return
        self._write_append('[DEBUG] %s: %s' % (self._get_time(), info))


logger = Logger()
