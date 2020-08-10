# -*- coding: UTF-8 -*-
import tkinter as tk


class EnvError(Exception):
    """ 环境异常 """
    pass


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

    def init_viewmodel(self):
        pass

    def init_frame(self):
        pass

    def pack_frame(self):
        pass

    def destroy(self):
        self.master.destroy()

    def show(self):
        self.init_viewmodel()
        self.init_frame()
        self.pack_frame()


class Pager(object):
    interface = None
    master = None
    width = None
    height = None
    frame = None
    _showing = False

    #def __new__(cls, *args, **kwargs):
    #    if not hasattr(cls, '_instance'):
    #        cls._instance = super(Pager, cls).__new__(cls)
    #    return cls._instance

    def _init(self):
        self._showing = True
        self.frame = tk.LabelFrame(self.master, width=self.width, height=self.height)
        self.frame.pack()
        self.frame.pack_propagate(0)

    def pack(self):
        self._init()
        self.stepper()

    def stepper(self):
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

