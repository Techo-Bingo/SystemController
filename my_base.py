# -*- coding: UTF-8 -*-
import tkinter as tk


class FileError(Exception):
    """ 文件异常 """
    pass


class JSONError(Exception):
    """ JSON解析异常 """
    pass


class SSHError(Exception):
    """ SSH登录失败异常 """
    pass


class ExecError(Exception):
    """ SSH 执行失败异常 """
    pass


class InputError(Exception):
    """ 用户输入错误异常 """
    pass


class ReportError(Exception):
    """ 脚本进度失败异常 """
    pass


class Singleton(object):
    """ 使用__new__实现抽象单例 """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class GuiBase(Singleton):
    """ 子窗体的基类 """
    master = None

    def init_windows(self):
        pass

    def destroy(self):
        self.master.destroy()

    def show(self):
        self.init_windows()


class Pager(object):
    interface = None
    master = None
    title = None
    width = None
    height = None
    frame = None
    ip_choose = False
    _showing = False

    def _init(self):
        self._showing = True
        self.frame = tk.LabelFrame(self.master, text=self.title, width=self.width, height=self.height)
        self.frame.pack(fill='both')
        self.frame.pack_propagate(0)

    def pack(self):
        self._init()
        self.pack_frame()

    def pack_frame(self):
        pass

    def alive(self):
        return self._showing

    def destroy_frame(self):
        pass

    def destroy(self):
        self._showing = False
        try:
            self.destroy_frame()
            self.frame.destroy()
        except:
            pass

