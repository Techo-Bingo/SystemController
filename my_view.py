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
from my_module import SubLogin, LabelButton, InfoWindow, TopProgress, MyButton


class Gui(tk.Tk):
    """ 界面入口基类 """
    _master_frame = None

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

    def set_title(self):
        self.title(Global.G_TITLE)
        self.iconbitmap(ViewUtil.get_image('ICO'))
        self.resizable(False, False)
        ViewUtil.set_maxsize(self.maxsize())
        ViewUtil.set_centered(self,
                              Global.G_LGN_WIN_WIDTH,
                              Global.G_LGN_WIN_WIDTH
                              )

    def pack(self):
        self.set_title()
        # 默认登录窗口并绑定关闭窗口函数
        # Packer.call(Global.EVT_LOGIN_GUI)
        self.Login()
        self.protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        """ 关闭窗口 """
        self.bonder.unbond(Global.EVT_LOGIN_GUI)
        self.bonder.unbond(Global.EVT_MAIN_GUI)
        self.destroy()
        """
        Define.undefine(Global.EVT_CALL_WIN_INFO)
        Define.undefine(Global.EVT_CALL_WIN_WARN)
        Define.undefine(Global.EVT_CALL_WIN_ERROR)
        Define.undefine(Global.EVT_CALL_WIN_ASK)
        """

    def Login(self, msg=None):
        """ 登录界面 """
        self._master_frame = tk.Frame(self)
        login = GuiLogin(self._master_frame)
        login.show()

    def Main(self, msg=None):
        """ 主操作界面 """
        self._master_frame = tk.Frame(self)
        main = GuiMain(self._master_frame)
        main.show()


class GuiLogin(GuiBase):
    """ 登录窗 """

    def __init__(self, master):
        self.master = master
        self.head_win = None
        self.func_win = None
        self.foot_win = None
        self.login_fm = None
        self.login_btn = None

    def init_frame(self):
        win_style = {'master': self.master,
                     'width': Global.G_LGN_WIN_WIDTH,
                     'background': Global.G_DEFAULT_COLOR
                     }
        self.head_win = tk.Frame(height=Global.G_LGN_HEAD_HEIGHT, **win_style)
        self.func_win = tk.Frame(height=Global.G_LGN_FUNC_HEIGHT, **win_style)
        self.foot_win = tk.Frame(height=Global.G_LGN_FOOT_HEIGHT, **win_style)
        self.login_fm = tk.LabelFrame(self.func_win,
                                      text=' 用 户 登 录 ',
                                      font=('楷体', 12),
                                      labelanchor='n'
                                      )

    def pack_frame(self):
        self.head_win.pack()
        self.func_win.pack()
        self.login_fm.pack()
        self.foot_win.pack()
        '''固定Frame的长和宽，不会随其中的控件多少改变'''
        self.head_win.pack_propagate(0)
        self.func_win.pack_propagate(0)
        self.foot_win.pack_propagate(0)
        # 子控件布局
        self.pack_subframe()

    def pack_subframe(self):
        lab_style = {'master': self.login_fm,
                     'font': (Global.G_FONT, 10)
                     }
        head_img = ViewUtil.get_image('HEAD')
        eye_img = ViewUtil.get_image('EYE')
        # 顶部图片
        tk.Label(self.head_win, image=head_img).pack()
        # 2个label占位用
        tk.Label(self.login_fm, font=(Global.G_FONT, 6)).grid(row=0, column=0)
        tk.Label(self.login_fm).grid(row=1, column=0)
        # 输入框提示词
        tk.Label(text='IP', **lab_style).grid(row=1, column=1)
        tk.Label(text='用户名', **lab_style).grid(row=1, column=2)
        tk.Label(text='用户密码', **lab_style).grid(row=1, column=3)
        tk.Label(text='root密码', **lab_style).grid(row=1, column=4)
        # 添加一个登录子版块
        self.add_sublogin()
        # 小眼睛
        eyebtn = tk.Button(self.login_fm, image=eye_img, bd=0)
        eyebtn.grid(row=2, column=5, padx=3)
        eyebtn.bind("<Button-1>",
                    lambda event: Packer.call(Global.EVT_SEE_PSWD_ON))
        eyebtn.bind("<ButtonRelease-1>",
                    lambda event: Packer.call(Global.EVT_SEE_PSWD_OFF))
        # 菜单按钮
        tk.Button(self.foot_win,
                  text='☰',
                  font=(Global.G_FONT, 18),
                  bd=0,
                  activebackground=Global.G_DEFAULT_COLOR,
                  bg=Global.G_DEFAULT_COLOR,
                  command=self.show_menu
                  ).pack(side=tk.LEFT, padx=50)
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
                  ).pack(side=tk.LEFT, padx=50)

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

    def show_menu(self):
        WinMsg.warn('敬请期待')

    def close(self):
        self.destroy()


class GuiMain(GuiBase):
    """ 操作窗 """
    def __init__(self, master):
        self.master = master
        self.left_win = None
        self.midd_win = None
        self.right_win = None
        self.info_fm = None
        self.view_fm = None
        self.page = None

    def init_frame(self):
        win_style = {'master': self.master,
                     'height': Global.G_MAIN_WIN_HEIGHT
                     }
        self.left_win = tk.Frame(width=Global.G_MAIN_LEFT_WIDTH, **win_style)
        self.midd_win = tk.Frame(width=Global.G_MAIN_MIDD_WIDTH, **win_style)
        fm_style = {'master': self.midd_win,
                    'width': Global.G_MAIN_MIDD_WIDTH,
                    'background': Global.G_MAIN_VIEW_BG
                    }
        self.view_fm = tk.Frame(height=Global.G_MAIN_VIEW_HEIGHT, **fm_style)
        self.info_fm = tk.Frame(height=Global.G_MAIN_WIN_HEIGHT -
                                       Global.G_MAIN_VIEW_HEIGHT, **fm_style)

    def pack_frame(self):
        self.left_win.pack(side=tk.LEFT)
        self.midd_win.pack(side=tk.LEFT)
        self.left_win.pack_propagate(0)
        self.midd_win.pack_propagate(0)
        self.pack_subframe()

    def pack_subframe(self):
        intvar = tk.IntVar()
        # intvar.set(1)
        for sub in Global.G_PAGES_NAME_DATA:
            try:
                _name = sub['name']
                _txt = sub['text']
                _shell = sub['shell']
            except Exception as e:
                ToolTips.inner_error(e)
                return
            LabelButton(self.left_win,
                        name=_name,
                        shell=_shell,
                        intvar=intvar,
                        text=_txt,
                        command=self.switch_page
                        ).pack()
        self.view_fm.pack()
        self.info_fm.pack()
        self.view_fm.pack_propagate(0)
        self.info_fm.pack_propagate(0)
        """ 初始化信息提示栏 """
        InfoWindow(self.info_fm)
        """ 初始化page """
        self.page = PageCtrl(self.view_fm)
        self.page.default_page()

    def switch_page(self, name, shell):
        self.page.swich_page(name, shell)

    def view_rightwin(self, show=False):
        if show:
            if self.right_win:
                return
            self.right_win = tk.Frame(self.master,
                                      width=Global.G_MAIN_RIGHT_WIDTH,
                                      height=Global.G_MAIN_WIN_HEIGHT
                                      )
            self.right_win.pack(side=tk.LEFT)
            self.right_win.pack_propagate(0)
        else:
            if not self.right_win:
                return
            self.right_win.destroy()
            self.right_win = None

