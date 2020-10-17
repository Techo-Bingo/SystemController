# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import my_global as Global
from my_common import Common
from my_base import Pager
from my_handler import PageHandler
from my_viewutil import ViewUtil, WinMsg, ToolTips
from my_timezone import TimezonePage
from my_module import ProgressBar, MyFrame, TopNotebook, CreateIPBar
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
        # 进度条实例
        self.progress = {}
        # 各控件实例和控件事件
        self.params = []

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

    def start_execute(self, ips, handler):
        def get_widget_input():
            if widget == 'Combobox':
                out = str(instance.current())
            elif widget == 'Checkbox':
                choose = [str(v.get()) for v in instance]
                # 未选择任意一项
                if len(set(choose)) == 1 and choose[0] == '0':
                    out = '@'.join(choose) if can_be_null else None
                else:
                    out = '@'.join(choose)
            elif widget == 'Entry':
                out = instance.get()
            elif widget == 'Text':
                input = instance.get('1.0', 'end').strip()
                if not input:
                    out = input
                else:
                    out = '{0}\\__{1}_{2}__.txt'.format(Global.G_TEMP_DIR, widget, index)
                    Common.write_to_file(out, input)
            else:
                out = None
            if not out and not can_be_null:
                # ToolTips.widget_tips(instance)
                WinMsg.warn("第{0}个必要控件{1}输入为空 !".format(index, widget))
                return None
            return out
        def parser_widget_actions():
            remote = param
            for act in actions:
                if act == 'UploadFile':
                    remote = "{0}/{1}".format(Global.G_UPLOAD_DIR, Common.basename(param))
                    upload_list.append((param, remote))
                else:
                    WinMsg.error("Not support WidgetAction: {}".format(act))
                    continue
            return remote
        ''' 1. 校验控件输入并组装脚本参数 '''
        shell_params, index, upload_list = "", 0, []
        for item in self.params:
            index += 1
            widget, instance, can_be_null = item[:3]
            actions = item[3:]
            # 1.1 获取控件输入信息
            param = get_widget_input()
            if not param:
                return
            # 1.2 解析actions, 如果是需要上传的，则需要把参数转换成文件上传到服务器的路径
            param = parser_widget_actions()
            # 1.3 组装脚本参数
            shell_params = "{0} '{1}'".format(shell_params, param)
        if self.print_in == 'Window':
            TopNotebook.close()
            TopNotebook.show(ips)
        ''' 2. 处理控件动作事件并执行脚本 '''
        handler.execute_start(self.callback, shell_params, upload_list)

    def stop_execute(self, handler):
        handler.execute_stop(self.callback)

    def pack_frame(self):
        self.pack_edt()
        if self.ip_choose:
            self.progress = CreateIPBar(self.frame, self.width, self.height/5*2, self.ip_list, self.button_callback)

    def button_callback(self, oper, ips, opts):
        if not ips:
            WinMsg.warn("请选择IP地址")
            return
        in_root = True if opts[0] == 1 else False
        in_back = True if opts[1] == 1 else False
        handler = PageHandler(ips, self.shell, in_root, in_back)
        if oper == 'start':
            self.start_execute(ips, handler)
        else:
            self.stop_execute(handler)

    def callback(self, ip, progress, success, out_print):
        color = False if success else 'Red'
        if not self.alive():
            return
        # 更新进度条
        self.progress[ip].update(progress, color)
        if not out_print:
            return
        if self.print_in == 'Window':
            TopNotebook.insert(ip, out_print)
        else:
            ToolTips.message_tips(out_print)


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

