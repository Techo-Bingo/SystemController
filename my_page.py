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
# import numpy
# import matplotlib.pyplot as plot


class PageClass(Pager):
    def __init__(self, master, width, height, ip_list, shell, buttons, window, widgets):
        self.master = master
        self.width = width
        self.height = height
        self.shell = shell
        self.ip_list = ip_list
        self.buttons = buttons
        self.window = window
        self.widgets = widgets
        # 进度条实例
        self.progress = {}
        # 各控件实例和控件事件
        self.instance = []

    def pack_frame(self):
        self.pack_widgets()
        if self.buttons:
            self.progress = CreateIPBar(self.frame, self.width, self.height/4, self.ip_list, self.button_callback)

    def pack_widgets(self):
        def get_widget_params():
            top_w, top_h, widget_w, widget_h = widget_params['Size']
            return (top_w, top_h), (widget_w, widget_h)
        def get_widget_attrs():
            if 'ShowEnterResult' in widget_attrs:
                result_widget.append((widget_name, instance))
            can_null = True if 'CanBeNull' in widget_attrs else False
            execute = True if 'ShowExecResult' in widget_attrs else False
            return can_null, execute
        def enter_callback(ip, out_print):
            for key, inst in result_widget:
                if key == 'Label':
                    inst.set("{0}\n【 {1} 】\n{2}".format(inst.get(), ip, out_print))
                elif key == 'Notebook':
                    text = inst[ip]
                    text['stat'] = 'normal'
                    text.delete('0.0', 'end')
                    text.insert('end', '{}\n'.format(out_print))
                    text.see('end')
                    text['stat'] = 'disabled'
        ''' 1. 控件解析和布局 '''
        # edt_fm = tk.LabelFrame(self.frame, width=self.width)
        edt_fm = tk.Frame(self.frame, width=self.width)
        edt_fm.pack(fill='x', padx=10, pady=10)
        result_widget = []
        for widget in self.widgets:
            widget_type = widget['WidgetType']
            widget_tips = widget['WidgetTips']
            widget_values = widget['WidgetValues']
            widget_params = widget['WidgetParams']
            widget_attrs = widget['WidgetAttrs']
            widget_actions = widget['WidgetActions']
            # 获取控件参数
            top_size, widget_size = get_widget_params()
            # 布局控件
            master_fm = MyFrame(master=edt_fm,
                                width=top_size[0],
                                height=top_size[1],
                                head=True if widget_tips else False,
                                title='\n'.join(widget_tips)).master()
            widget_name, instance = self.create_widget(master_fm, widget_type, widget_values, widget_size)
            # 获取控件属性
            attrs = (get_widget_attrs())
            # 添加控件实例，用于后续点击按钮后处理
            # Label和Notebook目前只读，用于提示和显示界面Enter的结果
            if widget_name not in ["Label", "Notebook"]:
                self.instance.append(((widget_name, instance), attrs, widget_actions))
        ''' 2. 执行界面ENTER脚本 '''
        PageHandler(self.ip_list, self.shell, True, False).execute_enter(enter_callback)

    def create_widget(self, master, widget_type, widget_values, widget_size):
        def widget_label():
            var = tk.StringVar()
            tk.Label(master,
                     textvariable=var,
                     anchor='w',
                     justify = "left",
                     width=width,
                     height=height).pack(side='left', padx=10)
            var.set('\n'.join(widget_values))
            return 'Label', var
        def widget_combobox():
            combobox = ttk.Combobox(master, width=width, values=widget_values, state='readonly')
            combobox.current(0)
            combobox.pack(side='left', padx=10)
            return 'Combobox', combobox
        def widget_checkbox():
            max_column, index, row, column, vars = 2, 0, 0, 0, []
            for opt in widget_values:
                column = index - (row * max_column)
                index += 1
                if column == max_column:
                    row += 1
                    column = 0
                vars.append(tk.IntVar())
                tk.Checkbutton(master,
                               text=opt,
                               anchor='w',
                               width=width,
                               height=height,
                               variable=vars[-1]
                               ).grid(row=row, column=column)
            return 'Checkbox', vars
        def widget_entry():
            var = tk.StringVar()
            entry = ttk.Entry(master, width=width, textvariable=var)
            entry.pack(side='left', padx=10)
            if widget_values:
                var.set('\n'.join(widget_values).strip())
            return 'Entry', entry
        def widget_text():
            text = scrolledtext.ScrolledText(master,
                                             font=(Global.G_FONT, 10),
                                             bd=2,
                                             relief='ridge',
                                             bg='Snow',
                                             height=height,
                                             width=width)
            text.pack()
            return 'Text', text
        def widget_button():
            interface, types = widget_values[:2]
            if interface == 'ChooseFile':
                def choose_file(var):
                    local_path = filedialog.askopenfilename()
                    var.set(local_path)
                entry_var = tk.StringVar()
                entry = ttk.Entry(master, width=70, textvariable=entry_var, state='disabled')
                entry.pack(side='left', padx=10)
                ttk.Button(master,
                           text="...",
                           width=3,
                           command=lambda x=entry_var: choose_file(x)
                           ).pack(side='left')
                return 'Entry', entry
        def widget_notebook():
            notebook = ttk.Notebook(master, width=width, height=height)
            notebook.pack(side='left')
            instance = {}
            for ip in self.ip_list:
                fm = tk.Frame(notebook)
                fm.pack()
                text = scrolledtext.ScrolledText(fm, width=120, height=60)
                text.pack(fill='both')
                text['stat'] = 'disabled'
                notebook.add(fm, text=ip)
                instance[ip] = text
            return 'Notebook', instance
        width, height = widget_size
        return eval("widget_{}".format(widget_type.lower()))()

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
            name = param
            for act in actions:
                if act == 'UploadFile':
                    uploads.append(param)
                    name = Common.basename(param)
                else:
                    WinMsg.error("Not support WidgetAction: {}".format(act))
                    continue
            return name
        ''' 1. 校验控件输入并组装脚本参数 '''
        shell_params, index, uploads = "", 0, []
        for item in self.instance:
            widget, instance = item[0]
            can_be_null, show_result = item[1]
            actions = item[2]
            index += 1
            # 1.1 获取控件输入信息
            param = get_widget_input()
            if not param:
                return
            # 1.2 解析actions
            param = parser_widget_actions()
            # 1.3 组装脚本参数
            shell_params = "{0} '{1}'".format(shell_params, param)
        ''' 2. 开启Top窗体显示执行结果 '''
        if self.window:
            TopNotebook.close()
            TopNotebook.show(ips)
        ''' 3. 处理控件动作事件并执行脚本 '''
        handler.execute_start(self.result_callback, shell_params, uploads)

    def stop_execute(self, handler):
        handler.execute_stop(self.result_callback)

    def result_callback(self, ip, progress, success, out_print):
        color = False if success else 'Red'
        if not self.alive():
            return
        # 更新进度条
        self.progress[ip].update(progress, color)
        if not out_print:
            return
        if self.window:
            TopNotebook.insert(ip, out_print)
        else:
            ToolTips.message_tips(out_print)

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


class PageCtrl(object):
    """ 页面切换控制类 """

    def __init__(self):
        self.current_text = None
        self.current_page = None
        # Bonder('__PageCtrl__').bond(Global.EVT_CLOSE_GUI, PlotMaker.close)

    def default(self, master, width, height):
        _master = tk.Frame(master, width=width, height=height)
        _master.pack(fill='both')
        _master.pack_propagate(0)
        self.current_page = _master
        my_fm = MyFrame(_master, 900, 600, True, "简 单 向 导", True).master()
        fm = tk.Frame(my_fm)
        fm.pack(fill='both')
        tk.Label(fm, image=ViewUtil.get_image('GUIDE')).pack()

    def switch_page(self, args_tuple):
        def destroy_page():
            try:
                self.current_page.destroy()
            except:
                pass
        text, widgets, shell, buttons, window = args_tuple
        if self.current_text == text:
            return
        self.current_text = text
        destroy_page()
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
            raise Exception("<Self>自定义控件界面不能使用<Template>模板控件")
        width, height = Caller.call(Global.EVT_PAGE_INTERFACE, 'PAGE_SIZE')
        pager_params = {'master': Caller.call(Global.EVT_PAGE_INTERFACE, 'PAGE_MASTER'),
                        'width': width,
                        'height': height,
                        'ip_list': ViewUtil.get_ssh_ip_list(),
                        'shell': shell,
                        'buttons': buttons,
                        'window': window,
                        'widgets': widgets}
        self.current_page = eval(class_name)(**pager_params)
        self.current_page.pack()

