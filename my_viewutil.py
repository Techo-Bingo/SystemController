# -*- coding: UTF-8 -*-
"""
View板块相关公共子模块;
提供接口，不参与处理逻辑
"""
import time
import my_global as Global
from tkinter import messagebox
from my_common import Common
from my_bond import Caller
from my_viewmodel import ViewModel


class WinMsg:
    """ windows提示窗 """

    @classmethod
    def info(cls, info):
        messagebox.showinfo('提示', info)

    @classmethod
    def error(cls, info):
        messagebox.showerror('错误', info)

    @classmethod
    def ask(cls, info):
        return messagebox.askokcancel('请确认', info)

    @classmethod
    def warn(cls, info):
        messagebox.showwarning('警告', info)


class ToolTips:

    @classmethod
    def message_tips(cls, info, level='INFO'):
        Caller.call(Global.EVT_INSERT_INFOWIN_TEXT, (info, level))

    @classmethod
    def widget_tips(cls, widget, region='background', back=Global.G_DEFAULT_COLOR):
        Common.create_thread(cls._change_color, args=(widget, region, back))

    @classmethod
    def _change_color(cls, widget, region, back):
        sleep = 0.3
        widget[region] = 'red'
        time.sleep(sleep)
        widget[region] = 'Gold'
        time.sleep(sleep)
        widget[region] = 'red'
        time.sleep(sleep)
        widget[region] = 'Gold'
        time.sleep(sleep)
        widget[region] = 'red'
        time.sleep(sleep)
        widget[region] = 'Gold'
        time.sleep(sleep)
        widget[region] = back


class ViewUtil:
    """
    view板块数据获取接口
    函数名要求：<动词>_<宾语>
    """
    _root = None
    _X = 0
    _Y = 0

    @classmethod
    def init_root(cls, root_gui):
        cls._root = root_gui
        ViewModel.cache('SCREEN_SIZE_LIST', type='ADD', data=root_gui.maxsize())

    @classmethod
    def close_root(cls):
        cls._root.close()

    @classmethod
    def calculate_size(cls):
        gui = cls._root
        gui.resizable(True, True)
        gui.state('zoomed')
        gui.update()
        screen_str = gui.winfo_geometry()
        gui.state('normal')
        w, h = screen_str.split('+')[0].split('x')
        x, y = screen_str.split('+')[1:]
        w, h = int(w), int(h)
        cls._X = 10 if int(x) < 0 else int(x) + 10
        cls._Y = 10 if int(y) < 0 else int(y) + 10
        Global.G_MAIN_WIN_WIDTH = w
        Global.G_MAIN_WIN_HEIGHT = h
        if w >= 1600:
            Global.G_MAIN_WIN_WIDTH = 1500
        elif 1360 <= w < 1600:
            Global.G_MAIN_WIN_WIDTH = 1200
        if h >= 1000:
            Global.G_MAIN_WIN_HEIGHT = 900
        elif 760 <= h < 1000:
            Global.G_MAIN_WIN_HEIGHT = 700

    @classmethod
    def get_screensize(cls):
        return ViewModel.cache('SCREEN_SIZE_LIST', type='QUE')[-1]

    @classmethod
    def reposition(cls, width, height):
        cls._root.geometry("{}x{}+{}+{}".format(width, height, cls._X, cls._Y))
        cls._root.resizable(False, False)

    @classmethod
    def set_widget_size(cls, widget=None, width=None, height=None, center=True):
        if not widget:
            widget = cls._root
        s_width, s_height = ViewModel.cache('SCREEN_SIZE_LIST', type='QUE')[-1]
        try:
            if not width:
                width = widget.width
            if not height:
                height = widget.height
            # 太大可能是多屏，中间显示效果不好，只在单屏上显示
            if s_width > 3000:
                s_width = s_width // 2
            if center:
                widget.geometry('%sx%s+%s+%s' % (width, height, (s_width-width)//2, (s_height-height)//2))
            else:
                widget.geometry('%sx%s' % (width, height))
        except:
            pass

    @classmethod
    def get_image(cls, name):
        images = ViewModel.cache('CONF_IMAGE_DICT', type='QUE')
        if name not in images:
            return None
        return images[name]

    @classmethod
    def add_sublogin(cls):
        _sublogin_index = ViewModel.cache('SUBLOGIN_INDEX_LIST', type='QUE')
        _sublogin_count = len(_sublogin_index)
        if _sublogin_count >= Global.G_LGN_COUNT_LIMIT:
            return False, Global.G_LGN_COUNT_LIMIT
        _new_index = 1
        if _sublogin_count:
            _new_index = _sublogin_index[-1] + 1

        ViewModel.cache('SUBLOGIN_INDEX_LIST', type='ADD', data=_new_index)
        return True, _new_index

    @classmethod
    def del_sublogin(cls, index):
        ViewModel.cache('SUBLOGIN_INDEX_LIST', type='SUB', data=index)

    @classmethod
    def set_infowin_flag(cls):
        ViewModel.cache('SET_INFOWIN_EVT_FLAG')

    @classmethod
    def get_ssh_ip_list(cls):
        return list(ViewModel.cache('LOGON_SSH_DICT', type='QUE').keys())

    @classmethod
    def get_treeview_data(cls):
        return ViewModel.cache('TREE_VIEW_DATA_LIST', type='QUE')[-1]
