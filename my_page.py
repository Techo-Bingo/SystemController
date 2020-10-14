# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import my_global as Global
from my_common import Common
from my_base import Pager
from my_handler import PageHandler
from my_viewutil import ViewUtil, WinMsg, ToolTips
from my_timezone import TimezonePage
from my_module import ProgressBar, MyFrame
from my_bond import Caller, Bonder
import numpy
import matplotlib.pyplot as plot


class PageClass(Pager):
    def __init__(self, master, width, height, ip_list, shell, print_in, ip_choose, widgets):
        self.master = master
        self.width = width
        self.height = height
        self.shell = shell
        self.ip_list = ip_list
        self.print_in = print_in
        self.ip_choose = ip_choose
        self.widgets = widgets
        self.ip_vars = []
        self.opt_vars = []
        self.progress = {}
        self.params = []

    def pack_frame(self):
        self.pack_edt()
        self.pack_ips()

    def callback(self, *prog_args):  # , print_args=None):
        ip, value, color = prog_args
        # out, = print_args
        if self.alive():
            self.progress[ip].update(value, color)
            #if self.print_in == 'Window':
            #    WinMsg.info(value)

    def pack_ips(self):
        if self.ip_choose:
            fm = tk.Frame(self.frame, width=self.width)
            fm.pack(fill='x', padx=10, pady=10)
            opr_fm = MyFrame(fm, self.width, self.height, True, "服务器选择").master()
            ips_fm = tk.LabelFrame(opr_fm, width=self.width / 5 * 3, height=self.height / 5 * 2)
            ips_fm.pack(fill='both', side='left', padx=10, pady=10)
            opt_fm = tk.LabelFrame(opr_fm, width=self.width / 5, height=self.height / 5 * 2)
            opt_fm.pack(fill='both', side='left', padx=10, pady=10)
            btn_fm = tk.Frame(opr_fm, width=self.width / 5, height=self.height / 5 * 2)
            btn_fm.pack(fill='x', side='left', padx=10)
            # IP和按钮栏
            row = 0
            for ip in self.ip_list:
                self.ip_vars.append(tk.IntVar())
                tk.Checkbutton(ips_fm,
                               text=ip,
                               font=(Global.G_FONT, 10),
                               anchor='w',
                               width=16,
                               variable=self.ip_vars[-1]
                               ).grid(row=row, column=0)
                self.progress[ip] = ProgressBar(master=ips_fm, row=row, column=1)
                row += 1
            for opt in ["root执行", "后台执行"]:
                self.opt_vars.append(tk.IntVar())
                tk.Checkbutton(opt_fm,
                               text=opt,
                               font=(Global.G_FONT, 10),
                               anchor='w',
                               width=16,
                               variable=self.opt_vars[-1]
                               ).pack()
            # 默认勾选root执行
            self.opt_vars[0].set(1)
            ttk.Button(btn_fm, text='执行', width=20, command=self.start_execute).grid(row=0, column=0, pady=15)
            ttk.Button(btn_fm, text='停止', width=20, command=self.stop_execute).grid(row=1, column=0, pady=15)

    def pack_edt(self):
        def get_widget_params():
            top_w, top_h, widget_w, widget_h = params['Size']
            can_null = False
            if 'CanBeNull' in params:
                can_null = True if params['CanBeNull'] == 'True' else False
            return top_w, top_h, widget_w, widget_h, can_null
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
            self.params.append(['Combobox', combobox, can_be_null] + actions)
        def widget_checkbox():
            max_column, index, row, column, vars = 2, 0, 0, 0, []
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
            self.params.append(['Checkbox', vars, can_be_null] + actions)
        def widget_entry():
            var = tk.StringVar()
            entry = ttk.Entry(sub_fm, width=widget_width, textvariable=var)
            entry.pack(side='left', padx=10)
            if values:
                var.set('\n'.join(values).strip())
            self.params.append(['Entry', entry, can_be_null] + actions)
        def widget_text():
            text = scrolledtext.ScrolledText(sub_fm,
                                             font=(Global.G_FONT, 10),
                                             bd=2,
                                             relief='ridge',
                                             bg='Snow',
                                             height=widget_height,
                                             width=widget_width)
            text.pack()
            self.params.append(['Text', text, can_be_null] + actions)
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
                self.params.append(['Entry', entry, can_be_null] + actions)
        # edt_fm = tk.LabelFrame(self.frame, width=self.width)
        edt_fm = tk.Frame(self.frame, width=self.width)
        edt_fm.pack(fill='x', padx=10, pady=10)
        for widget in self.widgets:
            type = widget['WidgetType']
            tips = widget['WidgetTips']
            values = widget['WidgetValues']
            params = widget['WidgetParams']
            actions = widget['WidgetActions']
            head = True if tips else False
            top_width, top_height, widget_width, widget_height, can_be_null = get_widget_params()
            sub_fm = MyFrame(edt_fm, top_width, top_height, head, '\n'.join(tips)).master()
            eval("widget_{}".format(type.lower()))()

    def start_execute(self):
        def get_widget_input():
            if widget == 'Combobox':
                return str(instance.current())
            elif widget == 'Checkbox':
                choose = [str(v.get()) for v in instance]
                # 未选择任意一项
                if len(set(choose)) == 1 and choose[0] == '0':
                    return '|'.join(choose) if can_be_null else None
                return '@'.join(choose)
            elif widget == 'Entry':
                return instance.get()
            elif widget == 'Text':
                input = instance.get('1.0', 'end').strip()
                if not input and not can_be_null:
                    return None
                filename = '{0}\\__{1}_{2}__.txt'.format(Global.G_TEMP_DIR, widget, index)
                Common.write_to_file(filename, input)
                return filename
            else:
                return None
        def parser_widget_actions():
            turn_path = False
            for act in actions:
                if act == 'UploadFile':
                    func = PageHandler.upload_file
                    args = (self.ip_list, self.callback, param, upload_path)
                    functions.append((act, func, args))
                    turn_path = True
                else:
                    WinMsg.error("Not support WidgetAction: {}".format(act))
                    continue
            return turn_path

        def do_widget_actions():
            for item in functions:
                act, func, args = item
                if not func(args):
                    WinMsg.error("Do active {} failed !".format(act))
                    ToolTips.message_tips("Do active {} failed !".format(act))
                    return False
            return True
        def get_selected_ip():
            ips, opts, i = [], [], 0
            for v in self.ip_vars:
                if int(v.get()):
                    ips.append(self.ip_list[i])
                i += 1
            for v in self.opt_vars:
                opts.append(int(v.get()))
            return ips, opts
        ''' 校验控件输入 '''
        shell_params, index, functions = "", 0, []
        for item in self.params:
            index += 1
            widget, instance, can_be_null = item[:3]
            actions = item[3:]
            # 获取控件输入信息
            param = get_widget_input()
            if not param and not can_be_null:
                # ToolTips.widget_tips(instance)
                WinMsg.warn("第{0}个必要控件{1}输入为空 !".format(index, widget))
                return
            # 先解析预处理actions
            upload_path = param
            if Common.is_file(param):
                upload_path = "{0}/{1}".format(Global.G_UPLOAD_DIR, Common.basename(param))
            if parser_widget_actions():
                param = upload_path
            # 组装脚本参数
            shell_params = "{0} '{1}'".format(shell_params, param)
        # 获取需要执行的IP
        select_ip, opt_list = get_selected_ip()
        if not select_ip:
            WinMsg.warn("请选择IP地址")
            return
        is_root = True if opt_list[0] else False
        # 处理控件预actions
        if not do_widget_actions():
            return
        # 远程执行脚本
        PageHandler.execute_for_progress_start(self.callback, select_ip, self.shell, shell_params, is_root)

    def stop_execute(self):
        pass


class PageCtrl(object):
    """ 页面切换控制类 """

    def __init__(self):
        self.current_text = None
        self.current_page = None
        # Bonder('__PageCtrl__').bond(Global.EVT_CLOSE_GUI, PlotMaker.close)

    def switch_page(self, args_tuple):
        def destroy_page():
            try:
                self.current_page.destroy()
            except:
                pass
        text, widgets, shell, print_in, ip_choose = args_tuple
        if self.current_text == text:
            return
        self.current_text = text
        destroy_page()
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
                        'print_in': print_in,
                        'ip_choose': ip_choose,
                        'widgets': widgets}
        self.current_page = eval(class_name)(**pager_params)
        self.current_page.pack()

