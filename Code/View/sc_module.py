# -*- coding: UTF-8 -*-

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import ImageGrab
from threading import Lock
from collections import OrderedDict
from Utils.sc_func import Common
from View.sc_global import Global
from View.Datamation.sc_provide import view_gate

def center_window(master, width_flag=0.5, height_flag=0.382):   # 0.382
    master.withdraw()
    master.update()
    current_window_width = master.winfo_width()
    current_window_height = master.winfo_height()
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    suitable_location_x = int((screen_width - current_window_width) * width_flag)
    suitable_location_y = int((screen_height - current_window_height) * height_flag)
    master.geometry('+{}+{}'.format(suitable_location_x, suitable_location_y))
    master.deiconify()

class WidgetTip:
    _toplevel = None

    @classmethod
    def info(cls, info):
        messagebox.showinfo('提示', info)

    @classmethod
    def error(cls, info):
        messagebox.showerror('错误', info)

    @classmethod
    def ask(cls, info):
        return messagebox.askokcancel('请确认', info)

    @classmethod
    def warn(cls, info):
        messagebox.showwarning('警告', info)

    @classmethod
    def enter_tips(cls, widget, text, width=20, height=20):
        def enter(event):
            cls._enter_tip(widget, text, width, height)
        def leave(event):
            cls._hide_tip()
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)

    @classmethod
    def _enter_tip(cls, widget, text, width, height):
        if cls._toplevel:
            return
        x, y, cx, cy = widget.bbox("insert")
        x = x + widget.winfo_rootx() + width
        y = y + widget.winfo_rooty() - height  #+ cy
        cls._toplevel = tw = tk.Toplevel(widget)
        tw.overrideredirect(1)
        tw.wm_attributes('-topmost', 1)
        tw.geometry("+%d+%d" % (x, y))
        tk.Label(tw,
                 text = text,
                 justify = 'left',
                 background = "#ffffe0",
                 relief = tk.SOLID,
                 borderwidth = 1,
                 font=("tahoma", "8")
                 ).pack(ipadx=1)

    @classmethod
    def _hide_tip(cls):
        if cls._toplevel:
            cls._toplevel.destroy()
            cls._toplevel = None

class SubLogin(object):
    """ 登录子板块 """
    def __init__(self, master, prefer_ips, passwords, store):
        self.ip_en = None
        self.user_en = None
        self.upwd_en = None
        self.rpwd_en = None
        self.tip_lab = None
        self.pack(master, prefer_ips, passwords, store)
        self.see_password(False)

    def destroy(self):
        del self

    def pack(self, master, prefer_ips, passwords, store):
        def destroy():
            tip_lab.grid_remove()
            ip_en.grid_remove()
            user_en.grid_remove()
            upwd_en.grid_remove()
            rpwd_en.grid_remove()
            del_btn.grid_remove()
            store.remove(self)
            self.destroy()
        def bind_tips():
            WidgetTip.enter_tips(ip_en, 'IP地址')
            WidgetTip.enter_tips(user_en, '用户名')
            WidgetTip.enter_tips(upwd_en, '用户密码')
            WidgetTip.enter_tips(rpwd_en, 'root密码')
            WidgetTip.enter_tips(del_btn, '删除该登录栏')
        def store_me():
            self.ip_en = ip_en
            self.user_en = user_en
            self.upwd_en = upwd_en
            self.rpwd_en = rpwd_en
            self.tip_lab = tip_lab
            store.append(self)
        def set_password():
            user_en.insert(0, passwords[0])
            upwd_en.insert(0, passwords[1])
            rpwd_en.insert(0, passwords[2])
        entry_style = {'master': master,
                       'font': (Global.G_DEFAULT_FONT, 11)}
        tip_lab = tk.Label(master, text='●', font=(Global.G_DEFAULT_FONT, 12), fg=Global.G_TIP_FG_COLOR['DEFAULT'])
        ip_en = ttk.Combobox(width=14, values=prefer_ips, **entry_style)
        if prefer_ips:
            ip_en.current(0)
        user_en = ttk.Entry(width=13, **entry_style)
        upwd_en = ttk.Entry(width=13, **entry_style)
        rpwd_en = ttk.Entry(width=13, **entry_style)
        del_btn = tk.Button(master, text='×', font=(Global.G_DEFAULT_FONT, 13, 'bold'), bd=0, command=destroy)
        index = len(store)
        grid_style = {'row': index,
                      'padx': 2,
                      'pady': 6,
                      'ipady': 2}
        tip_lab.grid(row=index, column=0)
        ip_en.grid(column=1, **grid_style)
        user_en.grid(column=2, **grid_style)
        upwd_en.grid(column=3, **grid_style)
        rpwd_en.grid(column=4, **grid_style)
        if index != 0:
            del_btn.grid(row=index, column=5)
        set_password()
        bind_tips()
        store_me()

    def get_inputs(self):
        return [self.ip_en.get(),
                self.user_en.get(),
                self.upwd_en.get(),
                self.rpwd_en.get()]

    def see_password(self, turn):
        if turn:
            self.upwd_en['show'] = ''
            self.rpwd_en['show'] = ''
        else:
            self.upwd_en['show'] = '*'
            self.rpwd_en['show'] = '*'

    def set_status(self, color):
        self.tip_lab['fg'] = color

class ProgressBar(object):
    """ 比例条 """
    def __init__(self, master, width=180, height=18, bg='White', row=0, column=0):   #height=20
        self.canvas_bar = None
        self.canvas_shape = None
        self.canvas_text = None
        self.width = width
        self.height = height
        self.pack(master, bg, row, column)

    def pack(self, master, bg, row, column):
        self.canvas_bar = tk.Canvas(master, bg=bg, width=self.width, height=self.height)
        self.canvas_shape = self.canvas_bar.create_rectangle(0, 0, 0, self.height, fill='LightSkyBlue')
        self.canvas_text = self.canvas_bar.create_text(self.width/2, self.height/2+2, text='0%')
        self.canvas_bar.grid(row=row, column=column)

    def update(self, percent, success, colors=False):
        prog_len = int(self.width * percent / 100) + 1
        color = 'LightSkyBlue'   # 默认进度条颜色
        if colors:     # 程度颜色
            if 60 <= percent < 70:
                color = 'Gold'
            elif 70 <= percent < 80:
                color = 'Coral'
            elif 80 <= percent < 90:
                color = 'OrangeRed'
            elif 90 <= percent <= 100:
                color = 'Red3'
        elif not success:    # 失败
            color = 'Red'
        self.canvas_bar.coords(self.canvas_shape, (0, 0, prog_len, self.height+2))
        self.canvas_bar.itemconfig(self.canvas_text, text='%s%%' % percent)      # %.1f
        self.canvas_bar.itemconfig(self.canvas_shape, fill=color, outline=color)

class TopProgress(object):
    """ 顶窗滑块进度 """
    def __init__(self):
        self.top = None
        self.label = None
        self.progress = None
        self.pack()

    def pack(self):
        def close():
            pass
        self.top = t = tk.Toplevel()
        t.title('')
        t.geometry('{}x{}'.format(300, 80))
        t.resizable(False, False)
        t.wm_attributes('-topmost', 1)
        t.protocol("WM_DELETE_WINDOW", close)
        center_window(t)
        self.label = tk.Label(t, font=(Global.G_DEFAULT_FONT, 11))
        self.label.pack(pady=8)
        self.progress = ttk.Progressbar(t, mode='indeterminate', length=250)
        self.progress.pack(ipady=3)
        self.progress.start(10)   # 设置滑块速度

    def update(self, msg):
        if self.label and msg:
            self.label['text'] = msg

    def destroy(self, msg=None):
        try:
            self.progress.destroy()
            self.label.destroy()
            self.top.destroy()
        except:
            pass
        del self

class UploadProgress(object):
    """ 上传进度条 """
    def __init__(self, ip_list):
        self.progress = {}
        self.top = None
        self.pack(ip_list)

    def pack(self, ip_list):
        def close():
            self.top.destroy()
        self.showing = True
        self.top = tk.Toplevel()
        self.top.title('上传中，请稍候...')
        self.top.geometry('{}x{}'.format(400, 30*len(ip_list)))
        self.top.resizable(False, False)
        # self.top.wm_attributes('-topmost', 1)
        self.top.protocol("WM_DELETE_WINDOW", close)
        center_window(self.top)
        row = 0
        for ip in ip_list:
            tk.Label(self.top, text="{}:".format(ip)).grid(row=row, column=0, padx=10, pady=2)
            prog = ProgressBar(self.top, width=250, row=row, column=1)
            text = tk.Label(self.top)
            text.grid(row=row, column=2)
            self.progress[ip] = (prog, text)
            row += 1

    def update(self, ip, current, total, color):
        progress, text = self.progress[ip]
        progress.update(current/total*100, True, color)
        text['text'] = "  大小：%.1f/%.1fMB" % (current/1024/1024, total/1024/1024)

    def destroy(self):
        self.top.destroy()
        del self

class ToolBar(object):
    """ 工具栏 """
    def __init__(self, master, images, callback):
        for image, text in images:
            btn = ttk.Button(master,
                             image=view_gate.query_photo_image_data(image),
                             style="App.TButton",
                             command=lambda x=image: callback(x))
            btn.pack(side='left')
            WidgetTip.enter_tips(btn, text)

class MenuBar(object):
    """ 顶部菜单栏 """
    def __init__(self, master, trees, callback):
        self.callback = callback
        [self.sub_tree(master, node, tree) for node, tree in trees.items()]

    def sub_tree(self, root, node, tree):
        menu = tk.Menu(root, tearoff=0)
        root.add_cascade(label=node, menu=menu)
        for elem in tree:
            if isinstance(elem, dict):
                [self.sub_tree(menu, n, t) for n, t in elem.items()]
            elif elem == '-':
                menu.add_separator()
            else:
                tag, txt = elem
                menu.add_command(label=txt, command=lambda x=tag: self.callback(x))

class TreeView(object):
    """ 侧边导航栏 """
    def __init__(self, master, trees, callback):
        self.callback = callback
        self.all_id_map = OrderedDict()
        self.sub_images = []
        self.curr_image = None
        self.treeview  = tv = ttk.Treeview(master, height=50, show="tree", selectmode='browse')
        tv.tag_configure('tree.sub', font=('宋体', 12))
        tv.tag_configure('tree.root', font=('宋体', 12, 'bold'))
        tv.bind('<<TreeviewSelect>>', lambda e=None: self.select_handle())
        tv.pack(fill='both')
        # 可绑定滑块
        # vbar = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.treeview.yview)
        # self.treeview.configure(yscrollcommand=vbar.set)
        # vbar.pack(side='left', fill='y')
        [self.sub_tree(root) for root in trees]

    def sub_tree(self, root, id=''):
        def parser_ploter():
            if "AutoPlot" in attrs:
                if "ManualPlot" in attrs or "OperateButtons" in attrs:
                    raise Exception("'{}'界面错误: AutoPlot不能与ManualPlot或OperateButtons同时存在".format(text))
                return "AutoPlot"
            elif "ManualPlot" in attrs:
                return "ManualPlot"
            return ""

        text, image, pages, subtree = root['Text'], root['Image'], root['Page'], root['SubTree']
        if image in self.all_id_map:
            raise Exception("'{}'界面错误: Image参数与'{}'界面冲突".format(text, self.all_id_map[image][0]))
        img = view_gate.query_photo_image_data(image)
        toolbar = False
        if pages == 'NA':
            sub_id = self.treeview.insert(id, 'end', text=text, image=img, tags=('tree.root', 'simple'), values="")
        else:
            widgets = pages['Widgets']
            shell = pages['Shell']
            attrs = pages['Attrs']
            ploter = parser_ploter()
            buttons = 'True' if "OperateButtons" in attrs else 'False'
            window = 'True' if "ResultWindow" in attrs else 'False'
            tag, values = 'tree.sub', [image, text, widgets, shell, ploter, buttons, window]
            sub_id = self.treeview.insert(id, 'end', text=text, image=img, tags=(tag, 'simple'), values=values)
            toolbar = True if "ToolBarMember" in attrs else False
            self.sub_images.append(image)
        # 保存所有节点id, 以界面image为key #
        self.all_id_map[image] = (text, sub_id, toolbar)
        if isinstance(subtree, list) and len(subtree) != 0:
            [self.sub_tree(sub, sub_id) for sub in subtree]

    def expand_trees(self):
        [self.treeview.item(tup[1], open=True) for _, tup in self.all_id_map.items()]

    def select_handle(self):
        id = self.treeview.selection()[-1]
        args_tuple = self.treeview.item(id, "values")
        if len(args_tuple) == 0:
            return
        image, text, widgets, shell, ploter, buttons, window = args_tuple
        # treeview values中取出来的都是字符串,所以这里需要转换一下 #
        buttons = True if buttons == 'True' else False
        window = True if window == 'True' else False
        back_tuple = (image, text, widgets, shell, ploter, buttons, window)
        self.callback(back_tuple)
        self.curr_image = image

    def selection(self, image):
        # 根据image, 进入界面 #
        id = self.all_id_map[image][1]
        self.treeview.see(id)
        # 触发select事件 #
        self.treeview.selection_set(id)

    def last(self):
        if not self.curr_image:
            WidgetTip.warn("未选择界面")
            return
        index = self.sub_images.index(self.curr_image)
        if index == 0:
            WidgetTip.warn("已经为第一个界面")
            return
        self.selection(self.sub_images[index - 1])

    def next(self):
        if not self.curr_image:
            WidgetTip.warn("未选择界面")
            return
        index = self.sub_images.index(self.curr_image)
        if index == len(self.sub_images) - 1:
            WidgetTip.warn("已经为最后一个界面")
            return
        self.selection(self.sub_images[index + 1])

    def get_toolbar_keys(self):
        out = []
        for image, tup in self.all_id_map.items():
            text = tup[0]
            toolbar = tup[2]
            if toolbar:
                out.append((image, text))
        return out

class InfoText(object):
    """ 消息提示栏 """
    def __init__(self, master, height=40):
        self.master = master
        self.infotext = None
        self.index = 0
        self.lock = Lock()
        self.init_frame(height)

    def init_frame(self, height):
        self.infotext = scrolledtext.ScrolledText(self.master,
                                                  font=(Global.G_DEFAULT_FONT, 9),
                                                  # bd=1,
                                                  relief='ridge',
                                                  bg=Global.G_DEFAULT_COLOR,
                                                  height=height)
        self.infotext['stat'] = 'disabled'
        self.infotext.pack(fill='both')

    def insert_text(self, info, color=False):
        # 多线程打印可能会串行等问题, 加锁
        self.lock.acquire()
        try:
            self.infotext['stat'] = 'normal'
            self.infotext.insert('end', '{}\n'.format(info))
            if color:
                self.index += 1
                line_num = len(info.split('\n'))
                line_end = int(self.infotext.index('end').split('.')[0]) - 1   # 减去换行那行
                line_start = line_end - line_num
                self.infotext.tag_add('TextS%s' % self.index, '%s.0' % line_start, '%s.end' % line_end)
                self.infotext.tag_config('TextS%s' % self.index, foreground=color)
            self.infotext.see('end')
            self.infotext['stat'] = 'disabled'
        finally:
            self.lock.release()

class LabelButton(object):
    """ Radiobutton实现的侧边菜单栏 """

    def __init__(self, master, name, shell, intvar, text, command):
        self.name = name
        self.shell = shell
        self.command = command
        self.button = tk.Radiobutton(master,
                                     selectcolor='SkyBlue2',
                                     fg='Snow',
                                     bg='SkyBlue4',
                                     variable=intvar,
                                     width=20,
                                     bd=0,
                                     indicatoron=0,
                                     value=name,
                                     text=text,
                                     justify='left',
                                     font=('宋体', 14),
                                     command=self._click)
        self.button.bind("<Enter>", self.enter)
        self.button.bind("<Leave>", self.leave)
        self.button.pack(fill='both')

    def enter(self, event=None):
        self.button['fg'] = 'Brown1'
        self.button['bg'] = 'SkyBlue3'

    def leave(self, event=None):
        self.button['fg'] = 'Snow'
        self.button['bg'] = 'SkyBlue4'
    
    def pack(self):
        self.button.pack(ipady=12)
        
    def _click(self, event=None):
        self.command(self.name, self.shell)

class LabelEntry(object):
    def __init__(self, master, text,
                 default='',
                 row=0, column=0,
                 lab_width=30, en_width=32):
        tk.Label(master, text=text, width=lab_width, anchor='e').grid(row=row, column=column)
        self.entry = ttk.Entry(master, width=en_width)
        self.entry.grid(row=row, column=column + 1, padx=10, pady=1, sticky='w')
        self.entry.insert(0, default)

    def get(self):
        return self.entry.get()

class LabelCombobox(object):
    def __init__(self, master, text, values,
                 default='',
                 row=0, column=0,
                 lab_width=30, com_width=30):
        tk.Label(master, text=text, width=lab_width, anchor='e').grid(row=row, column=column)
        self.Combobox = ttk.Combobox(master, values=values, width=com_width, state='readonly')
        self.Combobox.grid(row=row, column=column + 1, padx=10, pady=1)
        index = values.index(default) if (default and default in values) else 0
        self.Combobox.current(index)

    def get(self):
        return self.Combobox.get()

class ColorButton(object):
    """ 封装button，个性化外观 """

    def __init__(self, master, text, command, size=10, width=10):
        self.master = master
        self.button = tk.Button(master,
                                text=text,
                                activebackground=Global.G_DEFAULT_COLOR,
                                activeforeground='Red',
                                disabledforeground='Red',
                                fg='Gray23',  # 'DodgerBlue4',
                                bg=Global.G_DEFAULT_COLOR,
                                font=(Global.G_DEFAULT_FONT, size, 'bold'),
                                width=width,
                                bd=0,
                                relief='groove',
                                command=command)
        #self.button.bind("<Enter>", self.enter)
        #self.button.bind("<Leave>", self.leave)
        self.button.pack(side='left')
        self.disable(False)

    def enter(self, event=None):
        self.button['bg'] = 'Grey27'  # 'DodgerBlue4'
        self.button['fg'] = Global.G_DEFAULT_COLOR

    def leave(self, event=None):
        self.button['bg'] = Global.G_DEFAULT_COLOR
        self.button['fg'] = 'Gray23'  # 'DodgerBlue4'

    def disable(self, flag):
        if flag:
            self.button['state'] = 'disable'
            self.button.unbind("<Enter>")
            self.button.bind("<Leave>")
        else:
            self.button['state'] = 'normal'
            self.button.bind("<Enter>", self.enter)
            self.button.bind("<Leave>", self.leave)

class TitleFrame(object):
    """ 带有主题信息的Frame """
    def __init__(self, master, width, height, title='', center=False, color=Global.G_FM_TITLE_COLOR):
        head_height = 25 if title != '' else 0
        _master = tk.LabelFrame(master, width=width, height=height+head_height)
        _master.pack(anchor='w')
        _master.pack_propagate(0)
        if title != '':
            head_fm = tk.Frame(_master, height=head_height)
            head_fm.pack(fill='x')
            anchor = 'center' if center else 'w'
            text = "  %s  " % title
            label = tk.Label(head_fm, text=text, font=(Global.G_DEFAULT_FONT, 10, 'bold'), anchor=anchor, bg=color)
            label.pack(fill='both')
        self.body = tk.Frame(_master, height=height)
        self.body.pack(fill='both')

    def master(self):
        return self.body

class ScrollFrame(tk.Frame):
    """ 带有滑块的窗体Frame """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.body = tk.Frame(canvas)
        self.body.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.body, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class TopNotebook:
    """ 弹窗结果栏 """
    showing = False
    top = None
    instance = {}

    @classmethod
    def pack(cls, ip_list):
        def search(event=None):
            for ip, text in cls.instance.items():
                text.tag_remove("highlight", "1.0", "end")
                start = 1.0
                while True:
                    pattern = en.get()
                    if not pattern:
                        break
                    pos = text.search(pattern, start, stopindex='end', regexp=True)
                    if not pos:
                        break
                    end = '%s.%s' % (pos.split('.')[0], len(pattern) + int(pos.split('.')[1]))
                    text.tag_add('highlight', pos, end)
                    start = pos + '+1c'
        if cls.showing:
            return
        cls.showing = True
        cls.top = top = tk.Toplevel()
        top.title('')
        top.resizable(False, False)
        # top.wm_attributes('-topmost', 1)
        top.protocol("WM_DELETE_WINDOW", cls.close)
        top.geometry('{}x{}'.format(1000, 730))
        center_window(top)
        master = TitleFrame(top, 1000, 700, '输 出 结 果', True).master()
        notebook = ttk.Notebook(master, style="App.TNotebook")
        notebook.pack()

        for ip in ip_list:
            fm = tk.Frame(notebook)
            fm.pack()
            text = scrolledtext.ScrolledText(fm, width=200, height=50, bg='Gray20', fg='Snow', stat='disabled')
            text.tag_configure('highlight', background='red')
            text.pack(fill='both')
            notebook.add(fm, text=ip)
            cls.instance[ip] = text

        sub_fm = tk.Frame(master)
        sub_fm.pack()
        tk.Label(sub_fm, text='高亮搜索 ', font=(Global.G_DEFAULT_FONT, 12, 'bold'), fg='Red').pack(side='left')
        en = ttk.Entry(sub_fm, width=60)
        en.pack(side='left', pady=8)
        en.bind('<Key>', search)
        tags = en.bindtags()
        en.bindtags(tags[1:] + tags[:1])

    @classmethod
    def insert(cls, ip, info):
        if not cls.showing:
            return
        instance = cls.instance[ip]
        instance['stat'] = 'normal'
        instance.delete('0.0', 'end')
        instance.insert('end', '{}\n'.format(info))
        instance.see('end')
        instance['stat'] = 'disabled'

    @classmethod
    def close(cls):
        cls.showing = False
        cls.top.destroy()

class TopAbout(object):
    """ 关于信息栏 """
    def __init__(self):
        self.top = None
        self.pack()

    def pack(self):
        self.top = top = tk.Toplevel()
        top.title('关于软件')
        top.geometry('{}x{}'.format(500, 340))
        top.resizable(False, False)
        top.wm_attributes('-topmost', 1)
        top.protocol("WM_DELETE_WINDOW", self.close)
        center_window(top)
        tk.Label(top, image=view_gate.query_photo_image_data('ABOUT')).pack()
        # 中间部分说明
        tk.Label(top,
                 bg=Global.G_DEFAULT_COLOR,
                 justify='left',
                 text=view_gate.query_about_info_data(),
                 font=(Global.G_DEFAULT_FONT, 10)
                 ).pack(fill='both', ipady=5)
        # 底部版权说明
        tk.Label(top, text=view_gate.query_env_define_data('G_COPYRIGHT_INFO')).pack()

    def close(self):
        self.top.destroy()
        del self

class ScreenShot(object):
    """ 截屏实现类 """
    def __init__(self):
        self.sel = None
        self.last = None
        self.temp_png = '__temp__.png'
        # 先对全屏幕进行截图
        im = ImageGrab.grab()
        im.save(self.temp_png)
        im.close()
        # 变量X和Y用来记录鼠标左键按下的位置
        self.X = tk.IntVar(value=0)
        self.Y = tk.IntVar(value=0)
        self.top = tk.Toplevel()
        self.top.overrideredirect(True)
        width = self.top.winfo_screenwidth()
        height = self.top.winfo_screenheight()
        self.canvas = tk.Canvas(self.top, width=width, height=height)
        view_gate.add_image_data.set_data(['SCREEN_TEMP', self.temp_png])
        self.canvas.create_image(width//2, height//2, image=view_gate.query_photo_image_data('SCREEN_TEMP'))
        # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
        def deleteLastDraw():
            try:
                self.canvas.delete(self.last)
            except:
                pass
        # 鼠标左键按下的位置
        def onLeftButtonDown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            self.sel = True
        self.canvas.bind('<Button-1>', onLeftButtonDown)
        # 鼠标左键移动，显示选取的区域
        def onLeftButtonMove(event):
            if not self.sel:
                return
            deleteLastDraw()
            self.last = self.canvas.create_rectangle(self.X.get(),
                                                     self.Y.get(),
                                                     event.x,
                                                     event.y,
                                                     width = 2,
                                                     outline='Red')
        self.canvas.bind('<B1-Motion>', onLeftButtonMove)
        # 获取鼠标左键抬起的位置，保存区域截图
        def onLeftButtonUp(event):
            self.sel = False
            deleteLastDraw()
            Common.sleep(0.1)
            # 考虑鼠标左键从右下方按下而从左上方抬起的截图
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            pic = ImageGrab.grab((left+1, top+1, right, bottom))
            save_name = "ScreenShot-{0}.png".format(Common.get_time(format=False))
            pic.save(save_name)
            self.top.destroy()
            Common.remove(self.temp_png)
            WidgetTip.info("截图成功: {0}\n截图保存在工具家目录下".format(save_name))
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
        # 让canvas充满窗口，并随窗口自动适应大小
        self.canvas.pack(fill='both', expand=1)

class SelectionBar(object):
    """ IP 选项栏 """
    def __init__(self, master, ip_list, callback):
        self.master = master
        self.progress = {}
        self.lab_tips = {}
        self.btn_inst = []
        self.timer_inst = []
        self.pack(ip_list, callback)

    def set_progress(self, ip, prog, status):
        self.progress[ip].update(prog, status, False)

    def set_status(self, ip, status):
        if not self.lab_tips:
            return
        self.lab_tips[ip]['fg'] = Global.G_TIP_FG_COLOR[status]

    def pack(self, ip_list, callback):
        def execute(oper):
            ips, opts = [], []
            for v in ip_vars:
                if int(v.get()):
                    ips.append(ip_list[ip_vars.index(v)])
            opts.append(True if int(opt_vars[0].get()) == 1 else False)
            i = 1
            for en in [delay_en, loop_en]:
                if int(opt_vars[i].get()) == 1:
                    try:
                        val = int(en.get())
                    except:
                        WidgetTip.error("'延迟执行' 或 '周期执行' 参数非法")
                        return
                    opts.append(val)
                else:
                    opts.append(0)
                i += 1
            callback([oper, ips, opts])
        def pack_ips():
            master = tk.LabelFrame(self.master)
            master.pack(fill='both')
            sf = ScrollFrame(master)
            sf.pack(fill='both')
            ips_fm = sf.body
            row = 0
            for ip in ip_list:
                lab = tk.Label(ips_fm, text='●', font=(Global.G_DEFAULT_FONT, 12), fg=Global.G_TIP_FG_COLOR['DEFAULT'])
                lab.grid(row=row, column=0)
                self.lab_tips[ip] = lab
                ip_vars.append(tk.IntVar())
                ttk.Checkbutton(ips_fm,
                               text=ip,
                               #font=(Global.G_DEFAULT_FONT, 10),
                               #anchor='w',
                               width=15,
                               variable=ip_vars[-1]
                               ).grid(row=row, column=1)
                self.progress[ip] = ProgressBar(master=ips_fm, row=row, column=2)
                row += 1
        def pack_opts():
            opt_fm = tk.LabelFrame(self.master, width=width, height=height / 3 / 3 * 2)
            btn_fm = tk.LabelFrame(self.master, width=width, height=height / 3 / 3 * 1)
            opt_fm.pack(fill='both')
            btn_fm.pack(fill='both')
            ckb_style = {'master': opt_fm,
                         #'font': (Global.G_DEFAULT_FONT, 10),
                         #'anchor': 'w',
                         'width': 12}
            opt_vars.append(tk.IntVar())
            ttk.Checkbutton(text="root执行", variable=opt_vars[-1], **ckb_style).grid(row=0, column=0, padx=20, pady=3)
            opt_vars.append(tk.IntVar())
            ttk.Checkbutton(text="延迟执行", variable=opt_vars[-1], **ckb_style).grid(row=1, column=0, padx=20, pady=3)
            opt_vars.append(tk.IntVar())
            ttk.Checkbutton(text="周期执行", variable=opt_vars[-1], **ckb_style).grid(row=2, column=0, padx=20, pady=3)
            delay_en = ttk.Entry(opt_fm, width=15)
            loop_en = ttk.Entry(opt_fm, width=15)
            delay_en.grid(row=1, column=1)
            loop_en.grid(row=2, column=1)
            tk.Label(opt_fm, text='分钟').grid(row=1, column=2)
            tk.Label(opt_fm, text='分钟').grid(row=2, column=2)
            btn_e = ttk.Button(btn_fm, text='执行', width=20, command=lambda op='start': execute(op))
            btn_e.grid(row=0, column=0, padx=15, pady=10)
            btn_s = ttk.Button(btn_fm, text='停止', width=20, command=lambda op='stop': execute(op))
            btn_s.grid(row=0, column=1, padx=15, pady=10)
            self.btn_inst.append(btn_e)
            self.btn_inst.append(btn_s)
            return delay_en, loop_en
        def pack_timer():
            tk.Label(self.master).pack()
            tk.Label(self.master, text='首次执行倒计时: ').pack()
            first = tk.Label(self.master, text='00:00:00', font=(Global.G_DEFAULT_FONT, 16))
            first.pack()
            tk.Label(self.master, text='下一次执行倒计时: ').pack()
            next = tk.Label(self.master, text='00:00:00', font=(Global.G_DEFAULT_FONT, 16))
            next.pack()
            self.timer_inst.append(first)
            self.timer_inst.append(next)

        ip_vars, opt_vars = [], []
        width, height = Global.G_MAIN_IPS_WIDTH, Global.G_MAIN_OPER_HEIGHT
        pack_ips()
        delay_en, loop_en = pack_opts()
        pack_timer()

    def show_button(self, show):
        state = '!disabled' if show else 'disabled'
        [btn.state([state]) for btn in self.btn_inst]

    def update_timer(self, first, next):
        h = int(first / 3600)
        m = int((first % 3600) / 60)
        s = int(first % 60)
        self.timer_inst[0]['text'] = '%02d:%02d:%02d' % (h, m, s)
        h = int(next / 3600)
        m = int((next % 3600) / 60)
        s = int(next % 60)
        self.timer_inst[1]['text'] = '%02d:%02d:%02d' % (h, m, s)
