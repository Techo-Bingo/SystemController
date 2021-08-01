# -*- coding: UTF-8 -*-

import time
import traceback
import tkinter as tk
from tkinter import ttk
from Utils.sc_func import Common, Singleton
from View.sc_global import Global
from View.sc_page import PageCtrl, PlotMaker
from View.sc_settings import GuiSettings
from View.Datamation.sc_provide import view_gate
from View.sc_module import (WidgetTip,
                        SubLogin,
                        ColorButton,
                        TitleFrame,
                        ScrollFrame,
                        TopProgress,
                        center_window,
                        ToolBar,
                        MenuBar,
                        TopAbout,
                        ScreenShot,
                        TreeView,
                        SelectionBar,
                        InfoWindow,
                        #UploadProgress
                        )

class GuiBase(Singleton):
    """ 子窗体的基类 """
    master = None

    def init_windows(self):
        pass

    def destroy(self):
        self.master.destroy()
        del self

    def pack(self):
        self.init_windows()

class AppGate(object):
    def __init__(self):
        self.start_time = time.time()
        self.app = App()
        self.x_start = 0
        self.y_start = 0

    def run(self):
        self.app.pack()
        center_window(self.app)
        self.update_app_title(view_gate.query_title_ico_data())
        self.use_time = time.time() - self.start_time
        self.app.mainloop()

    def close(self, ask=True):
        if not self.app.close(ask):
            return
        PlotMaker.close()
        del self

    def switch_main(self):
        self.refresh()
        self.app.withdraw()
        self.app.main()
        self.app.deiconify()
        center_window(self.app)

    def refresh(self):
        Global.G_APP_WIDTH = w = self.app.winfo_screenwidth()
        Global.G_APP_HEIGHT = h = self.app.winfo_screenheight()
        if w >= 1600:
            Global.G_APP_WIDTH = 1600
        elif 1500 <= w < 1600:
            Global.G_APP_WIDTH = 1500
        elif 1400 <= w < 1500:
            Global.G_APP_WIDTH = 1400
        elif 1300 <= w < 1400:
            Global.G_APP_WIDTH = 1300
        if h >= 1000:
            Global.G_APP_HEIGHT = 950
        elif 900 <= h < 1000:
            Global.G_APP_HEIGHT = 850
        elif 800 <= h < 900:
            Global.G_APP_HEIGHT = 750
        elif 750 <= h < 800:
            Global.G_APP_HEIGHT = 700
        Global.refresh()

    def resize(self, width, height):
        self.app.geometry("{}x{}".format(width, height))

    def update_app_title(self, data):
        if not data:
            return
        title, ico = data
        if title:
            self.app.title(title)
        if ico:
            self.app.iconbitmap(ico)
    def update_app_trees(self, data):
        if not self.app.gui_main:
            return
        print('TODO update_trees for new data: {}'.format(data))

    def update_app_widgets(self, data):
        # 界面控件重新进入界面即可刷新 #
        pass
        #if not self.app.gui_main:
        #    return

    def update_login_return(self, data):
        self.app.gui_login.login_result(data)

    def update_login_state(self, data):
        if not self.app.gui_main:
            return
        self.app.gui_main.update_ip_state(data)

    def insert_text_info(self, data):
        if not self.app.gui_main:
            return
        self.app.gui_main.insert_text_info(data)

    def update_start_exec_result(self, data):
        if not self.app.gui_main:
            return
        self.app.gui_main.execute_start_result(data)

    def update_enter_exec_result(self, data):
        if not self.app.gui_main:
            return
        self.app.gui_main.execute_enter_result(data)

    def update_delay_loop_timer(self, data):
        if not self.app.gui_main:
            return
        self.app.gui_main.update_delay_loop_timer(data)

class App(tk.Tk):
    """ 界面入口基类 """

    def __init__(self):
        tk.Tk.__init__(self)
        self.gui_login = None
        self.gui_main = None

    def theme_style(self):
        style = ttk.Style()
        style.theme_use('vista')  # vista  # clam
        style.configure("App.TEntry", background=Global.G_DEFAULT_COLOR)
        style.configure("App.TButton", borderwidth=0, relief='flat')
        style.configure("App.TNotebook", tabposition='wn', background=Global.G_DEFAULT_COLOR)
        style.configure("Settings.TButton", font=(Global.G_DEFAULT_FONT, 10))

    def pack(self):
        self.theme_style()
        self.login()
        self.attributes('-topmost', 1)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.resizable(False, False)

    def close(self, ask=True):
        if ask and not WidgetTip.ask("请确认是否退出？"):
            return False
        view_gate.app_close_data.set_data(True)
        self.destroy()
        return True

    def login(self):
        """ 登录界面 """
        master = tk.Frame(self)
        master.pack()
        self.gui_login = GuiLogin(master)
        self.gui_login.pack()

    def main(self):
        self.attributes('-topmost', 0)
        master = tk.Frame(self)
        master.pack()
        menu = tk.Menu(self)
        self.config(menu=menu)
        self.gui_main = GuiMain(menu, master)
        self.gui_main.pack()

class GuiLogin(GuiBase):
    """ 登录窗 """

    def __init__(self, master):
        self.master = master
        self.head_image = view_gate.query_photo_image_data('LGN_HEAD')
        self.count_limit = view_gate.query_login_limit_data()
        self.default_pwd = view_gate.query_default_pwd_data()
        self.sub_login = []

    def init_windows(self):
        def init_frames():
            win_style = {'master': self.master,
                         'width': Global.G_LGN_WIN_WIDTH,
                         'background': Global.G_DEFAULT_COLOR}
            head_win = tk.Frame(height=Global.G_LGN_HEAD_HEIGHT, **win_style)
            body_win = tk.Frame(height=Global.G_LGN_FUNC_HEIGHT, **win_style)
            foot_win = tk.Frame(height=Global.G_LGN_FOOT_HEIGHT, **win_style)
            body_fm = TitleFrame(body_win,
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
                tk.Label(head_fm, image=self.head_image).pack(fill='both')
            def pack_sub_body_win():
                def see_password(turn):
                    for inst in self.sub_login:
                        inst.see_password(turn)
                def add_sublogin():
                    if len(self.sub_login) >= self.count_limit:
                        WidgetTip.info('最多支持%s个登录' % self.count_limit)
                        return
                    SubLogin(entry_fm, preference_ip, self.default_pwd, self.sub_login)
                def pack_sub_entry_fm():
                    # 添加第一个登录子版块
                    add_sublogin()
                def pack_sub_btn_fm():
                    btn_style = {'master': sub_btn_fm,
                                 'font': (Global.G_DEFAULT_FONT, 10),
                                 'bd': 0}
                    add_btn = tk.Button(text='✚', command=add_sublogin, **btn_style)
                    add_btn.pack(side='left', padx=20)
                    eye_btn = tk.Button(text='👀', **btn_style)
                    eye_btn.pack(side='right', padx=20)
                    eye_btn.bind("<Button-1>", lambda event,t=True: see_password(t))
                    eye_btn.bind("<ButtonRelease-1>", lambda event, t=False: see_password(t))
                    WidgetTip.enter_tips(add_btn, '增加一个登录栏', 10, 15)
                    WidgetTip.enter_tips(eye_btn, '显示明文密码', 10, 15)
                sub_btn_fm = tk.LabelFrame(body_fm, height=20)
                scroll_fm = ScrollFrame(body_fm)
                sub_btn_fm.pack(fill='both')
                scroll_fm.pack(fill='both')
                entry_fm = scroll_fm.body
                pack_sub_entry_fm()
                pack_sub_btn_fm()
            def pack_sub_foot_win():
                def settings():
                    GuiSettings.pack()
                def click_login():
                    def async_login(args=None):
                        self.login_handle()
                        try:
                            login_btn.disable(False)
                        except:
                            pass
                    login_btn.disable(True)
                    Common.create_thread(func=async_login)
                # 选项按钮
                set_byn = tk.Button(foot_fm,
                                  text='☰',
                                  font=(Global.G_DEFAULT_FONT, 18),
                                  bd=0,
                                  activebackground=Global.G_DEFAULT_COLOR,
                                  bg=Global.G_DEFAULT_COLOR,
                                  command=settings
                                  )
                set_byn.pack(side='left', padx=50)
                WidgetTip.enter_tips(set_byn, '首选项', 10, 15)
                # 一键登录按钮
                login_btn = ColorButton(foot_fm, size=14, width=26, text='一  键  登  录', command=click_login)
            pack_sub_head_win()
            pack_sub_body_win()
            pack_sub_foot_win()

        app_gate.resize(Global.G_LGN_WIN_WIDTH, Global.G_LGN_WIN_HEIGHT)
        preference_ip = view_gate.query_preference_ip_data()
        head_fm, body_fm, foot_fm = init_frames()
        pack_frames()

    def login_handle(self):
        def check_input():
            if not all(input_list):
                WidgetTip.error('输入不可为空')
                return False
            ip, user, upwd, rpwd = input_list
            if not Common.is_ip(ip):
                WidgetTip.error('请输入正确的IP地址')
                return False
            if ip in ip_exist_list:
                WidgetTip.error('{} 输入重复'.format(ip))
                return False
            ip_exist_list.append(ip)
            return True
        login_ip_data, ip_exist_list = [], []
        for inst in self.sub_login:
            input_list = inst.get_inputs()
            if not check_input():
                inst.set_status(Global.G_TIP_FG_COLOR['FAILED'])
                return
            login_ip_data.append(input_list)
        self.top_prog = TopProgress()
        self.top_prog.update('登录中, 请稍候...')
        view_gate.try_login_data.set_data(login_ip_data)

    def login_result(self, data):
        index, state, info = data
        if index == 'ALL':   # 最后结果
            self.top_prog.destroy()
            WidgetTip.info(info)
            if state:
                self.destroy()
                app_gate.switch_main()
        else:   # 单个登录结果
            instance = self.sub_login[index]
            self.top_prog.update(info)
            instance.set_status(Global.G_TIP_FG_COLOR[state])

class GuiMain(GuiBase):
    """ 操作窗 """
    def __init__(self, menu, master):
        self.master = master
        self.menu = menu
        self.info_inst = None
        self.page_inst = None
        self.select_inst = None
        self.page_args = None
        self.upload_inst = None
        self.last_page_key = None

    def init_windows(self):
        def init_frames():
            # 工具栏
            tool_fm = tk.Frame(self.master)
            tool_fm.pack(fill='x')
            # 主框架
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
            tree_fm = TitleFrame(tree_win,
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
                        'background': Global.G_MAIN_PAGE_COLOR}
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
            # 底部信息栏
            foot_fm = tk.LabelFrame(self.master)
            foot_fm.pack(fill='x')
            return tool_fm, tree_fm, page_fm, ips_fm, info_fm, note_fm, foot_fm

        def pack_frames():
            def switch_page(args_tuple):
                # image, text, widgets, shell, ploter, buttons, window = args_tuple = self.page_args
                self.page_args = []
                [self.page_args.append(i) for i in list(args_tuple)]
                try:
                    button = args_tuple[5]
                    new_page = pager.switch_page(args_tuple[1:])
                    if not new_page and self.last_page_key:
                        tree_inst.selection(self.last_page_key)     # 界面切换失败时还原到上一个可用界面
                        return
                    self.last_page_key = args_tuple[0]
                    self.page_inst = new_page
                    self.select_inst.show_button(button)
                except Exception as e:
                    WidgetTip.error("切换界面异常：%s" % e)
                    view_gate.exception_data.set_data(traceback.format_exc())
            def press_bar_handle(key):
                if key == 'TB_EXPAND':
                    tree_inst.expand_trees()
                elif key in ['TB_ABOUT', "MENU_ABOUT"]:
                    TopAbout()
                elif key in ['TB_SCREEN', 'MENU_SCREEN']:
                    ScreenShot()
                elif key in ['TB_HELP', 'MENU_HELP']:
                    pdf = 'SystemController.pdf'
                    if not Common.is_file(pdf):
                        WidgetTip.error('{}不存在,请确认!'.format(pdf))
                        return
                    Common.create_thread(lambda: Common.system_open(pdf))
                elif key in ['MENU_SET', 'TB_SET']:
                    GuiSettings.pack()
                elif key == 'MENU_EXIT':
                    app_gate.close()
                elif key == 'TB_LAST':
                    tree_inst.last()
                elif key == 'TB_NEXT':
                    tree_inst.next()
                elif key in ["MENU_WHITE", "MENU_BLACK"]:
                    WidgetTip.info("敬请期待 !")
                else:
                    # 根据界面 image 值即可进入对应界面 #
                    tree_inst.selection(key)
            def pack_menubar():
                trees = {'文件': ['-', ('MENU_EXIT', '退出')],
                         '设置': [('MENU_SET', '首选项'), '-', {'主题': [('MENU_WHITE', '白天'), ('MENU_BLACK', '黑夜')]}],
                         '工具': [('MENU_SCREEN', '截取屏幕')],
                         '帮助': [('MENU_HELP', '帮助文档'), ('MENU_ABOUT', '关于软件')]}
                MenuBar(self.menu, trees, press_bar_handle)
            def pack_toolbar():
                start = [('TB_EXPAND', "展开目录树"),
                         ('TB_LAST', "上一页面"),
                         ('TB_NEXT', "下一页面")]
                end = [('TB_SCREEN', "截取屏幕"),
                       ('TB_SET', "设置"),
                       ('TB_HELP', "帮助文档"),
                       ('TB_ABOUT', "关于软件")]
                toolbar_list = start + tree_inst.get_toolbar_keys() + end
                return ToolBar(tool_fm, toolbar_list, press_bar_handle)
            def pack_sub_tree_fm():
                tree_view_data = view_gate.query_tree_view_data()
                try:
                    treeview = TreeView(tree_fm, tree_view_data, switch_page)
                except Exception as e:
                    WidgetTip.error("界面数据异常： %s" % str(e))
                    view_gate.exception_data.set_data(traceback.format_exc())
                    app_gate.close(ask=False)
                return treeview
            def pack_sub_page_fm():
                pager = PageCtrl(page_fm)    # 初始化page
                pager.default(Global.G_MAIN_PAGE_WIDTH, Global.G_MAIN_OPER_HEIGHT)
                return pager
            def pack_sub_ips_fm():
                fm_style = {'width': Global.G_MAIN_IPS_WIDTH,
                            'height': Global.G_MAIN_OPER_HEIGHT}
                fm = TitleFrame(master=ips_fm, title="选择栏", **fm_style).master()
                select_bar = SelectionBar(fm, view_gate.query_login_ip_data(), self.execute_handle)
                [select_bar.set_status(ip, state) for ip, state in view_gate.query_ips_state_data().items()]
                select_bar.show_button(False)
                return select_bar
            def pack_sub_info_fm():
                # 初始化信息提示栏
                fm = TitleFrame(info_fm,
                             width=Global.G_MAIN_INFO_WIDTH,
                             height=Global.G_MAIN_TEXT_HEIGHT + 200,  # 预留 200高度用于支持窗口大小调整
                             title="提示栏").master()
                return InfoWindow(fm)
            def pack_sub_note_fm():
                fm = TitleFrame(note_fm,
                        width=Global.G_MAIN_NOTE_WIDTH,
                        height=Global.G_MAIN_TEXT_HEIGHT,
                        title="备注栏").master()
                tk.Text(fm).pack(fill='both')
            def pack_sub_foot_fm():
                def update_info():
                    while True:
                        time.sleep(60)
                        sec = time.time() - app_gate.start_time
                        run_time = '软件运行时长 {} 小时 {} 分钟'.format(int(sec / 3600), int((sec % 3600) / 60))
                        text = "{}      {}".format(use_time, run_time)
                        label['text'] = text
                use_time = '软件启动耗时 %.3f 秒' % app_gate.use_time
                run_time = '软件运行时长 0 小时 0 分钟'
                Common.create_thread(update_info)
                label = tk.Label(foot_fm, text="{}      {}".format(use_time, run_time))
                label.pack()

            pack_menubar()
            tree_inst = pack_sub_tree_fm()
            tool_inst = pack_toolbar()
            self.select_inst = pack_sub_ips_fm()
            self.info_inst = pack_sub_info_fm()
            pager = pack_sub_page_fm()
            pack_sub_note_fm()
            pack_sub_foot_fm()

        app_gate.resize(Global.G_APP_WIDTH, Global.G_APP_HEIGHT)
        tool_fm, tree_fm, page_fm, ips_fm, info_fm, note_fm, foot_fm = init_frames()
        pack_frames()

    def execute_handle(self, data):
        oper, ips, opts = data
        if not ips:
            WidgetTip.warn("请选择IP地址")
            return
        root, delay, loop = opts
        script = self.page_args[3]
        if oper == 'stop':
            view_gate.stop_exec_data.set_data([ips, script])
            return
        params = self.page_inst.combine_input(ips)
        if not params:
            return
        scripts_args, upload_list = params
        #upload_gui = False
        #for ip, up_list in upload_list.items():
        #    for file in up_list:
        #        if Common.file_size(file) > 10485760:   # 10MB以下文件不显示上传进度窗
        #            upload_gui = True
        #            break
        #    if upload_gui:
        #        break
        #if upload_gui:
        #    self.upload_inst = UploadProgress(ips)
        exec_data = [ips, script, root, delay, loop, scripts_args, upload_list]
        view_gate.start_exec_data.set_data(exec_data)

    def execute_enter_result(self, data):
        if not self.page_inst.alive():
            return
        ip, result = data
        if result:
            self.page_inst.update_enter_result(ip, result)

    def execute_start_result(self, data):
        if not self.page_inst.alive():
            return
        ip, progress, result, success = data
        self.select_inst.set_progress(ip, progress, success)    # 更新进度条
        if result:
            self.page_inst.update_start_result(ip, result)
            # self.info_inst.insert(result)

    def insert_text_info(self, data):
        info, level = data
        self.info_inst.insert_text(info, level)

    def update_ip_state(self, data):
        for ip, item in data.items():
            self.select_inst.set_status(ip, item['STATE'])

    def update_delay_loop_timer(self, data):
        first, next = data
        self.select_inst.update_timer(first, next)


app_gate = AppGate()
