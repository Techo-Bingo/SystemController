# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import ttk
import my_global as Global
from my_base import Pager
from my_viewutil import ToolTips, WinMsg
from my_module import ProgressBar
from my_handler import PageHandler


class TimezonePage(Pager):

    def __init__(self, master, width, height, shell, ip_list, options):
        self.master = master
        self.width = width
        self.height = height
        self.shell = shell
        self.ip_list = ip_list
        self.options = options
        self.row = 5
        self.column = 3
        # 用来保存排列的combox实例
        self.subcmb_list = self.get_struct_array()
        # 用来保存各个combox中显示的值
        self.cmbval_list = self.get_struct_array()
        self.label_list = self.get_struct_array()
        self.opts_dict = {}
        self.progress = {}

    def stepper(self):
        self.pack_frame()

    def pack_frame(self):
        self.init_combox_data()
        self.create_grid()
        self.init_display()

    def init_combox_data(self):
        self.cmbval_list[0][0] = self.get_zonearea_tup()
        self.cmbval_list[0][1] = self.get_month_tup()
        self.cmbval_list[0][2] = self.get_month_tup()
        self.cmbval_list[1][0] = ('YES', 'NO')
        self.cmbval_list[1][1] = self.get_month_day_tup()
        self.cmbval_list[1][2] = self.get_month_day_tup()
        self.cmbval_list[2][0] = ('DATE', 'WEEK')
        self.cmbval_list[2][1] = self.get_weekseq_tup()
        self.cmbval_list[2][2] = self.get_weekseq_tup()
        self.cmbval_list[3][0] = ('DATE', 'WEEK')
        self.cmbval_list[3][1] = self.get_week_tup()
        self.cmbval_list[3][2] = self.get_week_tup()
        self.cmbval_list[4][0] = self.get_offset_time_tup()
        self.cmbval_list[4][1] = self.get_day_hour_tup()
        self.cmbval_list[4][2] = self.get_min_second_tup()
        self.cmbval_list[4][3] = self.get_min_second_tup()
        self.cmbval_list[4][4] = self.get_day_hour_tup()
        self.cmbval_list[4][5] = self.get_min_second_tup()
        self.cmbval_list[4][6] = self.get_min_second_tup()

    def create_grid(self):
        bg_color = 'Snow'
        shw_fm = tk.LabelFrame(self.frame, width=self.width, text='当前状态')
        opt_fm = tk.LabelFrame(self.frame, bg=bg_color, width=self.width)
        opr_fm = tk.Frame(self.frame, width=self.width)
        btn_fm = tk.Frame(opr_fm, width=self.width/3, height=self.height/5*2)
        ips_fm = tk.LabelFrame(opr_fm, width=self.width/3*2, height=self.height/5*2)
        shw_fm.pack(fill='x', padx=10, pady=5)
        opt_fm.pack(fill='x', padx=10, pady=5)
        opr_fm.pack(fill='x', padx=10)
        ips_fm.pack(fill='both', side='left')
        btn_fm.pack(fill='x', side='left', padx=40)
        for ip in self.ip_list:
            status_lab = tk.Label(shw_fm, text="%s: " % ip, anchor='w')
            status_lab.pack(fill='x')
            self.get_current_zoneinfo(ip, status_lab)
        for x in range(self.row):
            for y in range(self.column):
                fm = tk.Frame(opt_fm, bg=bg_color, width=self.width/self.column-1, height=self.height/self.row-1)
                fm.grid(row=x, column=y, padx=2, sticky='e')
                # 两个时间的，需要特殊处理
                if x == self.row-1 and y in [self.column-2, self.column-1]:
                    lab = tk.Label(fm, bg=bg_color, text=self.get_labname(x, y), font=(Global.G_FONT, 10))
                    lab.pack(side='left')
                    self.label_list[x][y] = lab
                    # 由于y在 x=row-1的时候，相对以前多加了两列，所以下次y要多加2才是正确的数组位置
                    tmp_y = y
                    if y == self.column-1:
                        tmp_y = y+2
                    subfm = tk.Frame(fm, bg=bg_color, width=self.width/self.column/2-1, height=self.height/self.row/2-1)
                    subfm.pack(side='right')
                    for i in range(3):
                        combox_var = tk.StringVar()
                        subcmb = ttk.Combobox(subfm, textvariable=combox_var, width=2)
                        subcmb["values"] = self.cmbval_list[x][tmp_y+i]
                        subcmb.current(0)
                        subcmb["state"] = "readonly"
                        subcmb.bind("<<ComboboxSelected>>", func=self.handler_adaptor(self.choose_opt, cmb=subcmb, x=x, y=tmp_y+i))
                        subcmb.pack(side='left')
                        self.subcmb_list[x][tmp_y+i] = subcmb
                        if i != 2:
                            tk.Label(subfm, text=':').pack(side='left')
                else:
                    lab = tk.Label(fm, bg=bg_color, text=self.get_labname(x, y), font=(Global.G_FONT, 10))
                    lab.pack(side='left')
                    self.label_list[x][y] = lab
                    combox_var = tk.StringVar()
                    cmb = ttk.Combobox(fm, textvariable=combox_var, width=14)
                    cmb["values"] = self.cmbval_list[x][y]
                    cmb.current(0)
                    cmb["state"] = "readonly"
                    cmb.bind("<<ComboboxSelected>>", func=self.handler_adaptor(self.choose_opt, cmb=cmb, x=x, y=y))
                    cmb.pack(side='right', padx=4)
                    # 子窗体中的combox存入二位数组
                    self.subcmb_list[x][y] = cmb
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

    def get_current_zoneinfo(self, ip, master):
        def callback(info):
            master['text'] = "%s: %s" % (ip, info)
        PageHandler.execute_showing_start(callback, ip, self.shell, 'ENTER')

    def start_execute(self, var_list):
        not_set = self.exist_not_set_combox()
        if not_set:
            WinMsg.warn("请设置夏令时参数:%s" % not_set[0])
            return
        select_ip, index = [], 0
        for v in var_list:
            if int(v.get()):
                select_ip.append(self.ip_list[index])
            index += 1
        if not select_ip:
            WinMsg.warn("请勾选IP地址")
            return
        PageHandler.execute_download_start(self.callback, select_ip, self.shell, self.options_combine())

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

    def get_labname(self, x, y):
        return [['TimeZone\n时区', 'Start month\n开始月份', 'End month\n结束月份'],
                ['DaylightSave\n夏令时', 'Start date\n开始日期', 'End date\n结束日期'],
                ['StartType\n开始类型', 'Start week sequence\n开始星期序列', 'End week sequence\n结束星期序列'],
                ['EndType\n结束类型', 'Start week\n开始星期', 'End week\n结束星期'],
                ['AdjustMethod\n时间偏移量', 'Start time\n开始时间', 'End time\n结束时间']][x][y]

    def get_abbre_opts(self, x, y):
        return [['ZONET', 'SMONTH', 'EMONTH'],
                ['DST', 'SDAY', 'EDAY'],
                ['SMODE', 'SWSEQ', 'EWSEQ'],
                ['EMODE', 'SWEEK', 'EWEEK'],
                ['METHOD', 'STIMEH', 'STIMEM', 'STIMES', 'ETIMEH', 'ETIMEM', 'ETIMES']][x][y]

    def get_index_byname(self, name):
        """ 根据传入的option的name，返回所在二维列表中的位置 """
        namelist = [['ZONET', 'SMONTH', 'EMONTH'],
                    ['DST', 'SDAY', 'EDAY'],
                    ['SMODE', 'SWSEQ', 'EWSEQ'],
                    ['EMODE', 'SWEEK', 'EWEEK'],
                    ['METHOD', 'STIMEH', 'STIMEM', 'STIMES', 'ETIMEH', 'ETIMEM', 'ETIMES']]
        x = 0
        for sublist in namelist:
            x += 1
            y = 0
            for nm in sublist:
                y += 1
                if name == nm:
                    return [x-1, y-1]
        return []

    def exist_not_set_combox(self):
        """ 根据不同设置类型的key最小集，判断是否还有没有设置的combox """
        scene1 = ['ZONET','DST']
        scene2 = ['ZONET','DST','SMODE','SMONTH','SDAY','STIMES','STIMEM','STIMEH','EMODE','EMONTH','EDAY','ETIMES','ETIMEM','ETIMEH','METHOD']
        scene3 = ['ZONET','DST','SMODE','SMONTH','SDAY','STIMES','STIMEM','STIMEH','EMODE','EMONTH','EWSEQ','EWEEK','ETIMES','ETIMEM','ETIMEH','METHOD']
        scene4 = ['ZONET','DST','SMODE','SMONTH','SWSEQ','SWEEK','STIMES','STIMEM','STIMEH','EMODE','EMONTH','EDAY','ETIMES','ETIMEM','ETIMEH','METHOD']
        scene5 = ['ZONET','DST','SMODE','SMONTH','SWSEQ','SWEEK','STIMES','STIMEM','STIMEH','EMODE','EMONTH','EWSEQ','EWEEK','ETIMES','ETIMEM','ETIMEH','METHOD']
        if 'DST' not in self.opts_dict:
            return ['DST']
        elif 'ZONET' not in self.opts_dict:
            return ['ZONET']
        elif self.opts_dict['DST'] == 'NO':
            return []
        elif 'SMODE' not in self.opts_dict:
            return ['SMODE']
        elif 'EMODE' not in self.opts_dict:
            return ['EMODE']
        elif 'METHOD' not in self.opts_dict:
            return ['METHOD']
        tmplist = []
        if self.opts_dict['SMODE'] == 'DATE' and self.opts_dict['EMODE'] == 'DATE':
            tmplist = scene2
        elif self.opts_dict['SMODE'] == 'DATE' and self.opts_dict['EMODE'] == 'WEEK':
            tmplist = scene3
        elif self.opts_dict['SMODE'] == 'WEEK' and self.opts_dict['EMODE'] == 'DATE':
            tmplist = scene4
        elif self.opts_dict['SMODE'] == 'WEEK' and self.opts_dict['EMODE'] == 'WEEK':
            tmplist = scene5
        outlist = []
        for i in tmplist:
            if i not in self.opts_dict:
                if i in ['STIMES', 'STIMEH', 'STIMEM'] and 'STIME' in self.opts_dict:continue
                if i in ['ETIMES', 'ETIMEH', 'ETIMEM'] and 'ETIME' in self.opts_dict:continue
                outlist.append(i)
        return outlist

    def get_index_list(self,index=None):
        tmp_list = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2],[3,0],[3,1],[3,2],[4,0],[4,1],[4,2],[4,3],[4,4],[4,5],[4,6]]
        if index:
            return tmp_list[index]
        return tmp_list

    def get_day_list(self,month):
        """
        根据月份返回天数
        夏令时不能设在闰年的2月29
        所以2分返回28天
        """
        month = int(month)
        if month == 2:
            return 28
        elif month in [4, 6, 9, 11]:
            return 30
        elif month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        else:
            return -1

    def get_struct_array(self):
        return [['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', '', '', '', '', '']]

    def get_offset_time_tup(self,forfind=False):
        """ 获取夏令时偏移量的元组 """
        a = tuple(range(1, 121))
        b = tuple(range(-120, 0))
        tup = a + b
        if forfind:
            if forfind not in tup:return -1
            return tup.index(forfind)
        return tup

    def get_min_second_tup(self):
        """ 获取一小时的分钟或一分钟的秒数的元组 """
        return tuple(range(60))

    def get_day_hour_tup(self):
        """ 获取一天中的各个小时的元组 """
        return tuple(range(24))

    def get_month_day_tup(self):
        """ 获取一个月的天数的元组,最大的31天 """
        return tuple(range(1,32))

    def get_month_tup(self,forfind=False):
        tup = ('一月(Jan)', '二月(Feb)', '三月(Mar)', '四月(Apr)', '五月(May)', '六月(Jun)',
               '七月(Jul)', '八月(Aug)', '九月(Sep)', '十月(Oct)', '十一月(Nov)', '十二月(Dec)')
        if forfind:
            if forfind not in tup:return -1
            # 加1,是因为返回的是月份数字
            return tup.index(forfind)+1
        return tup

    def get_zonearea_tup(self,forfind=False):
        tup = ('GMT+14:00', 'GMT+13:00', 'GMT+12:45', 'GMT+12:00', 'GMT+11:30', 'GMT+11:00', 'GMT+10:30', 'GMT+10:00',
               'GMT+09:30', 'GMT+09:00', 'GMT+08:45', 'GMT+08:00', 'GMT+07:00', 'GMT+06:30', 'GMT+06:00', 'GMT+05:30',
               'GMT+05:00', 'GMT+04:30', 'GMT+04:00', 'GMT+03:30', 'GMT+03:00', 'GMT+02:00', 'GMT+01:00', 'GMT+00:00',
               'GMT-01:00', 'GMT-02:00', 'GMT-03:00', 'GMT-03:30', 'GMT-04:00', 'GMT-04:30', 'GMT-05:00', 'GMT-06:00',
               'GMT-07:00', 'GMT-07:30', 'GMT-08:00', 'GMT-08:30', 'GMT-09:00', 'GMT-09:30', 'GMT-10:00', 'GMT-10:30',
               'GMT-11:00', 'GMT-12:00')
        if forfind:
            if forfind not in tup:return -1
            ''' 这里不加1，是因为这里跟数字没有关系，只是获取索引 '''
            return tup.index(forfind)
        return tup

    def get_weekseq_tup(self,forfind=False):
        tup = ('第一个', '第二个', '第三个', '第四个', '最后一个')
        if forfind:
            if forfind not in tup:return -1
            return tup.index(forfind)+1
        return tup

    def get_week_tup(self,forfind=False):
        tup = ('星期一(Mon)', '星期二(Tues)', '星期三(Wed)', '星期四(Thur)', '星期五(Fri)', '星期六(Sat)', '星期日(Sun)')
        if forfind:
            if forfind not in tup:return -1
            return tup.index(forfind)+1
        return tup

    def handler_adaptor(self, fun,  **kwds):
        """ 事件处理函数的适配器，相当于中介 """
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

    def check_limit_dependence(self, key, value):
        if key not in ['SDAY', 'EDAY', 'SMONTH', 'EMONTH']:
            return True
        if key == 'SDAY':
            if 'SMONTH' not in self.opts_dict:
                return True
            if int(value) < 28:
                return True
            month = int(self.opts_dict['SMONTH'])
            if month == 2 and int(value) > 28:
                WinMsg.error('开始月份为2月时，日期不能设置大于28号！')
                self.reset_combox_list([[1, 1]])
                self.pop_opts_dict('SDAY')
                return False
            elif month in [4, 6, 9, 11] and int(value) > 30:
                WinMsg.error('开始月份为%s月时，日期不能设置大于30号！' % month)
                self.reset_combox_list([[1, 1]])
                self.pop_opts_dict('SDAY')
                return False
        elif key == 'EDAY':
            if 'EMONTH' not in self.opts_dict:
                return True
            if int(value) < 28:
                return True
            month = int(self.opts_dict['EMONTH'])
            if month == 2 and int(value) > 28:
                WinMsg.error('结束月份为2月时，日期不能设置大于28号！')
                self.reset_combox_list([[1, 2]])
                self.pop_opts_dict('EDAY')
                return False
            elif month in [4,6,9,11] and int(value) > 30:
                WinMsg.error('结束月份为%s月时，日期不能设置大于30号！' % month)
                self.reset_combox_list([[1, 2]])
                self.pop_opts_dict('EDAY')
                return False
        elif key == 'SMONTH':
            if 'SDAY' not in self.opts_dict:
                return True
            day = int(self.opts_dict['SDAY'])
            if int(value) == 2 and day > 28:
                WinMsg.error('开始月份为2月时，日期不能设置大于28号！')
                self.reset_combox_list([[0, 1]])
                self.pop_opts_dict('SMONTH')
                return False
            elif int(value) in [4,6,9,11] and day > 30:
                WinMsg.error('开始月份为%s月时，日期不能设置大于30号！' % value)
                self.reset_combox_list([[0, 1]])
                self.pop_opts_dict('SMONTH')
                return False
        elif key == 'EMONTH':
            if 'EDAY' not in self.opts_dict:
                return True
            day = int(self.opts_dict['EDAY'])
            if int(value) == 2 and day > 28:
                WinMsg.error('开始月份为2月时，日期不能设置大于28号！')
                self.reset_combox_list([[0, 2]])
                self.pop_opts_dict('EMONTH')
                return False
            elif int(value) in [4, 6, 9, 11] and day > 30:
                WinMsg.error('开始月份为%s月时，日期不能设置大于30号！' % value)
                self.reset_combox_list([[0, 2]])
                self.pop_opts_dict('EMONTH')
                return False
        return True

    def choose_opt(self, event, cmb, x, y):
        ''' 下拉框点击事件 '''
        optname = self.get_abbre_opts(x, y)
        optval = cmb.get()
        '''根据选择的类型做出按钮的限制'''
        if optname in ['DST', 'SMODE', 'EMODE']:
            self.display_diff_mode(optname, optval)
        '''组合成脚本所需要的形式'''
        if optname == 'ZONET':
            optval = optval.replace(':', '').replace('GMT', '')
        elif optname in ['SMONTH', 'EMONTH']:
            optval = self.get_month_tup(optval)
        elif optname in ['SWSEQ', 'EWSEQ']:
            optval = self.get_weekseq_tup(optval)
        elif optname in ['SWEEK', 'EWEEK']:
            optval = self.get_week_tup(optval)
        elif optname in ['STIMEH', 'STIMEM', 'STIMES']:
            ''' 通过subcmb_list中保存的实例直接获取3个时间框的值 '''
            h = self.subcmb_list[x][1].get()
            m = self.subcmb_list[x][2].get()
            s = self.subcmb_list[x][3].get()
            if not h:h = 0
            if not m:m = 0
            if not s:s = 0
            tmpval = '%02d:%02d:%02d' % (int(h), int(m), int(s))
            optname = 'STIME'
            optval = tmpval
        elif optname in ['ETIMEH', 'ETIMEM', 'ETIMES']:
            h = self.subcmb_list[x][4].get()
            m = self.subcmb_list[x][5].get()
            s = self.subcmb_list[x][6].get()
            if not h:h = 0
            if not m:m = 0
            if not s:s = 0
            tmpval = '%02d:%02d:%02d'%(int(h), int(m), int(s))
            optname = 'ETIME'
            optval = tmpval
        ''' 一些条件判断，比如2月不能设置大于28号；4,6,9,11月不能设置31号 '''
        if self.check_limit_dependence(optname, optval):
            self.opts_dict[optname] = optval
        ToolTips._infowin_msg(self.options_combine())

    def display_diff_mode(self, key, val):
        """ 无夏令时 """
        disable_list = self.get_index_list()
        disable_list.remove([0, 0])
        disable_list.remove([1, 0])
        if key == 'DST':
            if val != 'NO':
                # DST为YES时，只继续开放模式和偏移
                open_list = [[2, 0], [3, 0], [4, 0]]
                disable_list = []
            else:
                # 如果之前显示器上有其他参数，清除掉
                open_list = []
                self.remove_optsdict_key(['ZONET', 'DST'], True)
        elif key == 'SMODE':
            open_list = [[0, 1], [4, 1], [4, 2], [4, 3]]
            if val == 'DATE':
                open_list.append([1, 1])
                disable_list = [[2, 1], [3, 1]]
                self.remove_optsdict_key(['SWSEQ', 'SWEEK'])
            elif val == 'WEEK':
                open_list.append([2, 1])
                open_list.append([3, 1])
                disable_list = [[1, 1]]
                self.remove_optsdict_key(['SDAY'])
            else:
                return
        elif key == 'EMODE':
            open_list = [[0, 2], [4, 4], [4, 5], [4, 6]]
            if val == 'DATE':
                open_list.append([1, 2])
                disable_list = [[2, 2], [3, 2]]
                self.remove_optsdict_key(['EWSEQ', 'EWEEK'])
            elif val == 'WEEK':
                open_list.append([2, 2])
                open_list.append([3, 2])
                disable_list = [[1, 2]]
                self.remove_optsdict_key(['EDAY'])
            else:
                return
        else:
            return
        self.reset_combox_list(open_list)
        self.disable_combox_list(disable_list)

    def remove_optsdict_key(self, inlist, reverse=False):
        '''
        reverse=True时，删除opts_dict中除去inlist之外的键值
        否则删除inlist
        '''
        if not inlist:
            return
        rmlist = inlist
        if reverse:
            tmp_list = []
            for i in self.opts_dict:
                if i not in inlist:
                    tmp_list.append(i)
            rmlist = tmp_list
        for i in rmlist:
            if i in self.opts_dict:
                self.opts_dict.pop(i)

    def pop_opts_dict(self, which):
        if which in self.opts_dict:
            self.opts_dict.pop(which)

    def options_combine(self):
        opts_str = ""
        for k,v in sorted(self.opts_dict.items()):
            if not len(opts_str):
                opts_str = "%s=%s" % (k, v)
            else:
                opts_str = "%s=%s," % (k, v) + opts_str
        return opts_str

    def init_display(self):
        """ 初始化combox显示 """
        disable_list = self.get_index_list()
        disable_list.remove([0, 0])
        disable_list.remove([1, 0])
        self.disable_combox_list(disable_list)

    def onoff_label_view(self, tp, x, y):
        lab_y = y
        if x == self.row-1:
            if y in [1, 2, 3]:
                lab_y = 1
            elif y in [4, 5, 6]:
                lab_y = 2
        color = 'Gray' if tp == 'OFF' else 'black'
        self.label_list[x][lab_y]['fg'] = color

    def disable_combox_list(self, inlist):
        for x, y in inlist:
            self.onoff_label_view('OFF', x, y)
            self.subcmb_list[x][y].set('')
            self.subcmb_list[x][y]['state'] = 'disabled'

    def reset_combox_list(self, inlist):
        for x, y in inlist:
            self.onoff_label_view('ON', x, y)
            self.subcmb_list[x][y].set('')
            self.subcmb_list[x][y]['state'] = 'readonly'

    def set_combox_value(self, x, y, index):
        self.onoff_label_view('ON', x, y)
        self.subcmb_list[x][y].current(index)
        self.subcmb_list[x][y]['state'] = 'readonly'



    """
    def check_preset_options(self,presetpath):
        '''检查导入的配置文件的参数是否正确'''
        if not presetpath:return False
        '''
        改：2019-01-22
            加个保护，如果是一个非常大的非法的文件，cat_file中的f.read()可能会造成内存撑爆
            规则文件目前肯定不会超过1024字节，用 read_file_1024 获取一次next即可
        '''
        #print CommonFunc.get_nowtime_str()
        #opts_str = CommonFunc.cat_file(presetpath).replace('\n','').replace(' ','')
        opts_str = CommonFunc.read_file_1024(presetpath).next().replace('\n','').replace(' ','')
        #print CommonFunc.get_nowtime_str()
        if not opts_str:
            CommonFunc.windows_info('导入的规则文件内容为空','error')
            return False
        try:
            optsdict = {i.split('=')[0]:i.split('=')[1] for i in opts_str.split(',')}
        except:
            CommonFunc.windows_info('导入的规则文件内容不合法（格式不正确）','error')
            return False
        '''值不能为空'''	
        for k,v in optsdict.items():
            if not v:
                CommonFunc.windows_info('导入的规则文件内容不合法（存在空规则）','error')
                return False
        '''非法值和必要规则检查'''
        para_keylist = optsdict.keys()
        all_optskey = ['ZONET','DST','SMODE','SMONTH','SWSEQ','SWEEK','SDAY','STIME','EMODE','EMONTH','EWSEQ','EWEEK','EDAY','ETIME','METHOD']
        if not CommonFunc.is_sublist(para_keylist,all_optskey):
            CommonFunc.windows_info('导入的规则文件中存在其他非法数据','error')
            return False
        if not CommonFunc.is_sublist(['ZONET','DST'],para_keylist):
            CommonFunc.windows_info("导入的规则文件中缺少必要的规则（'时区'或'夏令时'）",'error')
            return False
        '''时区规则检查'''
        zone_area = optsdict['ZONET']
        try:
            # 只允许 '+' 或 '-'开头
            if list(zone_area)[0] in ['+','-']: # eg: -0800 or +0800
                if len(zone_area) != 5:raise
                if -1400 <= int(zone_area[1:]) <= 1400:
                    optsdict['ZONET'] = "GMT%s:%s"%(zone_area[:3],zone_area[3:])
                else:
                    raise
            else:
                raise
        except:
            CommonFunc.windows_info("导入的规则文件中'时区'规则非法",'error')
            return False
        '''夏令时值检查'''
        if optsdict['DST'] == 'NO':
            return optsdict
        elif optsdict['DST'] != 'YES':
            CommonFunc.windows_info("导入的规则文件中'夏令时'的值非法",'error')
            return False
        '''需要根据开始时间类型和结束时间类型，确定必要的规则最小集'''
        if 'SMODE' not in para_keylist or 'EMODE' not in para_keylist:
            CommonFunc.windows_info("导入的规则文件中缺少必要的规则（'开始类型'或'结束类型'）",'error')
            return False
        pa,pb = optsdict['SMODE'],optsdict['EMODE']
        min_optskey = all_optskey
        if pa == 'DATE' and pb == 'DATE':
            min_optskey.remove('SWSEQ')
            min_optskey.remove('SWEEK')
            min_optskey.remove('EWSEQ')
            min_optskey.remove('EWEEK')
            date_type = 'SDAY+EDAY'
        elif pa == 'DATE' and pb == 'WEEK':
            min_optskey.remove('SWSEQ')
            min_optskey.remove('SWEEK')
            min_optskey.remove('EDAY')
            date_type = 'SDAY+EWEEK'
        elif pa == 'WEEK' and pb == 'DATE':
            min_optskey.remove('SDAY')
            min_optskey.remove('EWSEQ')
            min_optskey.remove('EWEEK')
            date_type = 'SWEEK+EDAY'
        elif pa == 'WEEK' and pb == 'WEEK':
            min_optskey.remove('SDAY')
            min_optskey.remove('EDAY')
            date_type = 'SWEEK+EWEEK'
        else:
            CommonFunc.windows_info("导入的规则文件中'开始类型'或'结束类型'的值非法",'error')
            return False
        '''判断参数options的key是否包含最小集'''
        if not CommonFunc.is_sublist(min_optskey,para_keylist):
            less_list = []
            for i in min_optskey:
                if i not in para_keylist:
                    less_list.append(i)
            CommonFunc.windows_info("导入的规则文件中缺少必要的规则（%s）"%(less_list),'error')
            return False
        '''严格判断是否就是必须的最小集,一定要排序 !'''
        if sorted(min_optskey)!= sorted(para_keylist):
            less_list = []
            for i in para_keylist:
                if i not in min_optskey:
                    less_list.append(i)
                    optsdict.pop(i)
            CommonFunc.windows_info("导入的规则文件中含有不必要的规则\n已排除 ！（%s）"%(less_list),'warn')
            CommonFunc.tell_info("导入的规则文件中含有不必要的规则，已排除 ！（%s）"%(less_list))
        '''检查 STIME和ETIME的格式是否非法'''
        s_time,e_time = optsdict['STIME'],optsdict['ETIME']
        try:
            # 小时
            if (0 <= int(s_time.split(':')[0]) <= 23) and (0 <= int(e_time.split(':')[0]) <= 23):
                pass
            else:
                raise
            # 分钟
            if (0 <= int(s_time.split(':')[1]) <= 59) and (0 <= int(e_time.split(':')[1]) <= 59):
                pass
            else:
                raise
            # 秒
            if (0 <= int(s_time.split(':')[2]) <= 59) and (0 <= int(e_time.split(':')[2]) <= 59):
                pass
            else:
                raise
        except:
            CommonFunc.windows_info("导入的规则文件中'开始时间'或'结束时间'的值非法",'error')
            return False
        '''检查月份值范围'''
        try:
            s_month,e_month = int(optsdict['SMONTH']),int(optsdict['EMONTH'])
            if 1 <= s_month <= 12 and 1 <= e_month <= 12:
                pass
            else:
                raise
        except:
            CommonFunc.windows_info("导入的规则文件中'开始月份'或'结束月份'的值非法",'error')
            return False
        '''检查日期值范围'''
        # 开始时间为日期类型
        if 'SWEEK' not in min_optskey:
            try:
                s_day = int(optsdict['SDAY'])
                if 1 <= s_day <= 31:
                    pass
                else:
                    raise 
            except:
                CommonFunc.windows_info("导入的规则文件中'开始日期'的值非法",'error')
                return False
            if s_month == 2 and s_day > 28:
                CommonFunc.windows_info("导入的规则文件中'开始日期'的值非法（2月不能设置大于28号开始夏令时）",'error')
                return False
            elif s_month in [4,6,9,11] and s_day >= 31:
                CommonFunc.windows_info("导入的规则文件中'开始日期'的值非法（%s月不能设置大于30号开始夏令时）"%(s_month),'error')
                return False
        # 结束时间为日期类型
        if 'EWEEK' not in min_optskey:
            try:
                e_day = int(optsdict['EDAY'])
                if 1 <= e_day <= 31:
                    pass
                else:
                    raise 
            except:
                CommonFunc.windows_info("导入的规则文件中'结束日期'的值非法",'error')
                return False
            if e_month == 2 and e_day > 28:
                CommonFunc.windows_info("导入的规则文件中'结束日期'的值非法（2月不能设置大于28号开始夏令时）",'error')
                return False
            elif e_month in [4,6,9,11] and e_day >= 31:
                CommonFunc.windows_info("导入的规则文件中'结束日期'的值非法（%s月不能设置大于30号开始夏令时）"%(e_month),'error')
                return False
        # 开始时间为星期类型
        if 'SDAY' not in min_optskey:
            try:
                s_wseq = int(optsdict['SWSEQ'])
                s_week = int(optsdict['SWEEK'])
                if 1 <= s_wseq <= 5 and 1 <= s_week <= 7:
                    pass
                else:
                    raise
            except:
                CommonFunc.windows_info("导入的规则文件中'开始星期序列'或'开始星期'的值非法",'error')
                return False
        # 结束时间为星期类型
        if 'EDAY' not in min_optskey:
            try:
                e_wseq = int(optsdict['EWSEQ'])
                e_week = int(optsdict['EWEEK'])
                if 1 <= e_wseq <= 5 and 1 <= e_week <= 7:
                    pass
                else:
                    raise
            except:
                CommonFunc.windows_info("导入的规则文件中'结束星期序列'或'结束星期'的值非法",'error')
                return False
        '''判断夏令时偏移'''
        try:
            offset = int(optsdict['METHOD'])
            if 1 <= offset <= 120 or -120 <= offset <= -1:
                pass
            else:
                raise
        except:
            CommonFunc.windows_info("导入的规则文件中'时间偏移量'的值非法",'error')
            return False
        '''一切OK'''
        return optsdict


    def display_combox_by_optsdict(self,optsdict):
        '''到此处时，数值都是合法的，不必校验'''
        #print optsdict
        for which in optsdict:
            if which == 'ZONET':
                index = self.get_zonearea_tup(optsdict['ZONET'])
                x,y = 0,0  # self.get_index_byname('ZONET')
            elif which == 'DST':
                if optsdict['DST'] == 'NO':
                    x,y,index = 1,0,1
                else:
                    x,y,index = 1,0,0
            elif which == 'SMODE':
                if optsdict['SMODE'] == 'DATE':
                    x,y,index = 2,0,0
                else:
                    x,y,index = 2,0,1
            elif which == 'EMODE':
                if optsdict['EMODE'] == 'DATE':
                    x,y,index = 3,0,0
                else:
                    x,y,index = 3,0,1
            elif which == 'METHOD':
                index = self.get_offset_time_tup(int(optsdict['METHOD']))
                x,y = 4,0
            elif which == 'SMONTH':
                index = int(optsdict['SMONTH'])-1
                x,y = 0,1
            elif which == 'SDAY':
                index = int(optsdict['SDAY'])-1
                x,y = 1,1
            elif which == 'SWSEQ':
                index = int(optsdict['SWSEQ'])-1
                x,y = 2,1
            elif which == 'SWEEK':
                index = int(optsdict['SWEEK'])-1
                x,y = 3,1
            elif which == 'EMONTH':
                index = int(optsdict['EMONTH'])-1
                x,y = 0,2
            elif which == 'EDAY':
                index = int(optsdict['EDAY'])-1
                x,y = 1,2
            elif which == 'EWSEQ':
                index = int(optsdict['EWSEQ'])-1
                x,y = 2,2
            elif which == 'EWEEK':
                index = int(optsdict['EWEEK'])-1
                x,y = 3,2
            elif which == 'STIME':
                h_index = int(optsdict['STIME'].split(':')[0])
                m_index = int(optsdict['STIME'].split(':')[1])
                s_index = int(optsdict['STIME'].split(':')[2])
                self.set_combox_value(4,1,h_index)
                self.set_combox_value(4,2,m_index)
                self.set_combox_value(4,3,s_index)
                continue
            elif which == 'ETIME':
                h_index = int(optsdict['ETIME'].split(':')[0])
                m_index = int(optsdict['ETIME'].split(':')[1])
                s_index = int(optsdict['ETIME'].split(':')[2])
                self.set_combox_value(4,4,h_index)
                self.set_combox_value(4,5,m_index)
                self.set_combox_value(4,6,s_index)
                continue
        
            if index < 0:
                CommonFunc.windows_info("导入的规则文件中'%s'的值不在支持的范围中"%(which),'error')
                return False
            self.set_combox_value(x,y,index)
        # 注:for循环外
        '''更新自身的参数字典'''
        self.opts_dict = optsdict
        self.opts_dict['ZONET'] = self.opts_dict['ZONET'].replace(':','').replace('GMT','')
    """



