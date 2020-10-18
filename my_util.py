# -*- coding: UTF-8 -*-
"""
Viewmodel和Model板块公共模块
"""
from time import sleep
import my_global as Global
from my_logger import Logger
from my_viewmodel import ViewModel
from PIL import Image, ImageTk
from my_common import Common, JSONParser
from my_base import FileError
from my_bond import Caller, Define


class Utils:
    """ ViewModel/Model公共封装函数 """
    _infowin_cache = []

    @classmethod
    def _background_tell(cls, args=None):
        while 1:
            sleep(0.2)
            if not ViewModel.cache('GET_INFOWIN_EVT_FLAG'):
                continue
            """ infowin准备就绪后，消费掉info信息就退出线程 """
            for info_tuple in cls._infowin_cache:
                cls._tell(info_tuple)
            del cls._infowin_cache
            return

    @classmethod
    def _tell(cls, msg):
        Caller.call(Global.EVT_INSERT_INFOWIN_TEXT, msg)

    @classmethod
    def tell_info(cls, info, level='INFO'):
        """ 打印信息，如果infowin界面未就绪，开启线程等待 """
        if not ViewModel.cache('GET_INFOWIN_EVT_FLAG'):
            if not cls._infowin_cache:
                Common.create_thread(func=cls._background_tell)
            cls._infowin_cache.append((info, level))
            return
        cls._tell((info, level))

    @classmethod
    def windows_info(cls, info):
        Caller.call(Global.EVT_CALL_WIN_INFO, info)

    @classmethod
    def windows_warn(cls, info):
        Caller.call(Global.EVT_CALL_WIN_WARN, info)

    @classmethod
    def windows_error(cls, info):
        Caller.call(Global.EVT_CALL_WIN_ERROR, info)

    @classmethod
    def windows_ask(cls, info):
        return Caller.call(Global.EVT_CALL_WIN_ASK, info)

    @classmethod
    def top_progress_update(cls, info):
        Caller.call(Global.EVT_TOP_PROG_UPDATE, info)

    @classmethod
    def top_progress_stop(cls):
        Caller.call(Global.EVT_TOP_PROG_DESTROY)

    @classmethod
    def _top_progress(cls, info):
        Caller.call(Global.EVT_TOP_PROG_START)
        cls.top_progress_update(info)

    @classmethod
    def top_progress_start(cls, info):
        Common.create_thread(func=cls._top_progress, args=(info,))


class Init:
    """ 初始化处理类 """

    @classmethod
    def check_file(cls):
        for path in [Global.G_CONF_DIR,
                     Global.G_SHELL_DIR,
                     Global.G_DEPEND_FILE,
                     Global.G_SETTING_FILE]:
            if not Common.is_exists(path):
                Logger.error("{} is not exist".format(path))
                Utils.windows_error("{} is not exist".format(path))
                return False
        Common.mkdir(Global.G_LOG_DIR)
        Common.mkdir(Global.G_DOWNLOAD_DIR)
        Common.mkdir(Global.G_TEMP_DIR)
        Common.record_pid(Global.G_PID_FILE)
        # 日志大于阈值，清空
        if Common.file_size(Global.G_LOG_PATH) > Global.G_LOG_SIZE:
            Common.write_to_file(Global.G_LOG_PATH, 'Rollback init')
        return True

    @classmethod
    def _image_init(cls, image_data):
        _photo = {}
        for name, path in image_data.items():
            if not Common.is_file(path):
                raise FileError("%s is not exist !" % path)
            _photo[name] = path if name == 'ICO' else ImageTk.PhotoImage(image=Image.open(path))
        ViewModel.cache('CONF_IMAGE_DICT', type='ADD', data=_photo)

        Define.define(Global.EVT_ADD_IMAGE, cls._define_image)

    @classmethod
    def _define_image(cls, msg):
        name, image_path = msg
        image = {}
        image[name] = ImageTk.PhotoImage(image=Image.open(image_path))
        ViewModel.cache('CONF_IMAGE_DICT', type='ADD', data=image)

    @classmethod
    def conf_parser(cls):
        try:
            # dependance.json解析
            _depend_data = JSONParser.parser(Global.G_DEPEND_FILE)
            # settings.json解析
            _setting_data = JSONParser.parser(Global.G_SETTING_FILE)
            # ViewModel初始化
            if not ViewModel.init(_setting_data['Setting']):
                raise FileError("Settings init failed !")
            # 图片数据
            cls._image_init(_depend_data['Images'])
            # TreeView数据
            ViewModel.cache('TREE_VIEW_DATA_LIST', type='ADD', data=_depend_data['Tree'])
        except Exception as e:
            Logger.error(e)
            Utils.windows_error(e)
            return False

        del _depend_data
        del _setting_data
        return True

    @classmethod
    def init_style(cls, style):
        style.theme_use('clam')   # vista
        style.configure("DEFAULT.TButton", forceground='Red')
        style.configure("TopNotebook.TNotebook", font=('微软雅黑', 11))
        style.configure("MyToolBar.TButton", borderwidth=0, relief='flat')  #background=Global.G_MAIN_OPER_BG)
        return True

    @classmethod
    def init(cls):
        Logger.info(Global.G_LOGO)
        return all([cls.check_file(), cls.conf_parser()])

