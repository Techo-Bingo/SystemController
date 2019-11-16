# -*- coding: UTF-8 -*-

import os
import re
import time
import threading
from json import load
from my_base import JSONError


class JSONParser:
    """ JSON解析器 """

    @classmethod
    def parser(cls, json_path):
        try:
            with open(json_path, 'r', encoding='UTF-8') as f:
                return load(f)
        except Exception as e:
            raise JSONError(e)


class Common:
    """ 第三方公共方法 """

    @classmethod
    def is_exists(cls, dir):
        return os.path.exists(dir)

    @classmethod
    def is_file(cls, file_path):
        return os.path.isfile(file_path)

    @classmethod
    def remove(cls, file_path):
        return os.remove(file_path)

    @classmethod
    def mkdir(cls, dir):
        try:
            os.makedirs(dir)
        except FileExistsError:
            pass

    @classmethod
    def basename(cls, file_path):
        return os.path.split(file_path)[1]

    @classmethod
    def file_size(cls, file_path):
        if not cls.is_file(file_path):
            return 0
        return os.path.getsize(file_path)

    @classmethod
    def get_time(cls):
        ct = time.time()
        return '%s.%03d' % (time.strftime("%Y-%m-%d %H:%M:%S",
                                          time.localtime()),
                            (ct - int(ct)) * 1000)

    @classmethod
    def write_to_file(cls, filename, info):
        try:
            with open(filename, 'w') as f:
                f.write(info)
                return True
        except:
            return False

    @classmethod
    def create_thread(cls, func, args=()):
        th = threading.Thread(target=func, args=args)
        th.setDaemon(True)
        th.start()

    @classmethod
    def is_ip(cls, ip):
        p = re.compile("^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
                       "(25[0-5]|2[0-4]\d|[01]?\d\d?)$")
        return p.match(ip)

    @classmethod
    def sleep(cls, sec):
        time.sleep(sec)

    @classmethod
    def find_val_in_str(cls, in_str, key):
        return re.findall(r'%s:.*' % (key), in_str)[0].split(':')[-1]

