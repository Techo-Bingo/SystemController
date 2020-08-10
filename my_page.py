# -*- coding: UTF-8 -*-
import traceback
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import my_global as Global
from my_common import Common
from my_logger import Logger
from my_base import Pager
from my_handler import PageHandler
from my_viewutil import ToolTips, ViewUtil, WinMsg
from my_timezone import TimezonePage
from my_module import ProgressBar, PlotMaker
from my_bond import Caller


class HomePage(Pager):
    """ 主页 """
    def __init__(self, master, width, height, ip_list, shell, options):
        self.master = master
        self.width = width
        self.height = height
        self.shell = shell
        self.ip_list = ip_list
        self.options = options
        self.plot_params = None
        self.prepare_ok = False

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        opt_fm = tk.LabelFrame(self.frame, width=self.width)
        opt_fm.pack(fill='x', padx=10, pady=10, ipady=10)
        show_lab = tk.Label(opt_fm)
        show_lab.pack()
        PageHandler.execute_showing_start(self.callback, self.ip_list[0], self.shell, None)
        while True:
            if self.prepare_ok:
                break
            Caller.call(Global.EVT_REFRESH_GUI)
            Common.sleep(0.1)
        label_list, x_list, y_lists, png_path = self.plot_params
        myplot = PlotMaker(label_list, x_list, y_lists, png_path)
        myplot.make()
        Caller.call(Global.EVT_ADD_IMAGE, ('MEM_BAR', png_path))
        show_lab.config(image=ViewUtil.get_image('MEM_BAR'))

    def callback(self, infos):
        try:
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
        except Exception as e:
            print(traceback.format_exc())
            return


class OptionDownloadTypePage(Pager):
    """ 选项执行下载类型界面 """

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
        opt_fm = tk.LabelFrame(self.frame, width=self.width, text='选项框')
        opr_fm = tk.Frame(self.frame, width=self.width)
        btn_fm = tk.Frame(opr_fm, width=self.width/3, height=self.height/5*2)
        ips_fm = tk.LabelFrame(opr_fm, width=self.width/3*2, height=self.height/5*2)
        opt_fm.pack(fill='x', padx=10, pady=10, ipady=10)
        opr_fm.pack(fill='x', padx=10, pady=10)
        ips_fm.pack(fill='both', side='left')
        btn_fm.pack(fill='x', side='left', padx=40)
        # 选项框布局
        max_column, index, row, column, var_ops = 2, 0, 0, 0, []
        for opt in self.options:
            column = index - (row * max_column)
            index += 1
            if column == max_column:
                row += 1
                column = 0
            var_ops.append(tk.IntVar())
            tk.Checkbutton(opt_fm, text=opt, anchor='w', width=40, variable=var_ops[-1]).grid(row=row, column=column)
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


class OnlyEntryEditTypePage(Pager):
    """ 单个输入框执行下载类型界面 """
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
        # 输入框布局
        if self.options[0] != "NO_SHELL_TIPS":
            tk.Label(edt_fm, text="脚本名称:", font=(Global.G_FONT, 10)
                     ).grid(row=0, column=0, padx=10, pady=10, sticky='w')
            tk.Label(edt_fm, text="%s" % self.shell, font=(Global.G_FONT, 10)
                     ).grid(row=0, column=1, padx=10, pady=10, sticky='w')
        tk.Label(edt_fm, text="%s:" % self.options[1], font=(Global.G_FONT, 10)
                 ).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.entry = ttk.Entry(edt_fm, width=60, font=(Global.G_FONT, 10))
        self.entry.grid(row=1, column=1, pady=10)
        # tips
        tk.Label(edt_fm, text="%s" % self.options[2], fg='Gray40', font=(Global.G_FONT, 9)).grid(row=2, column=1)
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


class PageCtrl(object):
    """ 页面切换控制类 """

    def __init__(self):
        self.current_text = None
        self.current_page = None
        #self.images_fm = tk.Frame(Caller.call(Global.EVT_PAGE_INTERFACE, 'get_master'))
        #self.images_fm.pack()
        # 首页图片
        #tk.Label(self.images_fm, image=ViewUtil.get_image('BINGO')).pack(fill='both')

    def destroy_page(self):
        try:
            self.current_page.destroy()
        except:
            pass

    def switch_page(self, page_text, page_type_info, shell):
        if self.current_text == page_text:
            return
        self.current_text = page_text
        #if self.images_fm:
        #    self.images_fm.destroy()
        #    self.images_fm = None
        self.destroy_page()
        page_type_info = page_type_info.replace('{', '').replace('}', '').replace(',', '')
        page_type, page_options = page_type_info.split()[0], page_type_info.split()[1:]
        width, height = Caller.call(Global.EVT_PAGE_INTERFACE, 'PAGE_SIZE')
        pager_params = {'master': Caller.call(Global.EVT_PAGE_INTERFACE, 'PAGE_MASTER'),
                        'width': width,
                        'height': height,
                        'ip_list': ViewUtil.get_ssh_ip_list(),
                        'shell': shell,
                        'options': page_options}
        try:
            if page_type == 'HOME_PAGE':
                self.current_page = HomePage(**pager_params)
            elif page_type == 'ONLY_DOWNLOAD':
                return
            elif page_type == 'OPTION_DOWNLOAD':
                self.current_page = OptionDownloadTypePage(**pager_params)
            elif page_type == 'ONLY_TEXT_SHOW':
                return
            elif page_type == 'ONLY_TEXT_EDIT':
                return
                # self.current_page = OnlyTextEditTypePage(**pager_params)
            elif page_type == 'ONLY_ENTRY_EDIT':
                self.current_page = OnlyEntryEditTypePage(**pager_params)
            elif page_type == 'SELF':
                # 自定义界面，page_options第一个元素为类名，后面的为参数
                class_name = eval(page_options[0])
                pager_params['options'] = [] if len(page_options) == 1 else page_options[1:]
                self.current_page = class_name(**pager_params)
            else:
                raise Exception("未知界面类型： %s" % page_type)
            self.current_page.pack()
        except Exception as e:
            ToolTips.inner_error(e)
            Logger.error(traceback.format_exc())

