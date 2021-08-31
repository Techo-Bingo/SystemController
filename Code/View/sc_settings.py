# -*- coding: UTF-8 -*-

import tkinter as tk
from tkinter import ttk
from View.sc_global import Global
from View.sc_module import WidgetTip, LabelEntry, LabelCombobox, TitleFrame, center_window
from View.Datamation.sc_provide import view_gate

class GuiSettings:
    is_showing = False
    top = None
    settings = None

    @classmethod
    def pack(cls):
        if cls.is_showing:
            cls.top.wm_attributes('-topmost', 1)
            return
        cls.is_showing = True
        width, height = Global.G_LGN_WIN_WIDTH, Global.G_LGN_WIN_HEIGHT
        cls.settings = settings = view_gate.query_settings_data()
        cls.top = top = tk.Toplevel()
        top.geometry('{}x{}'.format(width, height))
        top.resizable(False, False)
        top.wm_attributes('-topmost', 1)
        top.protocol("WM_DELETE_WINDOW", cls.cancel)
        center_window(top)
        master = TitleFrame(cls.top, width=width, height=height).master()
        fm1 = tk.LabelFrame(master, text='工具选项设置')
        fm1.pack(fill='x', pady=10)
        cls.tool_alias = LabelEntry(fm1, '工具别名', settings.tool_alias, row=0)
        cls.tool_version = LabelEntry(fm1, '工具版本号', settings.tool_version, row=1)
        cls.log_level = LabelCombobox(fm1, '日志级别',
                                      ['debug', 'info', 'warning', 'error'],
                                      settings.log_level,
                                      row=2)
        cls.count_limit = LabelCombobox(fm1, '服务器同时登录最大数',
                                        list(range(1, 21)),
                                        settings.login_count_limit,
                                        row=3)
        cls.retry_times = LabelCombobox(fm1, '登录/操作执行失败重试次数',
                                        list(range(1, 6)),
                                        settings.retry_times,
                                        row=4)
        cls.refresh_json = LabelCombobox(fm1, '工具配置文件刷新周期(秒)',
                                         [2, 5, 10, 20, 30, 60],
                                         settings.refresh_json_period,
                                         row=5)

        fm2 = tk.LabelFrame(master, text='工具默认输入设置')
        fm2.pack(fill='x', pady=10)
        cls.user_name = LabelEntry(fm2, '默认用户名', settings.default_passwords[0], row=0)
        cls.user_password = LabelEntry(fm2, '默认用户密码', settings.default_passwords[1], row=1)
        cls.root_password = LabelEntry(fm2, '默认root密码', settings.default_passwords[2], row=2)

        fm3 = tk.LabelFrame(master, text='服务器设置')
        fm3.pack(fill='x', pady=10)
        cls.server_home = LabelEntry(fm3, '工具所在服务器目录', settings.server_dir, row=0)
        cls.keepalive_period = LabelCombobox(fm3, 'SSH保活周期(秒)',
                                             [10, 30, 60, 120, 180, 300, 600],
                                             settings.keepalive_period,
                                             row=1)

        fm4 = tk.Frame(master)
        fm4.pack(fill='x', pady=10)
        btn_style = {'master': fm4,
                     'width': 14,
                     'style': "Settings.TButton"}
        ttk.Button(text='确定', command=cls.confirm, **btn_style).pack(side='left', padx=80, pady=10)
        ttk.Button(text='取消', command=cls.cancel, **btn_style).pack(side='right', padx=80, pady=10)

    @classmethod
    def confirm(cls):
        data = {}
        data['tool_alias'] = cls.tool_alias.get()
        data['tool_version'] = cls.tool_version.get()
        data['log_level'] = cls.log_level.get()
        data['login_count_limit'] = int(cls.count_limit.get())
        data['retry_times'] = int(cls.retry_times.get())
        data['refresh_json_period'] = int(cls.refresh_json.get())

        data['passwords'] = {}
        data['passwords']['username'] = cls.user_name.get()
        data['passwords']['userpassword'] = cls.user_password.get()
        data['passwords']['rootpassword'] = cls.root_password.get()
        data['server_home'] = cls.server_home.get()
        data['keepalive_period'] = int(cls.keepalive_period.get())
        view_gate.update_settings_data.set_data(data)
        WidgetTip.info('设置成功')
        cls.cancel()

    @classmethod
    def cancel(cls):
        cls.top.destroy()
        cls.is_showing = False
        del cls.top
        del cls.settings


