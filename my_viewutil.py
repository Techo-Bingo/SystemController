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
        return messagebox.askokcancel('询问', info)

    @classmethod
    def warn(cls, info):
        messagebox.showwarning('警告', info)


class ToolTips:
    """
    提示类；
    改变控件颜色或infowin信息提示
    """
    @classmethod
    def inner_error(cls, info):
        """ Login窗体时不能使用 """
        cls._infowin_msg('(内部错误) %s' % info, 'ERROR')

    @classmethod
    def inner_warn(cls, info):
        cls._infowin_msg(info, 'WARN')

    @classmethod
    def widget_tips(cls,
                    widget,
                    region='background',
                    back=Global.G_DEFAULT_COLOR):
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

    @classmethod
    def _infowin_msg(cls, info, level='INFO'):
        Caller.call(Global.EVT_INSERT_INFOWIN_TEXT, (info, level))


class ViewUtil:
    """
    view板块数据获取接口
    函数名要求：<动词>_xx
    """

    @classmethod
    def set_maxsize(cls, size_tuple):
        ViewModel.cache('SCREEN_SIZE_LIST', type='ADD', data=size_tuple)

    @classmethod
    def set_centered(cls, widget, width=None, height=None):
        try:
            s_width, s_height = ViewModel.cache('SCREEN_SIZE_LIST',
                                                type='QUE'
                                                )[-1]
            if not width:
                width = widget.width
            if not height:
                height = widget.height
            widget.geometry('+%d+%d' % (
                           (s_width - width) / 2,
                           (s_height - height) / 2)
                            )
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

