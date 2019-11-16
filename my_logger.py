# -*- coding: UTF-8 -*-

import time
import my_global as Global


class Logger(object):
    """ 日志类 """

    @classmethod
    def _get_time(cls):
        ct = time.time()
        return '%s.%03d' % (time.strftime("%Y-%m-%d %H:%M:%S",
                                          time.localtime()),
                            (ct - int(ct)) * 1000)

    @classmethod
    def _write_append(cls, infos):
        try:
            with open(Global.G_LOG_PATH, 'a+') as f:
                f.write(infos + '\n')
        except:
            pass

    @classmethod
    def info(cls, info):
        cls._write_append('[INFO ] %s: %s ' % (cls._get_time(), info))

    @classmethod
    def warn(cls, info):
        cls._write_append('[WARN ] %s: %s' % (cls._get_time(), info))

    @classmethod
    def error(cls, info):
        cls._write_append('[ERROR] %s: %s' % (cls._get_time(), info))

    @classmethod
    def debug(cls, info):
        if Global.G_LOG_LEVEL != 'debug':
            return
        cls._write_append('[DEBUG] %s: %s' % (cls._get_time(), info))


