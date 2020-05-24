# -*- coding: UTF-8 -*-
import traceback
import tkinter as tk
from tkinter import ttk
import my_global as Global
from my_base import Pager
from my_module import ProgressBar, TopAbout
from my_handler import PageHandler
from my_viewutil import ToolTips, ViewUtil, WinMsg
from my_logger import Logger


class StatePage(Pager):
    """ 主备状态页面 """

    def __init__(self, master, shell, ip_list):
        self.master = master
        self.shell = shell
        self.ip_list = ip_list
        self.lab_width = 20
        self.ip_width = 16
        self.state_lab_inst = {}

    def stepper(self):
        self.pack_frame()
        PageHandler.collect_state_start(self.call_back,
                                        self.ip_list,
                                        self.shell
                                        )

    def pack_frame(self):
        _state_struct = Global.G_STATE_PAGE_STRUCT
        column, row = len(self.ip_list), len(_state_struct)
        """ 选项栏布局 """
        for sub in _state_struct:
            tk.Label(self.frame,
                     text=sub['text'],
                     width=self.lab_width,
                     font=(Global.G_FONT, 9),
                     bg='Gray80'
                     ).grid(row=_state_struct.index(sub),
                            column=0,
                            padx=1,
                            pady=1)
        """ IP横栏布局 """
        for ip in self.ip_list:
            tk.Label(self.frame,
                     text=ip,
                     width=self.ip_width,
                     font=(Global.G_FONT, 9),
                     bg='Gray80'
                     ).grid(row=0,
                            column=self.ip_list.index(ip)+1,
                            padx=1,
                            pady=1)
        """ 
        状态栏布局: 各个子状态label实例排版 
        state_inst格式: {'State': Label_instance, ...}
        state_lab_inst格式: {IP: {'State': Label_instance, ...}, ...}
        """
        for y in range(1, column+1):
            state_inst = {}
            for x in range(1, row):
                lab = tk.Label(self.frame,
                               width=self.ip_width,
                               font=(Global.G_FONT, 9),
                               bg='Snow'
                               )
                lab.grid(row=x, column=y)
                try:
                    name = _state_struct[x]['name']
                    state_inst[name] = lab
                    # print(name, x ,y)
                except Exception as e:
                    ToolTips.inner_error(e)
            self.state_lab_inst[self.ip_list[y-1]] = state_inst

    def fill_data(self, ip_state):
        """
        按照子状态label实例排版填充状态数据
        ip_state格式：(IP: {'State': State_value, ...})
        """
        ip, state_dict = ip_state
        try:
            for opt, lab_inst in self.state_lab_inst[ip].items():
                state = state_dict[opt]
                if state == 'NA':
                    color = 'Gray50'
                elif state == 'Fail':
                    color = 'Red'
                else:
                    color = 'MediumBlue'
                lab_inst['fg'] = color
                lab_inst['text'] = state
        except Exception as e:
            ToolTips.inner_error(e)
            # Logger.error(e)

    def call_back(self, *args):
        if self.alive():
            self.fill_data(args[0])


class HALogPage(Pager):
    """ 获取主备的日志 """

    def __init__(self, master, shell, ip_list):
        self.master = master
        self.shell = shell
        self.ip_list = ip_list
        self.progress = {}

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        for index in range(len(self.ip_list)):
            ip = self.ip_list[index]
            # 进度条
            prog = ProgressBar(master=self.frame,
                               name=ip,
                               size=10,
                               width=35,
                               row=index
                               )
            # self.prog = TtkProgress(self.frame, ip, row=index)
            self.progress[ip] = prog
            # 开始按钮
            ttk.Button(self.frame,
                       text='开始获取',
                       command=lambda ip=ip:
                       PageHandler.get_halog_start(
                           self.call_back, ip, self.shell)
                       ).grid(row=index,
                              column=3,
                              padx=10,
                              pady=10
                              )

    def call_back(self, *args):
        ip, value, color = args
        if self.alive():
            self.progress[ip].update(value, color)


class BinlogPage(Pager):
    """ binlog日志获取 """

    def __init__(self, master, shell, ip_list):
        self.master = master
        self.shell = shell
        self.ip_list = ip_list
        self.progress = {}

    def stepper(self):
        self.pack_frame()

    def start_wrapper(self, ip, combo):
        day_str = combo.get()
        param = 1
        if day_str == '一天':
            param = 1
        elif day_str == '一星期':
            param = 7
        elif day_str == '一个月':
            param = 30
        PageHandler.get_binlog_start(self.call_back, ip, self.shell, param)

    def pack_frame(self):
        for index in range(len(self.ip_list)):
            ip = self.ip_list[index]
            # 进度条
            prog = ProgressBar(master=self.frame,
                               name=ip,
                               size=10,
                               width=30,
                               row=index
                               )
            self.progress[ip] = prog
            # 下拉框 (选择天数)
            combo = ttk.Combobox(self.frame, width=6)
            combo['values'] = ('一天', '一星期', '一个月')
            combo.current(0)
            combo['state'] = 'readonly'
            combo.grid(row=index, column=2, padx=10)
            # 开始按钮
            ttk.Button(self.frame,
                       text='开始获取',
                       command=lambda ip=ip, combo=combo:
                       self.start_wrapper(ip, combo)
                       ).grid(row=index,
                              column=3,
                              padx=5,
                              pady=10
                              )

    def call_back(self, *args):
        ip, value, color = args
        if self.alive():
            self.progress[ip].update(value, color)


class OtherLogPage(Pager):
    """ 其他类型日志获取 """

    def __init__(self, master, shell, ip_list):
        self.master = master
        self.shell = shell
        self.ip_list = ip_list
        self.progress = {}
        self.selected_log = []
        self.selected_ip = []

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        log_fm = tk.LabelFrame(self.frame, text='日志选择')
        ips_fm = tk.LabelFrame(self.frame)
        log_fm.pack()
        ips_fm.pack()
        # tk.Checkbutton(log_fm, text='全部').grid(row=0, column=0)
        max_column = 3
        index, row, column = 0, 0, 0
        """ 日志类型布局 """
        for name in Global.G_OTHER_LOG_STRUCT:
            self.selected_log.append(0)
            column = index - (row * max_column)
            index += 1
            if column == max_column:
                row += 1
                column = 0
            tk.Checkbutton(log_fm,
                           text=name,
                           anchor='w',
                           width=30,
                           command=lambda _x=index: self.select_log(_x)
                           ).grid(row=row, column=column)
        """ IP和按钮等布局 """
        row = 0
        for ip in self.ip_list:
            tk.Checkbutton(ips_fm,
                           text=ip,
                           font=(Global.G_FONT, 10),
                           anchor='w',
                           width=20,
                           command=lambda _ip=ip: self.select_ip(_ip)
                           ).grid(row=row, column=0)
            prog = ProgressBar(master=ips_fm,
                               name='',
                               size=9,
                               width=40,
                               row=row,
                               column=1
                               )
            self.progress[ip] = prog
            row += 1
        # 开始获取按钮
        ttk.Button(self.frame,
                   text='开始获取',
                   width=20,
                   command=self.start_wrapper
                   ).pack(pady=6)

    def select_ip(self, ip):
        if ip not in self.selected_ip:
            self.selected_ip.append(ip)

    def select_log(self, index):
        value = self.selected_log[index - 1]
        if value:
            self.selected_log[index - 1] = 0
        else:
            self.selected_log[index - 1] = 1

    def start_wrapper(self, event=None):
        if not any(self.selected_log):
            WinMsg.warn("请至少选择一项日志")
            return
        if not self.selected_ip:
            WinMsg.warn("请勾选IP地址")
            return
        param = '|'.join([str(x) for x in self.selected_log])
        PageHandler.get_otherlog_start(self.call_back,
                                       self.selected_ip,
                                       self.shell,
                                       param
                                       )

    def call_back(self, *args):
        ip, value, color = args
        if self.alive():
            self.progress[ip].update(value, color)


class LogCheckPage(Pager):
    def __init__(self, master, shell, ip_list):
        ToolTips.inner_warn("暂不支持")


class HAConfigPage(Pager):
    def __init__(self, master, shell, ip_list):
        ToolTips.inner_warn("暂不支持")


class DownloadPage(Pager):
    def __init__(self, master, shell, ip_list):
        ToolTips.inner_warn("暂不支持")


class ReservePage1(Pager):
    def __init__(self, master, shell, ip_list):
        ToolTips.inner_warn("暂不支持")


class ReservePage2(Pager):
    def __init__(self, master, shell, ip_list):
        ToolTips.inner_warn("暂不支持")


class ReservePage3(Pager):
    def __init__(self, master, shell, ip_list):
        ToolTips.inner_warn("暂不支持")


class PageCtrl(object):
    """ 页面切换控制类 """

    def __init__(self, master):
        self.master = master
        self.current = None
        self.current_page = None
        self.banner_fm = tk.Frame(master)
        self.images_fm = tk.Frame(master)
        self.banner_fm.pack()
        self.images_fm.pack()
        # 横幅
        tk.Label(self.banner_fm).pack(side=tk.LEFT, ipadx=400)
        tk.Button(self.banner_fm,
                  text='？',
                  bd=0,
                  font=(Global.G_FONT, 9, 'bold'),
                  command=TopAbout.show
                  ).pack(side=tk.LEFT)
        # 图片
        tk.Label(self.images_fm, image=ViewUtil.get_image('BINGO')).pack()

    def default_page(self):
        """ 默认界面的处理 """
        PageHandler.default_page_deal()

    def swich_page(self, name, shell):
        if self.current == name:
            return
        self.current = name
        if self.images_fm:
            self.images_fm.destroy()
            self.images_fm = None
        try:
            self.current_page.destroy()
        except:
            pass
        try:
            class_name = eval(name)
            self.current_page = class_name(master=self.master,
                                           shell=shell,
                                           ip_list=ViewUtil.get_ssh_ip_list()
                                           )
            self.current_page.pack()
        except Exception as e:
            ToolTips.inner_error(e)
            Logger.error(traceback.format_exc())




