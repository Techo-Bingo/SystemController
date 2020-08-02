# -*- coding: UTF-8 -*-
"""
View板块;
处理逻辑，不包含数据
"""
import tkinter as tk
from tkinter import ttk
import my_global as Global
from my_base import GuiBase
from my_common import Common
from my_page import PageCtrl
from my_handler import LoginHandler
from my_viewutil import WinMsg, ViewUtil, ToolTips
from my_bond import Bonder, Packer, Define
from my_module import (SubLogin,
                       InfoWindow,
                       TopProgress,
                       MyButton,
                       MyTreeView,
                       MyToolBar,
                       TopAbout)


class Gui(tk.Tk):
    """ 界面入口基类 """
    _in_main_gui = False

    def __init__(self):
        tk.Tk.__init__(self)
        """ 注册界面布局 (用于界面切换) """
        self.bonder = Bonder(self.__class__.__name__)
        self.bonder.bond(Global.EVT_LOGIN_GUI, self.Login)
        self.bonder.bond(Global.EVT_MAIN_GUI, self.Main)
        Define.define(Global.EVT_CALL_WIN_INFO, WinMsg.info)
        Define.define(Global.EVT_CALL_WIN_WARN, WinMsg.warn)
        Define.define(Global.EVT_CALL_WIN_ERROR, WinMsg.error)
        Define.define(Global.EVT_CALL_WIN_ASK, WinMsg.ask)
        Define.define(Global.EVT_TOP_PROG_START, TopProgress.start)
        Define.define(Global.EVT_TOP_PROG_UPDATE, TopProgress.update)
        Define.define(Global.EVT_TOP_PROG_DESTROY, TopProgress.destroy)

    def settitle(self):
        self.title(Global.G_TITLE)
        self.iconbitmap(ViewUtil.get_image('ICO'))
        self.resizable(False, False)
        ViewUtil.set_maxsize(self.maxsize())

    def setsize(self, width, height, reposition=True):
        if reposition:
            ViewUtil.set_centered(self, width, height)
        else:
            self.geometry('%sx%s' % (width, height))

    def pack(self):
        self.settitle()
        # 默认登录窗口并绑定关闭窗口函数
        # Packer.call(Global.EVT_LOGIN_GUI)
        self.Login()
        self.protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        """ 关闭窗口 """
        if self._in_main_gui and not WinMsg.ask("请确认是否退出？"):
            return
        self.bonder.unbond(Global.EVT_LOGIN_GUI)
        self.bonder.unbond(Global.EVT_MAIN_GUI)
        self.destroy()

    def Login(self, msg=None):
        """ 登录界面 """
        master_frame = tk.Frame(self)
        master_frame.pack()
        login = GuiLogin(master_frame, self.setsize)
        login.show()

    def Main(self, msg=None):
        # 菜单栏
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        # 工具栏
        tool_frame = tk.Frame(self)
        tool_frame.pack(fill='x')
        # 主界面
        master_frame = tk.Frame(self)
        master_frame.pack()
        main = GuiMain(menu_bar, tool_frame, master_frame, self.setsize)
        main.show()
        self._in_main_gui = True


class GuiLogin(GuiBase):
    """ 登录窗 """

    def __init__(self, master, setsize):
        self.master = master
        self.setsize = setsize
        self.head_win = None
        self.func_win = None
        self.foot_win = None
        self.login_fm = None
        self.login_btn = None

    def init_frame(self):
        win_style = {'master': self.master,
                     'width': Global.G_LGN_WIN_WIDTH,
                     'background': Global.G_DEFAULT_COLOR}
        self.head_win = tk.Frame(height=Global.G_LGN_HEAD_HEIGHT, **win_style)
        self.func_win = tk.Frame(height=Global.G_LGN_FUNC_HEIGHT, **win_style)
        self.foot_win = tk.Frame(height=Global.G_LGN_FOOT_HEIGHT, **win_style)
        self.login_fm = tk.LabelFrame(self.func_win,
                                      text=' 登录服务器 ',
                                      font=('楷体', 12),
                                      labelanchor='n')

    def pack_frame(self):
        self.head_win.pack(fill='both')
        self.func_win.pack(fill='both')
        self.login_fm.pack(fill='both')
        self.foot_win.pack(fill='both')
        '''固定Frame的长和宽，不会随其中的控件多少改变'''
        self.head_win.pack_propagate(0)
        self.func_win.pack_propagate(0)
        self.foot_win.pack_propagate(0)
        # 子控件布局
        self.pack_subframe()
        self.setsize(Global.G_LGN_WIN_WIDTH, Global.G_LGN_WIN_HEIGHT)

    def pack_subframe(self):
        lab_style = {'master': self.login_fm,
                     'font': (Global.G_FONT, 10)}
        # 顶部图片
        tk.Label(self.head_win, image=ViewUtil.get_image('LGN_HEAD')).pack(fill='both')
        # 输入框提示词
        tk.Label(text='IP', **lab_style).grid(row=1, column=1)
        tk.Label(text='用户名', **lab_style).grid(row=1, column=2)
        tk.Label(text='用户密码', **lab_style).grid(row=1, column=3)
        tk.Label(text='root密码', **lab_style).grid(row=1, column=4)
        # 添加一个登录子版块
        self.add_sublogin()
        # 小眼睛
        eyebtn = tk.Button(self.login_fm, image=ViewUtil.get_image('LGN_EYE'), bd=0)
        eyebtn.grid(row=2, column=5, padx=3)
        eyebtn.bind("<Button-1>",
                    lambda event: Packer.call(Global.EVT_SEE_PSWD_ON))
        eyebtn.bind("<ButtonRelease-1>",
                    lambda event: Packer.call(Global.EVT_SEE_PSWD_OFF))
        # 选项按钮
        tk.Button(self.foot_win,
                  text='☰',
                  font=(Global.G_FONT, 18),
                  bd=0,
                  activebackground=Global.G_DEFAULT_COLOR,
                  bg=Global.G_DEFAULT_COLOR,
                  command=self.show_options
                  ).pack(side='left', padx=50)
        # 一键登录按钮
        self.login_btn = MyButton(self.foot_win,
                                  text='一  键  登  录',
                                  command=self.click_login,
                                  size=14,
                                  width=26
                                  )
        # 添加登录框按钮
        tk.Button(self.foot_win,
                  text='＋',
                  font=(Global.G_FONT, 22),
                  bd=0,
                  activebackground=Global.G_DEFAULT_COLOR,
                  bg=Global.G_DEFAULT_COLOR,
                  command=self.add_sublogin
                  ).pack(side='left', padx=50)

    def add_sublogin(self):
        """ 增加登录子版块 """
        result, index = ViewUtil.add_sublogin()
        if not result:
            WinMsg.info('最多支持%s个登录' % index)
            return
        # 通过获取当前的index值布局SubLogin
        SubLogin(self.login_fm, index)

    def _background_login(self, args=None):
        if LoginHandler.try_login():
            WinMsg.info('登录成功')
            self.close()
            # 切换到主界面
            Packer.call(Global.EVT_MAIN_GUI)
        else:
            self.login_btn.config('state', 'normal')

    def click_login(self):
        self.login_btn.config('state', 'disable')
        Common.create_thread(func=self._background_login)

    def show_options(self):
        WinMsg.warn('敬请期待')

    def close(self):
        self.destroy()


class GuiMain(GuiBase):
    """ 操作窗 """
    def __init__(self, menubar, toolbar, master, setsize):
        self.master = master
        self.setsize = setsize
        self.tree_window = None
        self.oper_window = None
        self.help_window = None
        self.treeview = None
        self.info_fm = None
        self.oper_fm = None
        self.help_fm = None
        self.pager = None
        self.init_menubar(menubar)
        self.init_toolbar(toolbar)

    def init_menubar(self, menubar):
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=filemenu)
        filemenu.add_command(label=" 打开 ", command=lambda x='MENU_OPEN': self.callback(x))
        filemenu.add_separator()
        filemenu.add_command(label=" 导入 ", command=lambda x='MENU_IMPORT': self.callback(x))
        filemenu.add_command(label=" 导出 ", command=lambda x='MENU_EXPORT': self.callback(x))
        filemenu.add_separator()
        filemenu.add_command(label=" 退出 ", command=lambda x='MENU_EXIT': self.callback(x))
        toolmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="工具", menu=toolmenu)
        toolmenu.add_separator()
        toolmenu.add_command(label=" 选项 ", command=lambda x='MENU_OPTION': self.callback(x))
        helpmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=helpmenu)
        helpmenu.add_command(label=" 说明 ", command=lambda x='MENU_HELP': self.callback(x))
        helpmenu.add_command(label=" 关于 ", command=lambda x='MENU_ABOUT': self.callback(x))

    def hello(self, event=None):
        pass

    def init_toolbar(self, toolbar):
        images = [('TB_EXPAND', "展开目录树"),
                  ('TB_LAST_ONE', "上一页面"),
                  ('TB_NEXT_ONE', "下一页面"),
                  ('TB_RUN_CMD', "运行命令"),
                  ('TB_DOWNLOAD', "快速下载"),
                  ('TB_UPLOAD', "快速上传"),
                  ('TB_SCREEN_CUT', "截取屏幕"),
                  ('TB_SETTING', "设置"),
                  ('TB_HELP', "帮忙信息"),
                  ('TB_INFO', "关于软件")]
        MyToolBar(toolbar, images, self.callback)

    def init_frame(self):
        win_style = {'master': self.master,
                     'height': Global.G_MAIN_WIN_HEIGHT}
        self.tree_window = tk.Frame(width=Global.G_MAIN_TREE_WIDTH, **win_style)
        self.oper_window = tk.Frame(width=Global.G_MAIN_OPER_WIDTH, **win_style)
        fm_style = {'master': self.oper_window,
                    'width': Global.G_MAIN_OPER_WIDTH,
                    'background': Global.G_MAIN_OPER_BG}
        self.oper_fm = tk.Frame(height=Global.G_MAIN_OPER_HEIGHT, **fm_style)
        self.info_fm = tk.Frame(height=Global.G_MAIN_INFO_HEIGHT, **fm_style)

    def pack_frame(self):
        self.tree_window.pack(side='left')
        self.oper_window.pack(side='left')
        self.tree_window.pack_propagate(0)
        self.oper_window.pack_propagate(0)
        self.pack_subframe()
        # 先设置最大窗口的中心布局，后进行初始窗体大小设置
        self.setsize(Global.G_MAIN_WIN_WIDTH, Global.G_MAIN_WIN_HEIGHT)
        self.setsize(Global.G_MAIN_WIN_WIDTH-Global.G_MAIN_HELP_WIDTH, Global.G_MAIN_WIN_HEIGHT, False)

    def init_treeview(self):
        self.treeview = MyTreeView(self.tree_window, ViewUtil.get_treeview_data(), self.switch_page)

    def pack_subframe(self):
        self.init_treeview()
        self.oper_fm.pack(fill='both')
        self.info_fm.pack(fill='both')
        self.oper_fm.pack_propagate(0)
        self.info_fm.pack_propagate(0)
        # 初始化信息提示栏
        InfoWindow(self.info_fm)
        # 初始化page
        self.pager = PageCtrl(self.interface)
        # self.show_help_window(True)

    def show_help_window(self, show=False):
        if show:
            self.setsize(Global.G_MAIN_WIN_WIDTH, Global.G_MAIN_WIN_HEIGHT, False)
            self.help_window = tk.Frame(self.master, width=Global.G_MAIN_HELP_WIDTH, height=Global.G_MAIN_WIN_HEIGHT)

            self.help_window.pack(side='left')
            self.help_window.pack_propagate(0)
        else:
            self.setsize(Global.G_MAIN_WIN_WIDTH-Global.G_MAIN_HELP_WIDTH, Global.G_MAIN_WIN_HEIGHT, False)
            self.help_window.destroy()
            self.help_window = None

    def switch_page(self, args_tuple):
        page_text, page_type_info, shell = args_tuple
        self.pager.switch_page(page_text, page_type_info, shell)

    def interface(self, key):
        if key == 'get_master':
            return self.oper_fm
        elif key == 'get_range':
            return Global.G_MAIN_OPER_WIDTH, Global.G_MAIN_OPER_HEIGHT
        elif key == 'show_help':
            self.show_help_window(True)
        elif key == 'hide_help':
            self.show_help_window(False)

    def callback(self, text):
        print(text)
        if text == 'TB_EXPAND':
            self.treeview.expand_trees()
        elif text == 'TB_HELP':
            self.show_help_window(False) if self.help_window else self.show_help_window(True)
        elif text == 'TB_INFO':
            TopAbout.show()

