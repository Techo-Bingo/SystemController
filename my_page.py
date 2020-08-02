# -*- coding: UTF-8 -*-
import traceback
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
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
    """ 选项执行下载类型界面 """

    def __init__(self, interface, options, shell, ip_list):
        self.interface = interface
        self.options = options
        self.shell = shell
        self.ip_list = ip_list
        self.progress = {}

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        opt_fm = tk.LabelFrame(self.frame, width=self.width, height=self.height/5*4, text='选项框')
        ips_fm = tk.LabelFrame(self.frame, width=self.width, height=self.height/5, text='服务器')
        opt_fm.pack(fill='x', pady=5, padx=5)
        ips_fm.pack(fill='x', pady=5, padx=5)
        # 选项框布局
        max_column, index, row, column, var_ops = 2, 0, 0, 0, []
        for opt in self.options:
            column = index - (row * max_column)
            index += 1
            if column == max_column:
                row += 1
                column = 0
            var_ops.append(tk.IntVar())
            tk.Checkbutton(opt_fm,
                           text=opt,
                           anchor='w',
                           width=40,
                           variable=var_ops[-1]
                           ).grid(row=row, column=column)
        # IP和进度条布局
        row, var_ips = 0, []
        for ip in self.ip_list:
            var_ips.append(tk.IntVar())
            tk.Checkbutton(ips_fm,
                           text=ip,
                           font=(Global.G_FONT, 10),
                           anchor='w',
                           width=20,
                           variable=var_ips[-1]
                           ).grid(row=row, column=0)
            self.progress[ip] = ProgressBar(master=ips_fm, name='', size=9, width=40, row=row, column=1)
            row += 1
        # 执行按钮布局
        ttk.Button(ips_fm,
                   text='开始执行',
                   width=20,
                   command=lambda x=var_ops, y=var_ips: self.start_execute(x, y)
                   ).grid(row=row+1, column=0)

    def start_execute(self, var_ops, var_ips):
        select_ips, has_ops, index = [], False, 0
        for v in var_ops:
            if int(v.get()):
                has_ops = True
                break
        for v in var_ips:
            if int(v.get()):
                select_ips.append(self.ip_list[index])
            index += 1
        if not has_ops:
            WinMsg.warn("请至少选择一个选项")
            return
        if not select_ips:
            WinMsg.warn("请勾选IP地址")
            return
        param = '|'.join([str(v.get()) for v in var_ops])
        PageHandler.execute_download_start(self.callback, select_ips, self.shell, param)

    def callback(self, *args):
        ip, value, color = args
        if self.alive():
            self.progress[ip].update(value, color)


class OnlyEntryEditTypePage(Pager):
    """ 单个输入框执行下载类型界面 """
    def __init__(self, interface, options, shell, ip_list):
        self.interface = interface
        self.options = options
        self.shell = shell
        self.ip_list = ip_list
        self.entry = None
        self.progress = {}

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        edt_fm = tk.LabelFrame(self.frame, width=self.width, height=self.height/5*2, text='输入框')
        ips_fm = tk.LabelFrame(self.frame, width=self.width, height=self.height/5*3, text='服务器')
        edt_fm.pack(fill='x', pady=5, padx=5)
        ips_fm.pack(fill='x', pady=5, padx=5)
        # 输入框布局
        if self.options[0] != "NO_SHELL_TIPS":
            tk.Label(edt_fm,
                     text="脚本名称:",
                     font=(Global.G_FONT, 11)
                     ).grid(row=0, column=0, sticky='w')
            tk.Label(edt_fm,
                     text="%s" % self.shell,
                     font=(Global.G_FONT, 11)
                     ).grid(row=0, column=1, sticky='w')
        tk.Label(edt_fm,
                 text="%s:" % self.options[1],
                 font=(Global.G_FONT, 11)
                 ).grid(row=1, column=0, sticky='w')
        self.entry = ttk.Entry(edt_fm, width=75, font=(Global.G_FONT, 10))
        self.entry.grid(row=1, column=1, pady=5)
        # tips
        tk.Label(edt_fm,
                 text="%s" % self.options[2],
                 fg='Gray40',
                 font=(Global.G_FONT, 9)
                 ).grid(row=2, column=1)
        # IP和进度条等布局
        row, var_list = 0, []
        for ip in self.ip_list:
            var_list.append(tk.IntVar())
            tk.Checkbutton(ips_fm,
                           text=ip,
                           font=(Global.G_FONT, 10),
                           anchor='w',
                           width=20,
                           variable=var_list[-1]
                           ).grid(row=row, column=0)
            self.progress[ip] = ProgressBar(master=ips_fm, name='', size=9, width=40, row=row, column=1)
            row += 1
        # 执行按钮布局
        ttk.Button(ips_fm,
                   text='开始执行',
                   width=20,
                   command=lambda x=var_list: self.start_execute(x)
                   ).grid(row=row+1, column=0)

    def start_execute(self, var_list):
        select_ip, index = [], 0
        for v in var_list:
            if int(v.get()):
                select_ip.append(self.ip_list[index])
            index += 1
        if not select_ip:
            WinMsg.warn("请勾选IP地址")
            return
        PageHandler.execute_download_start(self.callback, select_ip, self.shell, self.entry.get())

    def callback(self, *args):
        ip, value, color = args
        if self.alive():
            self.progress[ip].update(value, color)


class FastRunCommandPage(Pager):
    """ 自定义界面：快速执行命令 """
    def __init__(self, interface, shell, ip_list, params=None):
        self.interface = interface
        self.shell = shell
        self.ip_list = ip_list
        self.infotext = None
        self.is_root = tk.IntVar()
        self.is_loop = tk.IntVar()

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        txt_fm = tk.LabelFrame(self.frame, width=self.width, height=self.height/5*4, text='输入框')
        ips_fm = tk.LabelFrame(self.frame, width=self.width, height=self.height/5, text='服务器')
        txt_fm.pack(fill='x', pady=5, padx=5)
        ips_fm.pack(fill='x', pady=5, padx=5)
        self.infotext = scrolledtext.ScrolledText(txt_fm,
                                                  font=(Global.G_FONT, 10),
                                                  bd=2,
                                                  relief='ridge',
                                                  bg='Snow',
                                                  height=18,
                                                  width=110)
        self.infotext.pack()
        # IP和按钮布局
        tk.Checkbutton(ips_fm,
                       text="root执行",
                       font=(Global.G_FONT, 10),
                       anchor='w',
                       width=20,
                       variable=self.is_root
                       ).grid(row=0, column=0)
        tk.Checkbutton(ips_fm,
                       text="循环读取(2s)",
                       font=(Global.G_FONT, 10),
                       anchor='w',
                       width=20,
                       variable=self.is_loop
                       ).grid(row=0, column=1)
        column, var_list = 0, []
        for ip in self.ip_list:
            var_list.append(tk.IntVar())
            tk.Checkbutton(ips_fm, text=ip,
                           font=(Global.G_FONT, 10),
                           anchor='w',
                           width=20,
                           variable=var_list[-1]
                           ).grid(row=1, column=column)
            column += 1
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
        PageHandler.execute_fast_cmd_start(select_ip, text, self.shell, self.is_root.get(), self.is_loop.get())

    def stop_execute(self, var_list):
        select_ip, index = [], 0
        for v in var_list:
            if int(v.get()):
                select_ip.append(self.ip_list[index])
            index += 1
        if not select_ip:
            WinMsg.warn("请勾选IP地址")
            return
        PageHandler.execute_fast_cmd_stop(select_ip, self.shell)


class FastUploadFilePage(Pager):
    """ 自定义界面：快速上传界面 """
    def __init__(self, interface, shell, ip_list, params=None):
        self.interface = interface
        self.shell = shell
        self.ip_list = ip_list
        self.server_en = None
        self.chmod_en = None
        self.chown_en = None
        self.progress = {}

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        edt_fm = tk.LabelFrame(self.frame, width=self.width, height=self.height/5*2, text='输入框')
        opr_fm = tk.Frame(self.frame, width=self.width, height=self.height/5*2)
        btn_fm = tk.Frame(opr_fm, width=self.width/3, height=self.height/5*2)
        ips_fm = tk.LabelFrame(opr_fm, width=self.width/3*2, height=self.height/5*2)
        edt_fm.pack(fill='x', padx=5, pady=5)
        opr_fm.pack(fill='x', padx=5, pady=5)
        ips_fm.pack(fill='both', side='left')
        btn_fm.pack(fill='x', side='left', padx=10)
        # 输入栏
        tk.Label(edt_fm, text="本地文件：").grid(row=0, column=0, sticky='w', padx=5)
        entry_var = tk.StringVar()
        ttk.Entry(edt_fm,
                  width=60,
                  font=(Global.G_FONT, 10),
                  textvariable=entry_var,
                  state='disabled'
                  ).grid(row=0, column=1, pady=5)
        ttk.Button(edt_fm,
                   text=". . .",
                   width=3,
                   command=lambda x=entry_var: self.choose_file(x)
                   ).grid(row=0, column=3, padx=5)
        tk.Label(edt_fm, text="服务器：").grid(row=1, column=0, sticky='w', padx=5)
        self.server_en = ttk.Entry(edt_fm, width=60, font=(Global.G_FONT, 10))
        self.server_en.grid(row=1, column=1, pady=5)
        chmod_var, chown_var = tk.StringVar(), tk.StringVar()
        tk.Label(edt_fm, text="设置权限：").grid(row=2, column=0, sticky='w', padx=5)
        tk.Label(edt_fm, text="设置属主/组：").grid(row=3, column=0, sticky='w', padx=5)
        self.chmod_en = ttk.Entry(edt_fm, textvariable=chmod_var)
        self.chown_en = ttk.Entry(edt_fm, textvariable=chown_var)
        self.chmod_en.grid(row=2, column=1, sticky='w', pady=5)
        self.chown_en.grid(row=3, column=1, sticky='w', pady=5)
        chmod_var.set("0640")
        chown_var.set("root:root")
        # 按钮栏
        row, var_list = 0, []
        for ip in self.ip_list:
            var_list.append(tk.IntVar())
            tk.Checkbutton(ips_fm, text=ip,
                           font=(Global.G_FONT, 10),
                           anchor='w',
                           width=16,
                           variable=var_list[-1]
                           ).grid(row=row, column=0)
            self.progress[ip] = ProgressBar(master=ips_fm, name='', size=9, width=40, row=row, column=1)
            row += 1
        ttk.Button(btn_fm, text='执行', width=20, command=lambda x=var_list: self.start_execute(x)).grid(row=0, column=0, pady=15)
        ttk.Button(btn_fm, text='停止', width=20, command=lambda x=var_list: self.stop_execute(x)).grid(row=1, column=0, pady=15)

    def choose_file(self, entry_var):
        local_path = filedialog.askopenfilename()
        entry_var.set(local_path)
        print(self.server_en.get())

    def start_execute(self, var_list):
        print(var_list)

    def stop_execute(self, var_list):
        print(var_list)


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
                self.current_page = OnlyEntryEditTypePage(options=page_options, **pager_params)
            elif page_type == 'SELF':
                # 自定义界面，page_options第一个元素为类名，后面的为参数
                class_name = eval(page_options[0])
                params = [] if len(page_options) == 1 else page_options[1:]
                self.current_page = class_name(params=params, **pager_params)
            else:
                raise Exception("未知界面类型： %s" % page_type)
            self.current_page.pack()
        except Exception as e:
            ToolTips.inner_error(e)
            Logger.error(traceback.format_exc())

