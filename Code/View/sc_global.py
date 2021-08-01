# -*- coding: UTF-8 -*-

class Global:
    G_DEFAULT_FONT = '微软雅黑'
    G_DEFAULT_COLOR = 'Snow'
    # pages界面背景色
    G_MAIN_PAGE_COLOR = 'Gray94'  # ''Snow'
    # info window 文字前景色
    G_INFOWIN_LEVEL_COLOR = {'INFO': 'Black',
                             'TIPS': 'Blue',
                             'WARN': 'DarkOrange',
                             'ERROR': 'Red'}
    # 登录结果提示的前景色
    G_TIP_FG_COLOR = {'DEFAULT': 'Snow',
                      'SUCCESS': 'SeaGreen1',
                      'LOGGING': 'DarkGrey',
                      'FAILED': 'OrangeRed'}
    G_FM_TITLE_COLOR = 'LightBlue'
    # 登录界面宽高
    G_LGN_WIN_WIDTH = 600
    G_LGN_WIN_HEIGHT = 500
    # 登陆界面图片栏高度
    G_LGN_HEAD_HEIGHT = 160
    # 登陆界面按钮栏高度
    G_LGN_FOOT_HEIGHT = 60
    # 登录界面登录窗高度
    G_LGN_FUNC_HEIGHT = G_LGN_WIN_HEIGHT - G_LGN_HEAD_HEIGHT - G_LGN_FOOT_HEIGHT

    # 软件总宽高
    G_APP_WIDTH = 1600
    G_APP_HEIGHT = 950
    # 主界面宽高
    G_MAIN_WIN_WIDTH = 0
    G_MAIN_WIN_HEIGHT = 0
    # 主界面树形导航栏宽高
    G_MAIN_TREE_WIDTH = 0
    # 主界面操作窗宽高
    G_MAIN_OPER_WIDTH = 0
    G_MAIN_OPER_HEIGHT = 0
    # 主界面操作页面宽高
    G_MAIN_PAGE_WIDTH = 0
    # 主界面IP执行栏宽高
    G_MAIN_IPS_WIDTH = 0
    # 主界面text栏宽高
    G_MAIN_TEXT_HEIGHT = 0
    # 主界面信息提示info栏宽高
    G_MAIN_INFO_WIDTH = 0
    # 主界面note栏宽高
    G_MAIN_NOTE_WIDTH = 0

    # 支持的模板控件
    G_SUPPORTED_WIDGETS = ['Label',
                           'Checkbox',
                           'Combobox',
                           'Entry',
                           'Text',
                           'Button',
                           'Notebook',
                           'MultiCombobox',
                           "PlotNotebook"]

    @classmethod
    def refresh(cls):
        cls.G_MAIN_WIN_WIDTH = cls.G_APP_WIDTH
        cls.G_MAIN_WIN_HEIGHT = cls.G_APP_HEIGHT - 50     # 50含工具栏 + 底部信息栏高度
        cls.G_MAIN_TREE_WIDTH = 250
        cls.G_MAIN_OPER_WIDTH = cls.G_MAIN_WIN_WIDTH - cls.G_MAIN_TREE_WIDTH
        cls.G_MAIN_OPER_HEIGHT = 600
        cls.G_MAIN_PAGE_WIDTH = 930
        cls.G_MAIN_IPS_WIDTH = cls.G_MAIN_OPER_WIDTH - cls.G_MAIN_PAGE_WIDTH
        cls.G_MAIN_TEXT_HEIGHT = cls.G_MAIN_WIN_HEIGHT - cls.G_MAIN_OPER_HEIGHT
        cls.G_MAIN_INFO_WIDTH = cls.G_MAIN_PAGE_WIDTH
        cls.G_MAIN_NOTE_WIDTH = cls.G_MAIN_IPS_WIDTH
