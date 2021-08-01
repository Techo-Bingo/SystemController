# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from collections import defaultdict
from Utils.sc_func import Common
from View.sc_global import Global
from View.sc_timezone import TimezonePage
from View.Datamation.sc_provide import view_gate
from View.sc_module import WidgetTip, TitleFrame, ScrollFrame, TopNotebook

class PlotMaker:

    plot_param = None

    @classmethod
    def manual(cls, params):
        try:
            matplotlib.use('TkAgg')
            plt.ion()      # 开启interactive mode
            plt.close('all')
            '''
            l = len(params)
            if l == 1:
                axes = plt.subplots(figsize=(12, 6), nrows=1, ncols=1, sharey=True, sharex=True)[1]
                ax_list = [axes]
            elif 1 < l <= 2:
                axes = plt.subplots(figsize=(12, 6), nrows=2, ncols=1, sharey=True, sharex=True)[1]
                ax_list = [axes[1], axes[0]]
            else:
                axes = plt.subplots(figsize=(12, 6), nrows=2, ncols=2, sharey=True, sharex=True)[1]
                ax_list = [axes[1, 0], axes[0, 0], axes[1, 1], axes[0, 1]]
            '''
            download_dir = view_gate.query_env_define_data('G_DOWNLOAD_DIR')
            index = 0
            for ip, res_list in params.items():
                # proc, res, period = res_list
                proc, res = res_list
                file = "{}\\{}\\__FILE_DATA__\\{}.csv".format(download_dir, ip, proc)
                if not Common.is_file(file):
                    raise Exception("{} 不存在\n如果是首次登录，请等待30秒再进此界面".format(file))
                data = pd.read_csv(file, usecols=['Date', res], parse_dates=True, index_col=0)
                axes = plt.subplots(figsize=(12, 6), nrows=1, ncols=1, sharey=True, sharex=True)[1]
                data.plot(ax=axes, title="{}: {}".format(ip, proc), grid=True)
                #data.plot(ax=ax_list[index], title="{}: {}".format(ip, proc), grid=True)
                index += 1
            plt.rcParams['font.sans-serif'] = [u'SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            plt.subplots_adjust(wspace=0.02, hspace=0.2)  # 调整子图间距
            # plt.savefig('aa.png', dpi=200)
            plt.show()
        except Exception as e:
            WidgetTip.error(str(e))

    @classmethod
    def auto(cls, plot_param, detail=False):
        cls.plot_param = plot_param
        only_image = "TkAgg" if detail else "Agg"
        plt.close('all')
        matplotlib.use(only_image)
        plt.rcParams['font.sans-serif'] = [u'SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        instance, file_name, plot_size = plot_param
        width, height = (plot_size[0]-120)/100, plot_size[1]/100 - 0.5
        download_dir = view_gate.query_env_define_data('G_DOWNLOAD_DIR')
        pid_dir = view_gate.query_env_define_data('G_PID_DIR')
        for ip, inst in instance.items():
            file = "{}\\{}\\__FILE_DATA__\\{}".format(download_dir, ip, file_name)
            if not Common.is_file(file):
                raise Exception("{} 不存在\n请稍候重试".format(file))
            png = "{}\\{}_{}.png".format(pid_dir, ip, file_name.split('.')[0])
            data = pd.read_csv(file, parse_dates=True, index_col=0)
            data.plot(title="{}: {}".format(ip, file_name), grid=True, figsize=(width, height))
            if not detail:
                plt.savefig(png, dpi=100)
                view_gate.add_image_data.set_data(['AUTOPLOT_{}'.format(ip), png])
                inst.image_create('0.0', image=view_gate.query_photo_image_data('AUTOPLOT_{}'.format(ip)))
            else:
                plt.show()

    @classmethod
    def detail(cls):
        if not cls.plot_param:
            return
        cls.auto(cls.plot_param, True)

    @classmethod
    def close(cls, msg=None):
        plt.close('all')

class Pager(object):
    interface = None
    master = None
    title = None
    width = None
    height = None
    frame = None
    _showing = False
    _page_fm = None

    def _init(self):
        self._showing = True
        self._page_fm = tk.Frame(self.master)
        self._page_fm.pack()
        fm_style = {"width": self.width,
                    "height": self.height + 200   # 预留 200高度用于支持窗口大小调整
                    }
        fm = TitleFrame(self._page_fm, title=self.title, **fm_style).master()
        sf = ScrollFrame(fm, **fm_style)
        sf.pack(fill='both')
        sf.pack_propagate(0)
        self.frame = sf.body

    def pack(self):
        self._init()
        self.pack_frame()

    def pack_frame(self):
        pass

    def alive(self):
        return self._showing

    def destroy_frame(self):
        pass

    def destroy(self):
        self._showing = False
        try:
            self.destroy_frame()
            self._page_fm.destroy()
        except:
            pass

class PageClass(Pager):
    def __init__(self, master, title, width, height, ip_list, shell, ploter, buttons, window, widgets):
        self.master = master
        self.title = title
        self.width = width
        self.height = height
        self.shell = shell
        self.ip_list = ip_list
        self.ploter = ploter
        self.buttons = buttons
        self.window = window
        self.widgets = widgets
        # enter result结果控件实例容器
        self.enter_widgets_inst = []
        # 保存页面所有控件实例及其属性
        self.page_instance = []
        # multiCombobox 一行布置的个数
        self.column_limit = 4
        # 执行结果输出窗实例
        self.top_notebook = None

    def pack_frame(self):
        self.pack_widgets()

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
            combobox.pack(side='left', padx=10, pady=2)
            return 'Combobox', combobox
        def widget_multicombobox():
            def get_values(turned_values):
                for key in widget_values:
                    if ip in server_cache_data and key in server_cache_data[ip]:
                        turned_values += server_cache_data[ip][key]
                    else:
                        turned_values.append(key)
            row, column, multicombobox = 0, 0, []
            for ip in self.ip_list:
                turned_values = []
                get_values(turned_values)
                if column > self.column_limit - 1:
                    row += 2
                    column = 0
                tk.Label(master, text=ip).grid(row=row, column=column)
                combobox = ttk.Combobox(master, width=width, values=turned_values, state='readonly')
                if turned_values:
                    combobox.current(0)
                combobox.grid(row=row+1, column=column, padx=10)
                column += 1
                multicombobox.append((ip, combobox))
            return 'MultiCombobox', multicombobox
        def widget_checkbox():
            max_column, index, row, column, vars = 3, 0, 0, 0, []
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
            entry = ttk.Entry(master, width=width)
            entry.pack(side='left', padx=10, pady=2)
            if widget_values:
                entry.insert(0, '\n'.join(widget_values).strip())
            return 'Entry', entry
        def widget_text():
            text = scrolledtext.ScrolledText(master,
                                             font=(Global.G_DEFAULT_FONT, 10),
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
                           ).pack(side='left', pady=2)
                return 'Entry', entry
        def widget_notebook():
            notebook = ttk.Notebook(master, width=width, height=height, style="App.TNotebook")
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
        def widget_plotnotebook():
            notebook = ttk.Notebook(master, width=width, height=height, style="App.TNotebook")
            notebook.pack()
            ttk.Button(self.frame, text="查看详情", width=25, command=PlotMaker.detail).pack()
            instance = {}
            for ip in self.ip_list:
                fm = tk.Frame(notebook)
                fm.pack()
                text = scrolledtext.ScrolledText(fm, width=120, height=60)
                text.pack(fill='both')
                text['stat'] = 'disabled'
                notebook.add(fm, text=ip)
                instance[ip] = text
            return 'PlotNotebook', instance
        width, height = widget_size
        server_cache_data = view_gate.query_server_cache_data()
        # 服务器信息内部变量只能与组合控件一起使用
        if server_cache_data:
            for cache_key in list(list(server_cache_data.values())[0].keys()):
                if cache_key in widget_values and not widget_type.startswith('Multi'):
                    raise Exception("{}只能与Multi类型控件使用".format(cache_key))
        return eval("widget_{}".format(widget_type.lower()))()

    def pack_widgets(self):
        def parser_widget():
            w_type = widget['WidgetType']
            w_tips = widget['WidgetTips']
            w_values = widget['WidgetValues']
            w_params = widget['WidgetParams']
            w_attrs = widget['WidgetAttrs']
            w_actions = widget['WidgetActions']
            return w_type, w_tips, w_values, w_params, w_attrs, w_actions
        def get_widget_params():
            top_w, top_h, widget_w, widget_h = widget_params['Size']
            if widget_type == 'MultiCombobox':
                c = len(self.ip_list)
                top_h = (c//4 + (1 if c%4 else 0)) * 60
            return (top_w, top_h), (widget_w, widget_h)
        def get_widget_attrs():
            if 'ShowEnterResult' in widget_attrs:
                if widget_name not in readonly_widget:
                    raise Exception("ShowEnterResult只能用于{}".format('&'.join(readonly_widget)))
                self.enter_widgets_inst.append((widget_name, instance))
            can_null = True if 'CanBeNull' in widget_attrs else False
            # 预留一个位置
            return can_null, False
        ''' 1. 控件解析和布局 '''
        edt_fm = tk.Frame(self.frame, width=self.width)
        edt_fm.pack(fill='x', padx=5, pady=5)
        plot_widget, readonly_widget = [], ["Label", "Notebook"]
        for widget in self.widgets:
            # 解析控件数据
            widget_type, widget_tips, widget_values, widget_params, widget_attrs, widget_actions = parser_widget()
            # 获取控件参数
            top_size, widget_size = get_widget_params()
            # 布局控件
            widget_name, instance = self.create_widget(TitleFrame(master=edt_fm,
                                                               width=top_size[0],
                                                               height=top_size[1],
                                                               title='\n'.join(widget_tips)).master(),
                                                       widget_type,
                                                       widget_values,
                                                       widget_size)
            # 获取控件属性
            attrs = (get_widget_attrs())
            # 添加控件实例，用于后续点击按钮后处理，只读控件不用传入后续流程获取输入
            if widget_name == "PlotNotebook":
                plot_widget.append((instance, widget_values[0], widget_size))
            elif widget_name not in readonly_widget:
                self.page_instance.append(((widget_name, instance), attrs, widget_actions))
        ''' 2. 执行界面ENTER脚本 '''
        if self.enter_widgets_inst:
            view_gate.enter_exec_data.set_data([self.ip_list, self.shell])
        ''' 3. 自动触发型可视化界面 '''
        if self.ploter == 'AutoPlot':
            if len(plot_widget) != 1:
                raise Exception("AutoPlot型界面只能部署一个PlotNotebook控件")
            PlotMaker.auto(plot_widget[-1])

    def combine_input(self, ips):
        def get_widget_input():
            if widget == 'Combobox':  # 默认选择了第一个
                [shell_params[ip].append(str(instance.current())) for ip in ips]
            elif widget == 'MultiCombobox':  # 默认选择第一个，但可能是”“
                for ip, inst in instance:
                    if ip not in ips:
                        continue
                    _v = inst.get()
                    if not _v and not can_be_null:
                        return False
                    shell_params[ip].append(_v)
            elif widget == 'Checkbox':   # 默认无勾选
                choose = [str(_v.get()) for _v in instance]
                # 未选择任意一项
                if not can_be_null and len(set(choose)) == 1 and choose[0] == '0':
                    return False
                [shell_params[ip].append('@'.join(choose)) for ip in ips]
            elif widget == 'Entry':  # 默认为空
                for ip in ips:
                    _v = instance.get()
                    if not _v and not can_be_null:
                        return False
                    shell_params[ip].append(_v)
            elif widget == 'Text':
                _v = instance.get('1.0', 'end').strip()
                if not _v and not can_be_null:
                    return False
                f = '{0}\\__{1}_{2}__.txt'.format(pid_dir, widget, index)
                Common.write_to_file(f, _v)
                [shell_params[ip].append(f) for ip in ips]
            return True
        def parser_widget_actions():
            for act in actions:
                if act == 'UploadFile':
                    for ip in ips:
                        # 本地的文件路径传给上传列表，同时修改脚本参数为文件名
                        _local_f = shell_params[ip][-1]
                        prev_uploads[ip].append(_local_f)
                        shell_params[ip][-1] = Common.basename(_local_f)
                else:
                    WidgetTip.error("Not support WidgetAction: {}".format(act))
                    continue
        ''' 1. 校验控件输入并组装脚本参数 '''
        pid_dir = view_gate.query_env_define_data('G_PID_DIR')
        shell_params, prev_uploads, index = defaultdict(list), defaultdict(list), 0
        for item in self.page_instance:
            widget, instance = item[0]
            can_be_null, show_result = item[1]
            actions = item[2]
            index += 1
            if not get_widget_input():
                WidgetTip.warn("第{0}个必要控件{1}输入为空 !".format(index, widget))
                return None
            parser_widget_actions()    #  解析actions
        if self.ploter == 'ManualPlot':    # 手动触发型可视化界面
            PlotMaker.manual(shell_params)
            return None
        if self.ploter == '':              # 任务型事件
            if self.window:    # 开启Top窗体显示执行结果
                TopNotebook.pack(ips)
            return [shell_params, prev_uploads]

    def update_start_result(self, ip, result):
        if self.window:
            TopNotebook.insert(ip, result)

    def update_enter_result(self, ip, result):
        if not self.alive():
            return
        for key, inst in self.enter_widgets_inst:
            if key == 'Label':
                inst.set("{0}\n【 {1} 】\n{2}".format(inst.get(), ip, result))
            elif key == 'Notebook':
                text = inst[ip]
                text['stat'] = 'normal'
                text.delete('0.0', 'end')
                text.insert('end', '{}\n'.format(result))
                text.see('end')
                text['stat'] = 'disabled'

class PageCtrl(object):
    """ 页面切换控制类 """

    def __init__(self, master):
        self.master = master
        self.width = None
        self.height = None
        self.current_text = None
        self.last_text = None    # 用于切换界面失败时还原current_text
        self.current_page = None

    def default(self, width, height):
        self.width = width
        self.height = height
        master = tk.Frame(self.master)
        master.pack()
        self.current_page = master
        my_fm = TitleFrame(master, width, height, "统 计 信 息", True).master()
        fm = tk.Frame(my_fm)
        fm.pack(fill='both')
        tk.Label(fm, image=view_gate.query_photo_image_data('GUIDE')).pack()

    def switch_page(self, args_tuple):
        def destroy_page():
            try:
                self.current_page.destroy()
            except:
                pass
        def is_current():
            if self.current_text == text:
                return True
            self.last_text = self.current_text
            self.current_text = text
            return False
        def try_switch():
            task = view_gate.query_running_task_data()
            if task:
                WidgetTip.error("请等待任务 {} 执行结束或手动'取消'该任务后继续".format(task))
                return False
            return True
        def widget_type():
            widgets = view_gate.query_widgets_data()[widgeter]
            page_class, widget_types = 'PageClass', []
            for one in widgets:
                widget = one['WidgetType']
                if widget == 'Self':
                    widget_types.append(1)
                    page_class = one['WidgetValues'][0]
                elif widget in Global.G_SUPPORTED_WIDGETS:
                    widget_types.append(0)
                else:
                    raise Exception("Not support widget of {}".format(widget))
            if len(set(widget_types)) != 1:
                raise Exception("<Self>自定义控件界面不能使用<Template>模板控件")
            return page_class, widgets

        text, widgeter, shell, ploter, buttons, window = args_tuple
        if is_current():
           return self.current_page
        if not try_switch():
            self.current_text = self.last_text
            return None
        destroy_page()
        class_name, widgets = widget_type()
        pager_params = {'master': self.master,
                        'title': text,
                        'width': self.width,
                        'height': self.height,
                        'ip_list': view_gate.query_login_ip_data(),
                        'shell': shell,
                        'ploter': ploter,
                        'buttons': buttons,
                        'window': window,
                        'widgets': widgets}
        self.current_page = eval(class_name)(**pager_params)
        self.current_page.pack()
        return self.current_page
