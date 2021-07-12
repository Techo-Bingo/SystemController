# -*- coding: UTF-8 -*-
"""
View板块;
处理逻辑，不包含数据
"""
import traceback
import tkinter as tk
from tkinter import ttk
import my_global as Global
from my_logger import Logger
from my_common import Common, Singleton
from my_page import PageCtrl
from my_handler import LoginHandler
from my_viewutil import ViewUtil
from my_bond import Packer, Define, Caller
from my_module import (SubLogin,
                       InfoWindow,
                       TopProgress,
                       MyButton,
                       MyTreeView,
                       MyToolBar,
                       TopAbout,
                       MyScreenshot,
                       MyFrame,
                       ScrollFrame,
                       WidgetTip,
                       MyIPChoose
                       )


class GuiBase(Singleton):
    """ 子窗体的基类 """
    master = None

    def init_windows(self):
        pass

    def destroy(self):
        self.master.destroy()

    def show(self):
        self.init_windows()


class Gui(tk.Tk):
    """ 界面入口基类 """

    def __init__(self):
        tk.Tk.__init__(self)
        """ 注册界面布局 (用于界面切换) """
        Define.define(Global.EVT_LOGIN_GUI, self.Login)
        Define.define(Global.EVT_MAIN_GUI, self.Main)
        Define.define(Global.EVT_REFRESH_GUI, self.refresh)
        Define.define(Global.EVT_CALL_WIN_INFO, WidgetTip.info)
        Define.define(Global.EVT_CALL_WIN_WARN, WidgetTip.warn)
        Define.define(Global.EVT_CALL_WIN_ERROR, WidgetTip.error)
        Define.define(Global.EVT_CALL_WIN_ASK, WidgetTip.ask)
        Define.define(Global.EVT_TOP_PROG_START, TopProgress.start)
        Define.define(Global.EVT_TOP_PROG_UPDATE, TopProgress.update)
        Define.define(Global.EVT_TOP_PROG_DESTROY, TopProgress.destroy)

    def pack(self):
        ViewUtil.init_root(self)
        self.title(Global.G_TITLE)
        self.iconbitmap(ViewUtil.get_image('ICO'))
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.Login()

    def refresh(self, msg=None):
        self.update()

    def close(self):
        if not WidgetTip.ask("请确认是否退出？"):
            return
        self.destroy()
        Common.rm_dir(Global.G_PID_DIR)
        Packer.call(Global.EVT_CLOSE_GUI)

    def Login(self, msg=None):
        """ 登录界面 """
        master_frame = tk.Frame(self)
        master_frame.pack()
        login = GuiLogin(master_frame)
        login.show()

    def Main(self, msg=None):
        ViewUtil.calculate_size()
        # 菜单栏
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        # 工具栏
        tool_frame = tk.Frame(self)
        tool_frame.pack(fill='x')
        # 主框架
        master_frame = tk.LabelFrame(self)
        master_frame.pack()  #pady=5)
        main = GuiMain(master_frame, menu_bar, tool_frame)
        main.show()
        # 底部信息栏
        foot_frame = tk.LabelFrame(self)
        foot_frame.pack(fill='x')
        tk.Label(foot_frame, text='this is foot label').pack(fill='both')


class GuiLogin(GuiBase):
    """ 登录窗 """

    def __init__(self, master):
        self.master = master

    def init_windows(self):
        def init_frames():
            win_style = {'master': self.master,
                         'width': Global.G_LGN_WIN_WIDTH,
                         'background': Global.G_DEFAULT_COLOR}
            head_win = tk.Frame(height=Global.G_LGN_HEAD_HEIGHT, **win_style)
            body_win = tk.Frame(height=Global.G_LGN_FUNC_HEIGHT, **win_style)
            foot_win = tk.Frame(height=Global.G_LGN_FOOT_HEIGHT, **win_style)
            body_fm = MyFrame(body_win,
                              width=Global.G_LGN_WIN_WIDTH,
                              height=Global.G_LGN_FUNC_HEIGHT,
                              title="登录服务器",
                              center=True,
                              color=Global.G_DEFAULT_COLOR
                              ).master()
            head_win.pack(fill='both')
            body_win.pack(fill='both')
            foot_win.pack(fill='both')
            head_win.pack_propagate(0)
            body_win.pack_propagate(0)
            foot_win.pack_propagate(0)
            body_fm.pack(fill='both')
            return head_win, body_fm, foot_win

        def pack_frames():
            def pack_sub_head_win():
                tk.Label(head_fm, image=ViewUtil.get_image('LGN_HEAD')).pack(fill='both')
            def pack_sub_body_win():
                def add_sublogin():
                    result, index = ViewUtil.add_sublogin()
                    if not result:
                        WidgetTip.info('最多支持%s个登录' % index)
                        return
                    # 通过获取当前的index值布局SubLogin
                    SubLogin(entry_fm, index)

                def pack_sub_entry_fm():
                    # 添加第一个登录子版块
                    add_sublogin()

                def pack_sub_btn_fm():
                    add_btn = tk.Button(sub_btn_fm, bd=0, text='✚', font=(Global.G_FONT, 10), command=add_sublogin)
                    add_btn.pack(side='left', padx=20)
                    # 小眼睛
                    eye_btn = tk.Button(sub_btn_fm, image=ViewUtil.get_image('LGN_EYE'), bd=0)
                    eye_btn.pack(side='right', padx=20)
                    eye_btn.bind("<Button-1>", lambda event: Packer.call(Global.EVT_SEE_PSWD_ON))
                    eye_btn.bind("<ButtonRelease-1>", lambda event: Packer.call(Global.EVT_SEE_PSWD_OFF))
                    WidgetTip.enter_tips(add_btn, '增加一个登录栏')
                    WidgetTip.enter_tips(eye_btn, '显示明文密码')

                sub_btn_fm = tk.LabelFrame(body_fm, height=20)
                scroll_fm = ScrollFrame(body_fm)
                sub_btn_fm.pack(fill='both')
                scroll_fm.pack(fill='both')
                entry_fm = scroll_fm.body
                pack_sub_entry_fm()
                pack_sub_btn_fm()
            def pack_sub_foot_win():
                def click_login(event=None):
                    def _background_login(args=None):
                        if LoginHandler.try_login():
                            WidgetTip.info('登录成功')
                            self.close()
                            # 切换到主界面
                            Caller.call(Global.EVT_MAIN_GUI)
                        else:
                            login_btn.config('state', 'normal')

                    login_btn.config('state', 'disable')
                    Common.create_thread(func=_background_login)
                # 选项按钮
                tk.Button(foot_fm,
                          text='☰',
                          font=(Global.G_FONT, 18),
                          bd=0,
                          activebackground=Global.G_DEFAULT_COLOR,
                          bg=Global.G_DEFAULT_COLOR,
                          command=self.setting
                          ).pack(side='left', padx=50)
                # 一键登录按钮
                login_btn = MyButton(foot_fm, size=14, width=26, text='一  键  登  录', command=click_login)
            pack_sub_head_win()
            pack_sub_body_win()
            pack_sub_foot_win()

        head_fm, body_fm, foot_fm = init_frames()
        pack_frames()
        ViewUtil.set_widget_size(width=Global.G_LGN_WIN_WIDTH, height=Global.G_LGN_WIN_HEIGHT)

    def setting(self):
        WidgetTip.warn('敬请期待')

    def close(self):
        self.destroy()


class GuiMain(GuiBase):
    """ 操作窗 """
    def __init__(self, master, menubar, toolbar):
        self.master = master
        self.menubar = menubar
        self.toolbar = toolbar
        self.pager = None

    def init_windows(self):
        def init_frames():
            paned_win_outer = ttk.Panedwindow(self.master,
                                              orient=tk.HORIZONTAL,
                                              width=Global.G_MAIN_WIN_WIDTH,
                                              height=Global.G_MAIN_WIN_HEIGHT)
            win_style = {'master': paned_win_outer,
                         'height': Global.G_MAIN_WIN_HEIGHT}
            tree_win = tk.Frame(width=Global.G_MAIN_TREE_WIDTH, **win_style)
            oper_win = tk.Frame(width=Global.G_MAIN_OPER_WIDTH, **win_style)
            tree_win.pack(side='left', fill='both')
            tree_win.pack_propagate(0)
            oper_win.pack(side='right', fill='both')
            oper_win.pack_propagate(0)
            paned_win_outer.add(tree_win, weight=1)
            paned_win_outer.add(oper_win, weight=3)
            paned_win_outer.pack(fill='both')
            tree_fm = MyFrame(tree_win,
                              width=Global.G_MAIN_TREE_WIDTH + 200,  # 多200，可用于拖动窗口扩展
                              height=Global.G_MAIN_WIN_HEIGHT,
                              title="导航栏"
                              ).master()
            paned_win_inner = ttk.Panedwindow(oper_win,
                                          orient=tk.VERTICAL,
                                          width=Global.G_MAIN_OPER_WIDTH,
                                          height=Global.G_MAIN_WIN_HEIGHT)
            fm_style = {'master': paned_win_inner,
                        'width': Global.G_MAIN_OPER_WIDTH}
            oper_fm = tk.Frame(height=Global.G_MAIN_OPER_HEIGHT, **fm_style)
            text_fm = tk.Frame(height=Global.G_MAIN_TEXT_HEIGHT, **fm_style)
            oper_fm.pack(fill='both')
            oper_fm.pack_propagate(0)
            text_fm.pack(fill='both')
            text_fm.pack_propagate(0)
            paned_win_inner.add(oper_fm, weight=3)
            paned_win_inner.add(text_fm, weight=1)
            paned_win_inner.pack(fill='both')
            fm_style = {'master': oper_fm,
                        'height': Global.G_MAIN_OPER_HEIGHT + 200,
                        'background': Global.G_MAIN_OPER_BG}
            page_fm = tk.Frame(width=Global.G_MAIN_PAGE_WIDTH, **fm_style)
            ips_fm = tk.Frame(width=Global.G_MAIN_IPS_WIDTH, **fm_style)
            page_fm.pack(side='left', fill='both')
            page_fm.pack_propagate(0)
            ips_fm.pack(side='left', fill='both')
            ips_fm.pack_propagate(0)
            fm_style = {'master': text_fm,
                        'height': Global.G_MAIN_TEXT_HEIGHT}
            info_fm = tk.Frame(width=Global.G_MAIN_INFO_WIDTH, **fm_style)
            note_fm = tk.Frame(width=Global.G_MAIN_NOTE_WIDTH, **fm_style)
            info_fm.pack(side='left', fill='both')
            info_fm.pack_propagate(0)
            note_fm.pack(side='left', fill='both')
            note_fm.pack_propagate(0)
            return tree_fm, page_fm, ips_fm, info_fm, note_fm

        def pack_frames():
            def _switch_page(args_tuple):
                try:
                    pager.switch_page(args_tuple)
                except Exception as e:
                    WidgetTip.error("切换界面异常：%s" % e)
                    Logger.error(traceback.format_exc())
                    return
            def _press_callback(key):
                if key == 'TB_EXPAND':
                    treeview.expand_trees()
                elif key in ['TB_INFO', "MENU_ABOUT"]:
                    TopAbout.show()
                elif key == 'TB_SCREEN_CUT':
                    MyScreenshot(self.master)
                elif key == 'MENU_EXIT':
                    ViewUtil.close_root()
                elif key in ["TB_LAST_ONE", "TB_NEXT_ONE", "TB_SETTING", "TB_HELP",
                             "MENU_OPEN", "MENU_IMPORT", "MENU_EXPORT", "MENU_OPTION", "MENU_HELP"]:
                    WidgetTip.info("敬请期待 !")
                else:
                    treeview.command(key)
            def pack_menubar():  # 菜单栏
                filemenu = tk.Menu(self.menubar, tearoff=0)
                self.menubar.add_cascade(label="文件", menu=filemenu)
                # filemenu.add_command(label=" 打开 ", command=lambda x='MENU_OPEN': self.press_callback(x))
                # filemenu.add_separator()
                # filemenu.add_command(label=" 导入 ", command=lambda x='MENU_IMPORT': self.press_callback(x))
                # filemenu.add_command(label=" 导出 ", command=lambda x='MENU_EXPORT': self.press_callback(x))
                filemenu.add_separator()
                filemenu.add_command(label=" 退出 ", command=lambda x='MENU_EXIT': _press_callback(x))
                toolmenu = tk.Menu(self.menubar, tearoff=0)
                self.menubar.add_cascade(label="工具", menu=toolmenu)
                toolmenu.add_separator()
                toolmenu.add_command(label=" 选项 ", command=lambda x='MENU_OPTION': _press_callback(x))
                helpmenu = tk.Menu(self.menubar, tearoff=0)
                self.menubar.add_cascade(label="帮助", menu=helpmenu)
                helpmenu.add_command(label=" 说明 ", command=lambda x='MENU_HELP': _press_callback(x))
                helpmenu.add_command(label=" 关于 ", command=lambda x='MENU_ABOUT': _press_callback(x))
            def pack_toolbar():  # 工具栏
                start = [('TB_EXPAND', "展开目录树"),
                         ('TB_LAST_ONE', "上一页面"),
                         ('TB_NEXT_ONE', "下一页面")]
                end = [('TB_SCREEN_CUT', "截取屏幕"),
                       ('TB_SETTING', "设置"),
                       ('TB_HELP', "帮助信息"),
                       ('TB_INFO', "关于软件")]
                toolbar_list = start + treeview.get_toolbar_keys() + end
                MyToolBar(self.toolbar, toolbar_list, _press_callback)
            def pack_sub_tree_fm():
                try:
                    treeview = MyTreeView(tree_fm, _switch_page)
                    treeview.pack_trees(ViewUtil.get_treeview_data())
                except Exception as e:
                    WidgetTip.error("界面数据异常： %s" % str(e))
                    Logger.error(traceback.format_exc())
                    return None
                return treeview
            def pack_sub_page_fm():
                def page_interface(msg):
                    # 预留界面接口
                    pass
                # 定义page页接口事件回调函数
                Define.define(Global.EVT_PAGE_INTERFACE, page_interface)
                # 初始化page
                pager = PageCtrl(page_fm)
                pager.default(Global.G_MAIN_PAGE_WIDTH, Global.G_MAIN_OPER_HEIGHT)
                return pager
            def pack_sub_ips_fm():
                fm_style = {'width': Global.G_MAIN_IPS_WIDTH,
                            'height': Global.G_MAIN_OPER_HEIGHT}
                fm = MyFrame(master=ips_fm, title="选择栏", **fm_style).master()
                MyIPChoose.show(fm)
            def pack_sub_info_fm():
                # 初始化信息提示栏
                fm = MyFrame(info_fm,
                             width=Global.G_MAIN_INFO_WIDTH,
                             height=Global.G_MAIN_TEXT_HEIGHT + 200,  # 预留 200高度用于支持窗口大小调整
                             title="提示栏").master()
                InfoWindow(fm)
            def pack_sub_note_fm():
                fm = MyFrame(note_fm,
                        width=Global.G_MAIN_NOTE_WIDTH,
                        height=Global.G_MAIN_TEXT_HEIGHT,
                        title="备注栏").master()
                tk.Text(fm).pack(fill='both')

            pack_menubar()
            treeview = pack_sub_tree_fm()
            pack_toolbar()
            pager = pack_sub_page_fm()
            pack_sub_ips_fm()
            pack_sub_info_fm()
            pack_sub_note_fm()

        tree_fm, page_fm, ips_fm, info_fm, note_fm = init_frames()
        pack_frames()
        ViewUtil.reposition(Global.G_APP_WIDTH, Global.G_APP_HEIGHT)


