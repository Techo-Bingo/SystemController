# -*- coding: UTF-8 -*-

import os
import re
import time
import json
import shutil
import zipfile
import threading
from collections import OrderedDict

class Singleton(object):
    """ 使用__new__实现抽象单例 """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

class JSONParser:
    """ JSON解析器 """
    @classmethod
    def parser(cls, json_path):
        with open(json_path, 'r', encoding='UTF-8') as f:
            return json.loads(f.read(), object_pairs_hook=OrderedDict)

    @classmethod
    def write(cls, json_path, data):
        with open(json_path, 'w', encoding='UTF-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

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
        try:
            shutil.rmtree(path)
        except:
            pass

    @classmethod
    def remove(cls, file_path):
        try:
            os.remove(file_path)
        except:
            pass

    @classmethod
    def rename(cls, old, new):
        try:
            os.rename(old, new)
        except:
            pass

    @classmethod
    def mkdir(cls, dir):
        try:
            os.makedirs(dir)
        except FileExistsError:
            pass

    @classmethod
    def system_open(cls, file):
        try:
            os.startfile(file)
        except:
            pass

    @classmethod
    def get_pid(cls):
        return os.getpid()

    @classmethod
    def basename(cls, file_path):
        return os.path.split(file_path)[1]

    @classmethod
    def file_size(cls, file_path):
        if not cls.is_file(file_path):
            return 0
        return os.path.getsize(file_path)

    @classmethod
    def get_time(cls, format=True):
        if format:
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return time.strftime("%Y%m%d%H%M%S", time.localtime())

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
        p = re.compile("^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$")
        return p.match(ip)

    @classmethod
    def sleep(cls, sec):
        time.sleep(sec)

    @classmethod
    def time(cls):
        return time.time()

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
    
    @classmethod
    def unzip_file(cls, file_path, path):
        if not zipfile.is_zipfile(file_path):
            return False
        with zipfile.ZipFile(file_path, 'r') as zip:
            zip.extractall(path)
        return True

    @classmethod
    def exist_suffix_file(cls, dirname, suffix):
        for file in os.listdir(dirname):
            f_split = os.path.splitext(file)
            if f_split[1] == suffix:
                return True, f_split[0]
        return False, None

class Timer(threading.Thread):
    """ 定时器 """
    def __init__(self, func, period=10, do_first=False, args=()):
        super(Timer, self).__init__()
        self.func = func
        self.do_first = do_first
        self.period = period
        self.args = args
        self.daemon = True
        self._pause_flag = threading.Event()
        self._run_flag = threading.Event()
        self._pause_flag.set()
        self._run_flag.set()

    def run(self):
        _run_flag = self._run_flag.isSet
        _pause_wait = self._pause_flag.wait
        _sleep = time.sleep

        while _run_flag():
            _pause_wait()
            if self.do_first:
                self.func(self.args)
                _sleep(self.period)
            else:
                _sleep(self.period)
                self.func(self.args)

    def pause(self):
        self._pause_flag.clear()

    def resume(self):
        self._pause_flag.set()

    def stop(self):
        self._pause_flag.set()
        self._run_flag.clear()

    def update_period(self, per):
        self.period = per
