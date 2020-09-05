# -*- coding: UTF-8 -*-

import os
import re
import time
import shutil
import zipfile
import threading
from json import loads
from collections import OrderedDict
from my_base import JSONError


class JSONParser:
    """ JSON解析器 """

    @classmethod
    def parser(cls, json_path):
        try:
            with open(json_path, 'r', encoding='UTF-8') as f:
                return loads(f.read(), object_pairs_hook=OrderedDict)
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
    def rm_dir(cls, path):
        return shutil.rmtree(path)

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
    def zip_dir(cls, dirname, zipname):
        filelist = []
        if os.path.isfile(dirname):
            filelist.append(dirname)
        else:
            for root, dirs, files in os.walk(dirname):
                for name in files:
                    filelist.append(os.path.join(root, name))
        zf = zipfile.ZipFile(zipname, "w", zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(dirname):]
            zf.write(tar, arcname)
        zf.close()

