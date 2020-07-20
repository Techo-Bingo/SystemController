# -*- coding: UTF-8 -*-
import traceback
import tkinter as tk
from tkinter import ttk, scrolledtext
import my_global as Global
from my_logger import Logger
from my_base import Pager
from my_module import ProgressBar, TopAbout
from my_handler import PageHandler
from my_viewutil import ToolTips, ViewUtil, WinMsg
from my_timezone import TimezonePage


'''
class StatePage(Pager):
    """ 主备状态页面 """

    def __init__(self, interface, shell, ip_list):
        self.master = interface('get_master')
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

    def __init__(self, interface, shell, ip_list):
        self.master = interface('get_master')
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
                       command=lambda ip=ip: PageHandler.get_halog_start(self.call_back, ip, self.shell)
                       ).grid(row=index,
                              column=3,
                              padx=10,
                              pady=10)

    def call_back(self, *args):
        ip, value, color = args
        if self.alive():
            self.progress[ip].update(value, color)


class BinlogPage(Pager):
    """ binlog日志获取 """

    def __init__(self, interface, shell, ip_list):
        self.master = interface('get_master')
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
'''

class OptionDownloadTypePage(Pager):
    """ 选项下载类型界面 """

    def __init__(self, interface, options, shell, ip_list):
        self.interface = interface
        self.options = options
        self.shell = shell
        self.ip_list = ip_list
        self.progress = {}
        self.selected_opt = []
        self.selected_ip = []

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        opt_fm = tk.LabelFrame(self.frame, width=self.width, height=self.height/5*4, text='选项框')
        ips_fm = tk.LabelFrame(self.frame, width=self.width, height=self.height/5, text='服务器')
        opt_fm.pack(fill='both', pady=5)
        ips_fm.pack(fill='both')
        max_column = 3
        index, row, column = 0, 0, 0
        """ 日志类型布局 """
        for opt in self.options:

            self.selected_opt.append(0)
            column = index - (row * max_column)
            index += 1
            if column == max_column:
                row += 1
                column = 0
            tk.Checkbutton(opt_fm,
                           text=opt,
                           anchor='w',
                           width=30,
                           command=lambda _x=index: self.select_opt(_x)
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
                               column=1)
            self.progress[ip] = prog
            row += 1
        # 开始获取按钮
        ttk.Button(ips_fm,
                   text='开始获取',
                   width=20,
                   command=self.start_wrapper
                   ).grid(row=row+1, column=0)

    def select_ip(self, ip):
        if ip not in self.selected_ip:
            self.selected_ip.append(ip)

    def select_opt(self, index):
        value = self.selected_opt[index - 1]
        if value:
            self.selected_opt[index - 1] = 0
        else:
            self.selected_opt[index - 1] = 1

    def start_wrapper(self, event=None):
        if not any(self.selected_opt):
            WinMsg.warn("请至少选择一项日志")
            return
        if not self.selected_ip:
            WinMsg.warn("请勾选IP地址")
            return
        param = '|'.join([str(x) for x in self.selected_opt])
        PageHandler.execute_download_start(self.callback,
                                       self.selected_ip,
                                       self.shell,
                                       param)

    def callback(self, *args):
        ip, value, color = args
        if self.alive():
            self.progress[ip].update(value, color)


class FastRunCommandPage(Pager):

    def __init__(self, interface, shell, ip_list, params=None):
        self.interface = interface
        self.shell = shell
        self.ip_list = ip_list
        self.infotext = None
        self.selected_ip = []
        self.is_root = tk.IntVar()
        self.is_loop = tk.IntVar()

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        txt_fm = tk.LabelFrame(self.frame, width=self.width, height=self.height / 5 * 4, text='输入框')
        ips_fm = tk.LabelFrame(self.frame, width=self.width, height=self.height / 5, text='服务器')
        txt_fm.pack(fill='both', pady=5)
        ips_fm.pack(fill='both')
        self.infotext = scrolledtext.ScrolledText(txt_fm,
                                                  font=(Global.G_FONT, 10),
                                                  bd=2,
                                                  relief='ridge',
                                                  bg='Snow',
                                                  height=21,
                                                  width=110)
        self.infotext.pack()
        """ IP和按钮等布局 """
        clm, var_list = 0, []
        for ip in self.ip_list:
            var_list.append(tk.IntVar())
            tk.Checkbutton(ips_fm, text=ip, font=(Global.G_FONT, 10), anchor='w', width=20,
                           variable=var_list[-1]).grid(row=0, column=clm)
            clm += 1
        tk.Checkbutton(ips_fm, text="root执行", font=(Global.G_FONT, 10), anchor='w', width=20,
                       variable=self.is_root).grid(row=1, column=0)
        tk.Checkbutton(ips_fm, text="循环读取(2s)", font=(Global.G_FONT, 10), anchor='w', width=20,
                       variable=self.is_loop).grid(row=1, column=1)
        # 开始获取按钮
        ttk.Button(ips_fm, text='执行', width=20, command=lambda x=var_list: self.start_execute(x)).grid(row=2, column=0)
        ttk.Button(ips_fm, text='停止', width=20, command=lambda x=var_list: self.stop_execute(x)).grid(row=2, column=1)

    def start_execute(self, var_list):
        select_ip, index = [], 0
        for v in var_list:
            if int(v.get()):
                select_ip.append(self.ip_list[index])
            index += 1
        text = self.infotext.get('1.0', 'end')
        if text.strip() == '':
            WinMsg.warn("请输入命令")
            return
        if not select_ip:
            WinMsg.warn("请勾选IP地址")
            return
        PageHandler.execute_showing_start(None, select_ip, text, self.is_root.get(), self.is_loop.get())

    def stop_execute(self, var_list):
        select_ip, index = [], 0
        for v in var_list:
            if int(v.get()):
                select_ip.append(self.ip_list[index])
            index += 1
        if not select_ip:
            WinMsg.warn("请勾选IP地址")
            return
        PageHandler.execute_showing_stop(select_ip)


class PageCtrl(object):
    """ 页面切换控制类 """

    def __init__(self, interface):
        self.interface = interface
        self.current = None
        self.current_page = None
        self.images_fm = tk.Frame(interface('get_master'))
        self.images_fm.pack()
        # 首页图片
        tk.Label(self.images_fm, image=ViewUtil.get_image('BINGO')).pack(fill='both')

    def switch_page(self, page_text, page_type_info, shell):
        if self.current == page_text:
            return
        self.current = page_text
        if self.images_fm:
            self.images_fm.destroy()
            self.images_fm = None
        try:
            self.current_page.destroy()
        except:
            pass
        page_type_info = page_type_info.replace('\\{', '(').replace('\\}', ')').replace('{', '').replace('}', '').replace(',', '')
        page_type, page_options = page_type_info.split()[0], page_type_info.split()[1:]
        pager_params = {'interface': self.interface,
                        'shell': shell,
                        'ip_list': ViewUtil.get_ssh_ip_list()}
        try:
            if page_type == 'ONLY_DOWNLOAD':
                return
            elif page_type == 'OPTION_DOWNLOAD':
                self.current_page = OptionDownloadTypePage(options=page_options, **pager_params)
            elif page_type == 'ONLY_TEXT_SHOW':
                return
            elif page_type == 'ONLY_TEXT_EDIT':
                return
                # self.current_page = OnlyTextEditTypePage(**pager_params)
            elif page_type == 'ONLY_ENTRY_EDIT':
                return
            elif page_type == 'SELF':
                # 自定义界面，page_options第一个元素为类名，后面的为参数
                class_name = eval(page_options[0])
                params = [] if len(page_options) == 1 else page_options[1:]
                self.current_page = class_name(interface=self.interface,
                                               shell=shell,
                                               ip_list=ViewUtil.get_ssh_ip_list(),
                                               params=params)
            else:
                raise Exception("未知界面类型： %s" % page_type)
            self.current_page.pack()
        except Exception as e:
            ToolTips.inner_error(e)
            Logger.error(traceback.format_exc())

        '''
        try:
            class_name = eval(page_name)
            self.current_page = class_name(interface=self.interface,
                                           shell=shell,
                                           ip_list=ViewUtil.get_ssh_ip_list()
                                           )
            self.current_page.pack()
        except Exception as e:
            ToolTips.inner_error(e)
            Logger.error(traceback.format_exc())
        '''



