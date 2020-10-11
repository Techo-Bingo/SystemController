# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import my_global as Global
# from my_common import Common
from my_base import Pager
from my_handler import PageHandler
from my_viewutil import ViewUtil, WinMsg
from my_timezone import TimezonePage
from my_module import ProgressBar, MyFrame
from my_bond import Caller, Bonder
import numpy
import matplotlib.pyplot as plot
# import matplotlib.backends.backend_tkagg
# import matplotlib.backends.backend_svg


class HomePage(Pager):
    """ 主页 """
    def __init__(self, master, width, height, ip_list, shell, options):
        self.master = master
        self.width = width
        self.height = height
        self.shell = shell
        self.ip_list = ip_list
        self.options = options
        # self.plot_params = None
        # self.prepare_ok = False
        # self.show_lab = []

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        opt_fm = tk.LabelFrame(self.frame, width=self.width)
        opt_fm.pack(fill='x', padx=10, ipady=10)
        for ip in self.ip_list:
            txt_fm = MyFrame(opt_fm, self.width, self.height/4, "【 服务器：%s 】" % ip).master()
            label = tk.Label(txt_fm, bg=Global.G_DEFAULT_COLOR, justify = 'left')
            label.pack(fill='both')
            self.get_system_infos(ip, label)

    def get_system_infos(self, ip, label):
        def callback(infos):
            label['text'] = infos
        PageHandler.execute_showing_start(callback, ip, self.shell, None)

    """
        #while True:
        #    if self.prepare_ok:
        #        break
        #    Caller.call(Global.EVT_REFRESH_GUI)
        #    Common.sleep(0.1)
        
        label_list, x_list, y_lists, png_path = self.plot_params
        PlotMaker.init()
        PlotMaker.make('内存情况', '单位：MB', label_list, x_list, y_lists, png_path)
        Caller.call(Global.EVT_ADD_IMAGE, ('MEM_BAR', png_path))
        show_lab.config(image=ViewUtil.get_image('MEM_BAR'))
    
    def callback(self, ip, infos):
        self.show_lab.config(text=infos)
        # self.prepare_ok = True
        
        infos = infos.split('\n')
        label_list = infos[0].split()
        x_list = infos[1].split()
        y_lists = []
        for line in infos[2:]:
            y_list = line.split()
            y_list = [int(y) for y in y_list]
            y_lists.append(y_list)
        png_path = "%s\\MemBar.png" % Global.G_CMDS_DIR
        self.plot_params = (label_list, x_list, y_lists, png_path)
        self.prepare_ok = True
    """


class CheckboxProgressTypePage(Pager):
    """ 复选框执行下载类型界面 """

    def __init__(self, master, width, height, ip_list, shell, options):
        self.master = master
        self.width = width
        self.height = height
        self.shell = shell
        self.ip_list = ip_list
        self.options = options
        self.progress = {}

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        opt_fm = tk.LabelFrame(self.frame, width=self.width)
        opr_fm = tk.Frame(self.frame, width=self.width)
        btn_fm = tk.Frame(opr_fm, width=self.width/3, height=self.height/5*2)
        ips_fm = tk.LabelFrame(opr_fm, width=self.width/3*2, height=self.height/5*2)
        opt_fm.pack(fill='x', padx=10, pady=10, ipady=10)
        opr_fm.pack(fill='x', padx=10, pady=10)
        ips_fm.pack(fill='both', side='left')
        btn_fm.pack(fill='x', side='left', padx=40)
        # 选项框布局
        # TODO 支持多个复选框
        (text, opts), = self.options.items()
        max_column, index, row, column, var_ops = 2, 0, 0, 0, []
        opt_master = MyFrame(opt_fm, self.width, self.height/5*3, text).master()
        for opt in opts:
            column = index - (row * max_column)
            index += 1
            if column == max_column:
                row += 1
                column = 0
            var_ops.append(tk.IntVar())
            tk.Checkbutton(opt_master, text=opt, anchor='w', width=40, variable=var_ops[-1]).grid(row=row, column=column)
        # IP和进度条布局
        row, var_ips = 0, []
        for ip in self.ip_list:
            var_ips.append(tk.IntVar())
            tk.Checkbutton(ips_fm, text=ip, font=(Global.G_FONT, 10), anchor='w', width=14, variable=var_ips[-1]
                           ).grid(row=row, column=0)
            self.progress[ip] = ProgressBar(master=ips_fm, row=row, column=1)
            row += 1
        # 执行按钮布局
        ttk.Button(btn_fm, text='执行', width=20, command=lambda x=var_ops, y=var_ips: self.start_execute(x, y)
                   ).grid(row=0, column=0, pady=15)
        ttk.Button(btn_fm, text='停止', width=20, command=lambda x=var_ips: self.stop_execute(x)
                   ).grid(row=1, column=0, pady=15)

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
        param = '@'.join([str(v.get()) for v in var_ops])
        PageHandler.execute_download_start(self.callback, select_ips, self.shell, param)

    def stop_execute(self, var_list):
        select_ip, index = [], 0
        for v in var_list:
            if int(v.get()):
                select_ip.append(self.ip_list[index])
            index += 1
        if not select_ip:
            WinMsg.warn("请勾选IP地址")
            return
        PageHandler.execute_download_stop(select_ip, self.shell)

    def callback(self, *args):
        ip, value, color = args
        if self.alive():
            self.progress[ip].update(value, color)


class ComboboxProgressTypePage(Pager):
    """ 单选框执行下载类型界面 """
    def __init__(self, master, width, height, ip_list, shell, options):
        self.master = master
        self.width = width
        self.height = height
        self.shell = shell
        self.ip_list = ip_list
        self.options = options
        self.progress = {}

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        opt_fm = tk.LabelFrame(self.frame, width=self.width)
        opr_fm = tk.Frame(self.frame, width=self.width)
        btn_fm = tk.Frame(opr_fm, width=self.width/3, height=self.height/5*2)
        ips_fm = tk.LabelFrame(opr_fm, width=self.width/3*2, height=self.height/5*2)
        opt_fm.pack(fill='x', padx=10, pady=10, ipady=10)
        opr_fm.pack(fill='x', padx=10, pady=10)
        ips_fm.pack(fill='both', side='left')
        btn_fm.pack(fill='x', side='left', padx=40)
        # 选项框布局
        # TODO 支持多个单选框
        (text, opts), = self.options.items()
        tk.Label(opt_fm, text=text).grid(row=0, column=0, padx=20, pady=10)
        combobox = ttk.Combobox(opt_fm, width=20)
        combobox['values'] = tuple(opts)
        combobox.current(0)
        combobox['state'] = 'readonly'
        combobox.grid(row=0, column=1)
        # IP和进度条布局
        row, var_ips = 0, []
        for ip in self.ip_list:
            var_ips.append(tk.IntVar())
            tk.Checkbutton(ips_fm, text=ip, font=(Global.G_FONT, 10), anchor='w', width=14, variable=var_ips[-1]
                           ).grid(row=row, column=0)
            self.progress[ip] = ProgressBar(master=ips_fm, row=row, column=1)
            row += 1
        # 执行按钮布局
        ttk.Button(btn_fm, text='执行', width=20, command=lambda x=combobox, y=var_ips: self.start_execute(x, y)
                   ).grid(row=0, column=0, pady=15)
        ttk.Button(btn_fm, text='停止', width=20, command=lambda x=var_ips: self.stop_execute(x)
                   ).grid(row=1, column=0, pady=15)

    def start_execute(self, combobox, var_ips):
        select_ips, has_ops, index = [], False, 0
        for v in var_ips:
            if int(v.get()):
                select_ips.append(self.ip_list[index])
            index += 1
        if not select_ips:
            WinMsg.warn("请勾选IP地址")
            return
        param = combobox.current()
        PageHandler.execute_download_start(self.callback, select_ips, self.shell, param)

    def stop_execute(self, var_list):
        select_ip, index = [], 0
        for v in var_list:
            if int(v.get()):
                select_ip.append(self.ip_list[index])
            index += 1
        if not select_ip:
            WinMsg.warn("请勾选IP地址")
            return
        PageHandler.execute_download_stop(select_ip, self.shell)

    def callback(self, *args):
        ip, value, color = args
        if self.alive():
            self.progress[ip].update(value, color)


class EntryProgressTypePage(Pager):
    """ 输入框执行下载类型界面 """
    def __init__(self, master, width, height, ip_list, shell, options):
        self.master = master
        self.width = width
        self.height = height
        self.shell = shell
        self.ip_list = ip_list
        self.options = options
        self.entry = None
        self.progress = {}

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        edt_fm = tk.LabelFrame(self.frame, width=self.width, text='输入框')
        opr_fm = tk.Frame(self.frame, width=self.width)
        btn_fm = tk.Frame(opr_fm, width=self.width/3, height=self.height/5*2)
        ips_fm = tk.LabelFrame(opr_fm, width=self.width/3*2, height=self.height/5*2)
        edt_fm.pack(fill='x', padx=10, pady=10, ipady=10)
        opr_fm.pack(fill='x', padx=10, pady=10)
        ips_fm.pack(fill='both', side='left')
        btn_fm.pack(fill='x', side='left', padx=40)
        tips = self.options['TipsInfo']
        entrys = self.options['EntryList']
        row = 1
        # tips
        tk.Label(edt_fm, text="%s" % tips, fg='Gray40', font=(Global.G_FONT, 9)).grid(row=0, column=1)
        # 输入框布局
        for entry_name in entrys:
            tk.Label(edt_fm, text="%s:" % entry_name, font=(Global.G_FONT, 10)
                     ).grid(row=row, column=0, padx=10, pady=10, sticky='w')
            self.entry = ttk.Entry(edt_fm, width=60, font=(Global.G_FONT, 10))
            self.entry.grid(row=row, column=1, pady=10)
            row += 1

        # IP和进度条等布局
        row, var_list = 0, []
        for ip in self.ip_list:
            var_list.append(tk.IntVar())
            tk.Checkbutton(ips_fm, text=ip, font=(Global.G_FONT, 10), anchor='w', width=14, variable=var_list[-1]
                           ).grid(row=row, column=0)
            self.progress[ip] = ProgressBar(master=ips_fm, row=row, column=1)
            row += 1
        # 执行按钮布局
        ttk.Button(btn_fm, text='执行', width=20, command=lambda x=var_list: self.start_execute(x)
                   ).grid(row=0, column=0, pady=15)
        ttk.Button(btn_fm, text='停止', width=20, command=lambda x=var_list: self.stop_execute(x)
                   ).grid(row=1, column=0, pady=15)

    def start_execute(self, var_list):
        param = self.entry.get()
        select_ip, index = [], 0
        for v in var_list:
            if int(v.get()):
                select_ip.append(self.ip_list[index])
            index += 1
        if param == '':
            WinMsg.warn("输入为空！")
            return
        if not select_ip:
            WinMsg.warn("请勾选IP地址")
            return
        PageHandler.execute_download_start(self.callback, select_ip, self.shell, param)

    def stop_execute(self, var_list):
        select_ip, index = [], 0
        for v in var_list:
            if int(v.get()):
                select_ip.append(self.ip_list[index])
            index += 1
        if not select_ip:
            WinMsg.warn("请勾选IP地址")
            return
        PageHandler.execute_download_stop(select_ip, self.shell)

    def callback(self, *args):
        ip, value, color = args
        if self.alive():
            self.progress[ip].update(value, color)


class FastRunCommandPage(Pager):
    """ 自定义界面：快速执行命令 """
    def __init__(self, master, width, height, ip_list, shell, options):
        self.master = master
        self.width = width
        self.height = height
        self.shell = shell
        self.ip_list = ip_list
        self.options = options
        self.infotext = None
        self.progress = {}
        self.is_root = tk.IntVar()
        self.is_loop = tk.IntVar()

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        edt_fm = tk.LabelFrame(self.frame, width=self.width, text='输入框')
        opt_fm = tk.LabelFrame(self.frame, width=self.width)
        opr_fm = tk.Frame(self.frame, width=self.width)
        btn_fm = tk.Frame(opr_fm, width=self.width/3, height=self.height/5*2)
        ips_fm = tk.LabelFrame(opr_fm, width=self.width/3*2, height=self.height/5*2)
        edt_fm.pack(fill='x', padx=10, pady=10)
        opt_fm.pack(fill='x', padx=10, pady=5)
        opr_fm.pack(fill='x', padx=10)
        ips_fm.pack(fill='both', side='left')
        btn_fm.pack(fill='x', side='left', padx=40)
        self.infotext = scrolledtext.ScrolledText(edt_fm,
                                                  font=(Global.G_FONT, 10),
                                                  bd=2,
                                                  relief='ridge',
                                                  bg='Snow',
                                                  height=13,
                                                  width=110)
        self.infotext.pack()
        # IP和按钮布局
        tk.Checkbutton(opt_fm, text="root执行", font=(Global.G_FONT, 10), anchor='w', width=20, variable=self.is_root
                       ).grid(row=0, column=0)
        tk.Checkbutton(opt_fm, text="循环读取(2s)", font=(Global.G_FONT, 10), anchor='w', width=20, variable=self.is_loop
                       ).grid(row=0, column=1)
        row, var_list = 0, []
        for ip in self.ip_list:
            var_list.append(tk.IntVar())
            tk.Checkbutton(ips_fm, text=ip, font=(Global.G_FONT, 10), anchor='w', width=14, variable=var_list[-1]
                           ).grid(row=row, column=0)
            self.progress[ip] = ProgressBar(master=ips_fm, row=row, column=1)
            row += 1
        ttk.Button(btn_fm, text='执行', width=20, command=lambda x=var_list: self.start_execute(x)
                   ).grid(row=0, column=0, pady=15)
        ttk.Button(btn_fm, text='停止', width=20, command=lambda x=var_list: self.stop_execute(x)
                   ).grid(row=1, column=0, pady=15)

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
        PageHandler.execute_fast_cmd_start(self.callback, select_ip, self.shell, text, self.is_root.get(), self.is_loop.get())

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

    def callback(self, *args):
        ip, value, color = args
        if self.alive():
            self.progress[ip].update(value, color)


class FastUploadFilePage(Pager):
    """ 自定义界面：快速上传界面 """
    def __init__(self, master, width, height, ip_list, shell, options):
        self.master = master
        self.width = width
        self.height = height
        self.shell = shell
        self.ip_list = ip_list
        self.options = options
        self.local_en = None
        self.server_en = None
        self.chmod_en = None
        self.chown_en = None
        self.progress = {}
        self.chmod_var = tk.StringVar()
        self.chown_var = tk.StringVar()

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        edt_fm = tk.LabelFrame(self.frame, width=self.width, text='输入框')
        opr_fm = tk.Frame(self.frame, width=self.width)
        btn_fm = tk.Frame(opr_fm, width=self.width/3, height=self.height/5*2)
        ips_fm = tk.LabelFrame(opr_fm, width=self.width/3*2, height=self.height/5*2)
        edt_fm.pack(fill='x', padx=10, pady=10, ipady=10)
        opr_fm.pack(fill='x', padx=10, pady=10)
        ips_fm.pack(fill='both', side='left')
        btn_fm.pack(fill='x', side='left', padx=40)
        # 输入栏
        tk.Label(edt_fm, text="本地文件：").grid(row=0, column=0, sticky='w', padx=5)
        entry_var = tk.StringVar()
        self.local_en = ttk.Entry(edt_fm, width=60, font=(Global.G_FONT, 10), textvariable=entry_var, state='disabled')
        self.local_en.grid(row=0, column=1, pady=10)
        ttk.Button(edt_fm, text=". . .", width=3, command=lambda x=entry_var: self.choose_file(x)
                   ).grid(row=0, column=3)
        tk.Label(edt_fm, text="服务器路径：").grid(row=1, column=0, sticky='w', padx=5)
        self.server_en = ttk.Entry(edt_fm, width=60, font=(Global.G_FONT, 10))
        self.server_en.grid(row=1, column=1, pady=10)
        tk.Label(edt_fm, text="设置权限：").grid(row=2, column=0, sticky='w', padx=5)
        tk.Label(edt_fm, text="设置属主/组：").grid(row=3, column=0, sticky='w', padx=5)
        self.chmod_en = ttk.Entry(edt_fm, textvariable=self.chmod_var)
        self.chown_en = ttk.Entry(edt_fm, textvariable=self.chown_var)
        self.chmod_en.grid(row=2, column=1, sticky='w', pady=5)
        self.chown_en.grid(row=3, column=1, sticky='w', pady=5)
        self.chmod_var.set("0640")
        self.chown_var.set("root:root")
        # 按钮栏
        row, var_list = 0, []
        for ip in self.ip_list:
            var_list.append(tk.IntVar())
            tk.Checkbutton(ips_fm, text=ip, font=(Global.G_FONT, 10), anchor='w', width=14, variable=var_list[-1]
                           ).grid(row=row, column=0)
            self.progress[ip] = ProgressBar(master=ips_fm, row=row, column=1)
            row += 1
        ttk.Button(btn_fm, text='执行', width=20, command=lambda x=var_list: self.start_execute(x)
                   ).grid(row=0, column=0, pady=15)
        ttk.Button(btn_fm, text='停止', width=20, command=lambda x=var_list: self.stop_execute(x)
                   ).grid(row=1, column=0, pady=15)

    def choose_file(self, entry_var):
        local_path = filedialog.askopenfilename()
        entry_var.set(local_path)

    def start_execute(self, var_list):
        local_path = self.local_en.get()
        remote_path = self.server_en.get()
        chmod_str = self.chmod_en.get()
        chown_str = self.chown_en.get()
        select_ip, index = [], 0
        for v in var_list:
            if int(v.get()):
                select_ip.append(self.ip_list[index])
            index += 1
        if local_path == "":
            WinMsg.warn("请选择本地上传文件")
            return
        if remote_path == "" or remote_path[0] != "/":
            WinMsg.warn("请输入服务器绝对路径")
            return
        if chmod_str == "":
            WinMsg.warn("请设置文件上传后的权限")
            return
        if chown_str == "" or len(chown_str.split(":")) != 2:
            WinMsg.warn("请正确设置文件上传后的属主/组")
            return
        if not select_ip:
            WinMsg.warn("请勾选IP地址")
            return
        PageHandler.execute_fast_upload_start(self.callback, select_ip, local_path, remote_path, chmod_str, chown_str)

    def stop_execute(self, var_list):
        select_ip, index = [], 0
        for v in var_list:
            if int(v.get()):
                select_ip.append(self.ip_list[index])
            index += 1
        PageHandler.execute_fast_upload_stop(select_ip)

    def callback(self, *args):
        ip, value, color = args
        if self.alive():
            self.progress[ip].update(value, color)


class PageClass(Pager):
    def __init__(self, master, width, height, ip_list, shell, print, ip_choose, widgets):
        self.master = master
        self.width = width
        self.height = height
        self.shell = shell
        self.ip_list = ip_list
        self.print = print
        self.ip_choose = ip_choose
        self.widgets = widgets
        self.comboboxs = []
        self.checkboxs = []
        self.entrys = []
        self.texts = []
        self.ip_vars = []
        self.progress = {}

    def pack_frame(self):
        self.pack_edt()
        self.pack_ips()

    def pack_ips(self):
        if self.ip_choose:
            fm = tk.Frame(self.frame, width=self.width)
            fm.pack(fill='x', padx=10, pady=10)
            opr_fm = MyFrame(fm, self.width, self.height, True, "服务器选择").master()
            ips_fm = tk.LabelFrame(opr_fm, width=self.width / 3 * 2, height=self.height / 5 * 2)
            ips_fm.pack(fill='both', side='left', padx=10, pady=10)
            btn_fm = tk.Frame(opr_fm, width=self.width / 3, height=self.height / 5 * 2)
            btn_fm.pack(fill='x', side='left', padx=10)
            # IP和按钮栏
            row = 0
            for ip in self.ip_list:
                self.ip_vars.append(tk.IntVar())
                tk.Checkbutton(ips_fm, text=ip,
                               font=(Global.G_FONT, 10),
                               anchor='w',
                               width=16,
                               variable=self.ip_vars[-1]
                               ).grid(row=row, column=0)
                self.progress[ip] = ProgressBar(master=ips_fm, row=row, column=1)
                row += 1
            ttk.Button(btn_fm, text='执行', width=20, command=self.start_execute).grid(row=0, column=0, pady=15)
            ttk.Button(btn_fm, text='停止', width=20, command=self.stop_execute).grid(row=1, column=0, pady=15)

    def pack_edt(self):
        def widget_label():
            tk.Label(sub_fm,
                     text='\n'.join(values),
                     width=widget_width,
                     height=widget_height
                     ).pack(side='left', padx=10)
        def widget_combobox():
            combobox = ttk.Combobox(sub_fm, width=widget_width)
            combobox['values'] = tuple(values)
            combobox.current(0)
            combobox['state'] = 'readonly'
            combobox.pack(side='left', padx=10)
            self.comboboxs.append(combobox)
        def widget_checkbox():
            max_column, index, vars, row, column = 2, 0, [], 0, 0
            for opt in values:
                column = index - (row * max_column)
                index += 1
                if column == max_column:
                    row += 1
                    column = 0
                vars.append(tk.IntVar())
                tk.Checkbutton(sub_fm,
                               text=opt,
                               anchor='w',
                               width=widget_width,
                               height=widget_height,
                               variable=vars[-1]
                               ).grid(row=row, column=column)
            self.checkboxs.append(vars)
        def widget_entry():
            var_list.append(tk.StringVar())
            entry = ttk.Entry(sub_fm, textvariable=var_list[-1], width=widget_width)
            entry.pack(side='left', padx=10)
            if values:
                var_list[-1].set('\n'.join(values))
            self.entrys.append(entry)
        def widget_text():
            text = scrolledtext.ScrolledText(sub_fm,
                                             font=(Global.G_FONT, 10),
                                             bd=2,
                                             relief='ridge',
                                             bg='Snow',
                                             height=widget_height,
                                             width=widget_width)
            text.pack()
            self.texts.append(text)
        def widget_button():
            interface, types = values[:2]
            if interface == 'ChooseFile':
                def choose_file(var):
                    local_path = filedialog.askopenfilename()
                    var.set(local_path)
                entry_var = tk.StringVar()
                entry = ttk.Entry(sub_fm, width=70, textvariable=entry_var, state='disabled')
                entry.pack(side='left', padx=10)
                btn_style = ttk.Style()
                btn_style.configure("F.TButton", font=(Global.G_FONT, 8))
                ttk.Button(sub_fm,
                           text="...",
                           width=3,
                           style="F.TButton",
                           command=lambda x=entry_var: choose_file(x)
                           ).pack(side='left')
                self.entrys.append(entry)
        # edt_fm = tk.LabelFrame(self.frame, width=self.width)
        edt_fm = tk.Frame(self.frame, width=self.width)
        edt_fm.pack(fill='x', padx=10, pady=10)
        var_list = []
        for one in self.widgets:
            widget = one['WidgetType']
            tips = one['WidgetTips']
            params = one['WidgetParams']
            values = one['WidgetValues']
            top_width, top_height, widget_width, widget_height = params['Size']
            head = True if tips else False
            sub_fm = MyFrame(edt_fm, top_width, top_height, head, '\n'.join(tips)).master()
            if widget == 'Label':
                widget_label()
            elif widget == 'Combobox':
                widget_combobox()
            elif widget == 'Checkbox':
                widget_checkbox()
            elif widget == 'Entry':
                widget_entry()
            elif widget == 'Text':
                widget_text()
            elif widget == 'Button':
                widget_button()

    def start_execute(self):
        pass

    def stop_execute(self):
        pass


class PageCtrl(object):
    """ 页面切换控制类 """

    def __init__(self):
        self.current_text = None
        self.current_page = None
        Bonder('__PageCtrl__').bond(Global.EVT_CLOSE_GUI, PlotMaker.close)

    def switch_page(self, args_tuple):
        text, widgets, shell, print, ip_choose = args_tuple
        if self.current_text == text:
            return
        self.current_text = text
        self.destroy_page()
        ip_choose = True if ip_choose == 'True' else False
        class_name, widget_types = 'PageClass', []
        for one in widgets:
            widget = one['WidgetType']
            if widget == 'Self':
                widget_types.append(1)
                class_name = one['WidgetValues'][0]
            elif widget in Global.G_SUPPORTED_WIDGETS:
                widget_types.append(0)
            else:
                raise Exception("Not support widget of {}".format(widget))
        if len(set(widget_types)) != 1:
            raise Exception("Self widget cannot coexist with Template widget")
        width, height = Caller.call(Global.EVT_PAGE_INTERFACE, 'PAGE_SIZE')
        pager_params = {'master': Caller.call(Global.EVT_PAGE_INTERFACE, 'PAGE_MASTER'),
                        'width': width,
                        'height': height,
                        'ip_list': ViewUtil.get_ssh_ip_list(),
                        'shell': shell,
                        'print': print,
                        'ip_choose': ip_choose,
                        'widgets': widgets}
        self.current_page = eval(class_name)(**pager_params)
        self.current_page.pack()

    def destroy_page(self):
        try:
            self.current_page.destroy()
        except:
            pass


class PlotMaker:

    _color = ['red', 'green', 'grey', 'blue', 'magenta']
    _figure = None

    @classmethod
    def init(cls):
        plot.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体支持
        plot.rcParams['savefig.dpi'] = 70  # 图片像素
        plot.legend(loc="upper center")
        cls._figure = plot.figure(figsize=(8, 4))

    @classmethod
    def make(cls, title, ylabel, png_path, label_list, x_list, y_lists):
        plot.title(title)
        plot.ylabel(ylabel)
        data = numpy.array(y_lists)
        ax1 = cls._figure.add_subplot(121)
        #ax2 = cls._figure.add_subplot(122)
        for i in range(len(label_list)):
            v_start = numpy.sum(data[:i], axis=0)
            ax1.bar(x_list, data[i], width=0.3, bottom=v_start, label=label_list[i], color=cls._color[i % len(label_list)])
        #ax2.
        plot.savefig(png_path)

    @classmethod
    def clear(cls):
        plot.clf()

    @classmethod
    def show(cls):
        plot.show()

    @classmethod
    def close(cls, msg=None):
        plot.close('all')


