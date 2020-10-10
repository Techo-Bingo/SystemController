# -*- coding: UTF-8 -*-
"""
View板块的单个子模块
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import ImageGrab
import my_global as Global
from my_common import Common
from my_bond import Bonder, Define, Caller
from my_viewutil import WinMsg, ToolTips, ViewUtil
# from my_logger import Logger


class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        # Display text in tooltip window
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() - 10
        tw = self.tipwindow = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        tk.Label(tw,
                 text=self.text,
                 justify='left',
                 background="#ffffe0",
                 relief=tk.SOLID,
                 borderwidth=1,
                 font=("tahoma", "8")
                 ).pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


class SubLogin(object):
    """ 登录子板块，不可为单例 """

    def __init__(self, master, index):
        self.master = master
        self.index = index
        self.bonder = None
        self.tiglab = None
        self.ip_en = None
        self.user_en = None
        self.userpwd_en = None
        self.rootpwd_en = None
        self.delbtn = None
        self.var_user = tk.StringVar()
        self.var_upwd = tk.StringVar()
        self.var_rpwd = tk.StringVar()
        self.init_event()
        self.init_frame()
        self.pack_frame()
        self.set_defaults()
        self.see_passwd_off()

    def init_event(self):
        _index = self.index
        _name = Global.G_EVT_NAME_SUBLOGIN % _index
        self.bonder = Bonder(_name)
        self.bonder.bond(Global.EVT_SEE_PSWD_ON, self.see_passwd_on)
        self.bonder.bond(Global.EVT_SEE_PSWD_OFF, self.see_passwd_off)
        Define.define(Global.EVT_GET_LOGIN_INPUT % _index, self.get_inputs)
        Define.define(Global.EVT_CHG_LOGIN_TIG_COLOR % _index, self.status_tig)
        Define.define(Global.EVT_SUBLOGIN_ENTRY_TIG % _index, self.widget_tips)

    def init_frame(self):
        entry_style = {'master': self.master,
                       'font': (Global.G_FONT, 11)}
        self.tiglab = tk.Label(self.master,
                               text='●',
                               font=(Global.G_FONT, 16),
                               fg=Global.G_TIG_FG_COLOR['DEFAULT'])
        self.ip_en = ttk.Entry(width=15, **entry_style)
        self.user_en = ttk.Entry(width=13, textvariable=self.var_user, **entry_style)
        self.userpwd_en = ttk.Entry(width=14, textvariable=self.var_upwd, **entry_style)
        self.rootpwd_en = ttk.Entry(width=13, textvariable=self.var_rpwd, **entry_style)
        self.delbtn = tk.Button(self.master,
                                text='×',
                                font=(Global.G_FONT, 13, 'bold'),
                                bd=0,
                                command=self.destroy)

    def pack_frame(self):
        grid_style = {'row': self.index + 1,
                      'padx': 4,
                      'pady': 6,
                      'ipady': 3}
        self.tiglab.grid(row=self.index + 1, column=0)
        self.ip_en.grid(column=1, **grid_style)
        self.user_en.grid(column=2, **grid_style)
        self.userpwd_en.grid(column=3, **grid_style)
        self.rootpwd_en.grid(column=4, **grid_style)
        if self.index == 1:
            return
        self.delbtn.grid(row=self.index + 1, column=5)

    def set_defaults(self):
        """ 设置默认用户和密码 """
        default_info = Global.G_DEFAULT_PASSWORDS
        self.var_user.set(default_info[0])
        self.var_upwd.set(default_info[1])
        self.var_rpwd.set(default_info[2])

    def get_inputs(self, msg=None):
        return (self.ip_en.get(),
                self.user_en.get(),
                self.userpwd_en.get(),
                self.rootpwd_en.get()
                )

    def see_passwd_on(self, msg=None):
        self.userpwd_en['show'] = ''
        self.rootpwd_en['show'] = ''

    def see_passwd_off(self, msg=None):
        self.userpwd_en['show'] = '*'
        self.rootpwd_en['show'] = '*'

    def status_tig(self, status):
        """ 登录状态颜色提示 """
        try:
            self.tiglab['fg'] = Global.G_TIG_FG_COLOR[status]
        except:
            pass

    def widget_tips(self, which):
        """ 用于提示具体的entry填入的值有误 """
        try:
            ToolTips.widget_tips(eval('self.{}_en'.format(which)))
        except:
            pass

    def destroy(self):
        _index = self.index
        self.tiglab.grid_remove()
        self.ip_en.grid_remove()
        self.user_en.grid_remove()
        self.userpwd_en.grid_remove()
        self.rootpwd_en.grid_remove()
        self.delbtn.grid_remove()
        self.bonder.unbond(Global.EVT_SEE_PSWD_ON)
        self.bonder.unbond(Global.EVT_SEE_PSWD_OFF)
        Define.undefine(Global.EVT_GET_LOGIN_INPUT % _index)
        Define.undefine(Global.EVT_CHG_LOGIN_TIG_COLOR % _index)
        Define.undefine(Global.EVT_SUBLOGIN_ENTRY_TIG % _index)
        ViewUtil.del_sublogin(_index)
        del self


class TtkProgress(object):
    """ Ttk 实现的进度条 """

    def __init__(self,
                 master,
                 name,
                 width=200,
                 size=2,
                 row=1,
                 column=0):
        self.prog = ttk.Progressbar(master,
                                    length=width,
                                    mode="determinate",
                                    orient=tk.HORIZONTAL)
        self.prog["maximum"] = 100
        self.prog["value"] = 0
        tk.Label(master, text=name, font=(Global.G_FONT, 9+size)).grid(row=row, column=column)
        self.val_lab = tk.Label(master, text='0%', font=(Global.G_FONT, 9+size))
        self.prog.grid(row=row, column=column+1, ipady=size)
        self.val_lab.grid(row=row, column=column+2)

    def update(self, value):
        """ 0~1 """
        _value = value * 100
        self.prog['value'] = _value
        self.val_lab['text'] = '%s%%' % _value

    def destroy(self):
        self.prog.destroy()
        self.val_lab.destroy()


class ProgressBar(object):
    """ 进度条/比例条 """
    def __init__(self, master, width=240, height=20, bg='White', row=0, column=0):
        self.canvas_bar = None
        self.canvas_shape = None
        self.canvas_text = None
        self.width = width
        self.height = height
        self.pack_frame(master, bg, row, column)

    def pack_frame(self, master, bg, row, column):
        self.canvas_bar = tk.Canvas(master, bg=bg, width=self.width, height=self.height)
        self.canvas_shape = self.canvas_bar.create_rectangle(0, 0, 0, self.height, fill='LightSkyBlue')
        self.canvas_text = self.canvas_bar.create_text(self.width/2, self.height/2+2, text='0%')
        self.canvas_bar.grid(row=row, column=column)

    def update(self, percent, change_color=False):
        prog_len = int(self.width * percent / 100) + 1
        color = 'LightSkyBlue'
        if isinstance(change_color, str):
            color = change_color
        elif change_color:
            if 60 <= percent < 70:
                color = 'Gold'
            elif 70 <= percent < 80:
                color = 'Coral'
            elif 80 <= percent < 90:
                color = 'OrangeRed'
            elif 90 <= percent <= 100:
                color = 'Red3'
        self.canvas_bar.coords(self.canvas_shape, (0, 0, prog_len, self.height+2))
        self.canvas_bar.itemconfig(self.canvas_text, text='%d%%' % percent)
        self.canvas_bar.itemconfig(self.canvas_shape, fill=color, outline=color)


class MyToolBar(object):
    """ 快捷工具栏 """
    def __init__(self, master, images, callback):
        btn_style = ttk.Style()
        btn_style.theme_use('clam')
        btn_style.configure("C.TButton", borderwidth=0, background=Global.G_MAIN_OPER_BG)
        for image_set in images:
            image, text = image_set
            btn = ttk.Button(master,
                             image=ViewUtil.get_image(image),
                             style="C.TButton",
                             command=lambda x=image: callback(x))
            btn.pack(side='left')
            createToolTip(btn, text)


class MyTreeView(object):
    """ 侧边折叠菜单栏 """
    def __init__(self, master, treelist, callback):
        self.master = master
        self.treelist = treelist
        self.callback = callback
        self.treeview = None
        self.widgets = None
        self.sub_id = []
        self.init_frame()

    def _add_subtree(self, root, id=''):
        if '__ThisIsPageWidgets__' in root:
            self.widgets = root
            return
        text = ' ' + root['Text']
        img = root['Image']
        pages = root['Page']
        subtree = root['SubTree']

        if pages == 'NA':
            tag, values = 'tree.root', ""
        else:
            widgets = pages['Widgets']
            print = pages['PrintIn']
            shell = pages['Shell']
            showip = pages['IPChoose']
            tag, values = 'tree.sub', [text, widgets, shell, print, showip]
        image = ViewUtil.get_image(img)
        sub_id = self.treeview.insert(id, 'end', text=text, image=image, tags=(tag, 'simple'), values=values)
        self.sub_id.append(sub_id)
        if isinstance(subtree, list) and len(subtree) != 0:
            [self._add_subtree(sub, sub_id) for sub in subtree]

    def init_frame(self):
        self.treeview = ttk.Treeview(self.master, height=50, show="tree", selectmode='browse')
        self.treeview.tag_configure('tree.sub', font=('宋体', 12))
        self.treeview.tag_configure('tree.root', font=('宋体', 12, 'bold'))
        self.treeview.bind('<<TreeviewSelect>>', self.command)
        [self._add_subtree(root) for root in self.treelist]
        self.treeview.pack(fill='both')
        # 可选绑定滑块
        # vbar = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.treeview.yview)
        # self.treeview.configure(yscrollcommand=vbar.set)
        # vbar.pack(side='left', fill='y')

    def expand_trees(self):
        # 展开所有子树
        [self.treeview.item(id, open=True) for id in self.sub_id]

    def command(self, event=None):
        args_tuple = self.treeview.item(self.treeview.selection()[-1], "values")
        if len(args_tuple) == 0:
            return
        text, widgets, print, shell, showip = args_tuple
        try:
            back_tuple = (text, self.widgets[widgets], shell, print, showip)
        except Exception as e:
            ToolTips.inner_error(e)
        else:
            self.callback(back_tuple)


class InfoWindow(object):
    """ 消息提示栏 """

    def __init__(self, master):
        self.master = master
        self.infotext = None
        self.index = 0
        self.init_event()
        self.init_frame()

    def init_event(self):
        Define.define(Global.EVT_INSERT_INFOWIN_TEXT, self.insert_text)

    def init_frame(self):
        self.infotext = scrolledtext.ScrolledText(self.master,
                                                  font=(Global.G_FONT, 9),
                                                  bd=2,
                                                  relief='ridge',
                                                  # fg='Blue',
                                                  bg=Global.G_DEFAULT_COLOR,
                                                  height=40)
        self.infotext.insert(tk.END, Global.G_WELCOME_INFO)
        self.infotext['stat'] = 'disabled'
        self.infotext.pack(fill='x')
        # 设置infowin可以接受事件的变量为True
        ViewUtil.set_infowin_flag()

    def insert_text(self, msg=None):
        info, level = msg
        try:
            """ 级别转换成对应的颜色 """
            color = Global.G_INFOWIN_LEVEL_COLOR[level.upper()]
        except KeyError:
            color = Global.G_INFOWIN_LEVEL_COLOR['INFO']

        """ 信息中加入时间戳 """
        info = "\n[{0}] {1}: {2}".format(level.upper(), Common.get_time(), str(info))
        self.infotext['stat'] = 'normal'
        self.infotext.insert('end', info)
        self.index += 1
        line_num = len(info.split('\n'))
        line_end = int(self.infotext.index('end').split('.')[0])
        line_start = line_end - line_num + 1
        self.infotext.tag_add('BINGO%s' % self.index, '%s.0' % line_start, '%s.end' % line_end)
        self.infotext.tag_config('BINGO%s' % self.index, foreground=color)
        self.infotext.see('end')
        self.infotext['stat'] = 'disabled'


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


class MyButton(object):
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
                                font=(Global.G_FONT, size, 'bold'),
                                width=width,
                                bd=0,
                                relief='groove',
                                command=command)
        self.button.bind("<Enter>", self.enter)
        self.button.bind("<Leave>", self.leave)
        self.button.pack(side='left')

    def enter(self, event=None):
        self.button['bg'] = 'Grey27'  # 'DodgerBlue4'
        self.button['fg'] = Global.G_DEFAULT_COLOR

    def leave(self, event=None):
        self.button['bg'] = Global.G_DEFAULT_COLOR
        self.button['fg'] = 'Gray23'  # 'DodgerBlue4'

    def config(self, key, value):
        self.button[key] = value


class MyFrame(object):
    """ 封装Frame，带有头部的个性化Frame """
    def __init__(self, master, width, height, title, head=True):
        self.body = None
        self.pack_frame(master, width, height, title, head)

    def pack_frame(self, master, width, height, title, head):
        head_height = 25 if head else 0
        _master = tk.LabelFrame(master, width=width, height=height+head_height, bg='Snow')
        _master.pack()
        _master.pack_propagate(0)
        if head:
            head_fm = tk.Frame(_master, height=head_height)
            label = tk.Label(head_fm, text=title, height=1, font=(Global.G_FONT, 10, 'bold'),  bg='LightBlue')
            head_fm.pack(fill='x')
            label.pack(fill='both')
        self.body = tk.Frame(_master, height=height, bg='Snow')
        self.body.pack(fill='both')

    def master(self):
        return self.body


class TopProgress:
    """ 顶窗提示进度 """
    _toplevel = None
    _progress = None
    _infolab = None
    _top_size = (300, 80)

    @classmethod
    def start(cls, msg=None):
        width, height = cls._top_size
        cls._toplevel = tk.Toplevel()
        cls._toplevel.title('请稍候')
        cls._toplevel.resizable(False, False)
        cls._toplevel.wm_attributes('-topmost', 1)
        cls._toplevel.protocol("WM_DELETE_WINDOW", cls.close)
        ViewUtil.set_widget_size(cls._toplevel, width, height, True)
        cls._infolab = tk.Label(cls._toplevel, font=(Global.G_FONT, 11))
        cls._infolab.pack(pady=8)
        cls._progress = ttk.Progressbar(cls._toplevel, mode='indeterminate', length=250)
        cls._progress.pack(ipady=3)
        """ 开始滑块，并设置速度 """
        cls._progress.start(10)

    @classmethod
    def update(cls, info):
        if cls._infolab:
            cls._infolab['text'] = info

    @classmethod
    def destroy(cls, msg=None):
        try:
            cls._progress.destroy()
            cls._toplevel.destroy()
            cls._infolab.destroy()
        except:
            pass
        cls._toplevel = None
        cls._progress = None

    @classmethod
    def close(cls):
        pass


class TopAbout:
    """ 关于窗 """
    _top_size = (500, 340)
    _toplevel = None
    _showing = False

    @classmethod
    def show(cls, event=None):
        if cls._showing:
            return
        cls._showing = True
        width, height = cls._top_size
        cls._toplevel = tk.Toplevel()
        cls._toplevel.title('关于软件')
        cls._toplevel.resizable(False, False)
        cls._toplevel.wm_attributes('-topmost', 1)
        cls._toplevel.protocol("WM_DELETE_WINDOW", cls.close)
        ViewUtil.set_widget_size(cls._toplevel, width, height, True)
        # 图标
        tk.Label(cls._toplevel, image=ViewUtil.get_image('ABOUT')).pack()
        # 中间部分说明
        _infolab = tk.Label(cls._toplevel,
                            bg='Snow',
                            justify='left',
                            text=Global.G_ABOUT_INFO,
                            font=(Global.G_FONT, 10))
        _infolab.pack(fill='both', ipady=5)
        # 底部版权说明
        tk.Label(cls._toplevel, text=Global.G_COPYRIGHT_INFO).pack()

    @classmethod
    def close(cls, event=None):
        cls._showing = False
        cls._toplevel.destroy()


class MyScreenshot(object):
    """ 截屏实现类 """
    def __init__(self, master):
        self.sel = None
        self.last = None
        self.temp_png = '.\\download\\__temp__.png'
        # 先对全屏幕进行截图
        im = ImageGrab.grab()
        im.save(self.temp_png)
        im.close()
        # 变量X和Y用来记录鼠标左键按下的位置
        self.X = tk.IntVar(value=0)
        self.Y = tk.IntVar(value=0)
        width, height = ViewUtil.get_screensize()
        self.top = tk.Toplevel(master, width=width, height=height)
        self.top.overrideredirect(True)
        Caller.call(Global.EVT_ADD_IMAGE, ('SCREEN_TEMP', self.temp_png))
        self.canvas = tk.Canvas(self.top, width=width, height=height)
        self.canvas.create_image(width//2, height//2, image=ViewUtil.get_image('SCREEN_TEMP'))
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
            WinMsg.info("截屏成功: {0}".format(save_name))
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
        #让canvas充满窗口，并随窗口自动适应大小
        self.canvas.pack(fill='both', expand=1)

