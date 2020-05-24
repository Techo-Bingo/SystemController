# -*- coding: UTF-8 -*-
"""
全局定义
"""
__author__ = 'libin WX382598 (Bingo)'
# 版权信息
G_COPYRIGHT_INFO = 'Copyright©2019 Bingo. All Rights Reserved.'
# 工具名称
G_TOOL_NAMED = ''
# 工具版本
G_VERSION = ''
# 默认字体 
G_FONT = '微软雅黑'
# 登录/上传等失败重试次数
G_RETRY_TIMES = 1
# 日志级别
G_LOG_LEVEL = 'info'
# 日志回滚大小
G_LOG_SIZE = 10485760
# 工具标题
G_TITLE = ''
# 关于信息
G_ABOUT_INFO = ''
# 欢迎信息
G_WELCOME_INFO = ''
# 默认密码
G_DEFAULT_PASSWORDS = []
# 脚本压缩包名
G_PACKAGE_NAME = 'package.zip'
""" 控件相关 """
# 一键登录按钮的前景色
G_LGN_BTN_FG_COLOR = 'Gray30'
# 鼠标进入控件时控件的背景色
G_ENTER_BG_COLOR = 'Gray70'
# 鼠标进入控件时控件的前景色
G_ENTER_FG_COLOR = 'DarkGreen'
# 鼠标离开控件时控件的背景色
G_LEAVE_BG_COLOR = 'Gray'
# 鼠标离开控件时控件的前景色
G_LEAVE_FG_COLOR = 'Black'
# 控件默认颜色
G_DEFAULT_COLOR = 'Snow'
G_DEFAULT_BG = 'Gray95'
G_MAIN_VIEW_BG = 'Azure3'  # 'Gray'   # 'Azure4' G_DEFAULT_COLOR
G_LGN_WIN_WIDTH = 600
G_LGN_HEAD_HEIGHT = 160
G_LGN_FUNC_HEIGHT = 235
G_LGN_FOOT_HEIGHT = 60
G_LGN_COUNT_LIMIT = 4
G_MAIN_WIN_HEIGHT = 700
G_MAIN_VIEW_HEIGHT = 500
G_MAIN_LEFT_WIDTH = 160
G_MAIN_MIDD_WIDTH = 820
G_MAIN_RIGHT_WIDTH = 350
# G_LABELBTN_WIDTH = 20
G_PAGES_NAME_DATA = None
G_STATE_PAGE_STRUCT = None
G_OTHER_LOG_STRUCT = None
G_INFOWIN_LEVEL_COLOR = {'INFO': 'SeaGreen',
                         'TIPS': 'Purple',
                         'WARN': 'DarkOrange',
                         'ERROR': 'Red'
                         }
# 登录结果提示的前景色
G_TIG_FG_COLOR = {'DEFAULT': 'Snow',
                  'SUCCESS': 'SeaGreen1',
                  'LOGING': 'DarkGrey',
                  'FAILED': 'OrangeRed'
                  }
""" 路径相关 """
G_LOG_DIR = '.\\log'
G_CONF_DIR = '.\\conf'
G_CMDS_DIR = '.\\cmds'
G_LOG_PATH = '\\'.join([G_LOG_DIR, 'tool.log'])
G_DEPEND_FILE = '\\'.join([G_CONF_DIR, 'dependance.json'])
G_SETTING_FILE = '\\'.join([G_CONF_DIR, 'settings.json'])
G_SERVER_DIR = '/home/Bingo'
""" 事件相关 """
G_EVT_NAME_SUBLOGIN = 'SubLogin_%s'
G_EVT_NAME_GUI = 'Gui'
G_EVT_NAME_INFOWIN = 'InfoWindow'
EVT_LOGIN_GUI = 'event_login_gui'
EVT_MAIN_GUI = 'event_main_gui'
EVT_SEE_PSWD_ON = 'event_see_pswd_on'
EVT_SEE_PSWD_OFF = 'event_see_pswd_off'
# 新增登录子板块
EVT_GET_LOGIN_INPUT = 'event_get_login_input_%s'
EVT_SUBLOGIN_ENTRY_TIG = 'event_sublogin_entry_tig_%s'
EVT_CHG_LOGIN_TIG_COLOR = 'event_change_login_tig_color_%s'
EVT_INSERT_INFOWIN_TEXT = 'event_insert_infowin_text'
EVT_CALL_WIN_INFO = 'event_call_window_info'
EVT_CALL_WIN_WARN = 'event_call_window_warn'
EVT_CALL_WIN_ERROR = 'event_call_window_error'
EVT_CALL_WIN_ASK = 'event_call_window_ask'
EVT_TOP_PROG_START = 'event_toplevel_start'
EVT_TOP_PROG_UPDATE = 'event_toplevel_update'
EVT_TOP_PROG_DESTROY = 'event_toplevel_destroy'

def reload():
    global G_TITLE
    global G_WELCOME_INFO
    global G_ABOUT_INFO
    G_TITLE = '%s V%s' % (G_TOOL_NAMED, G_VERSION)
    G_WELCOME_INFO= ' ' * 50 + '【 欢迎使用%s 】' % G_TOOL_NAMED
    G_ABOUT_INFO = '''%s%s
     用途：
              此工具用于对服务器进行批量远程操控；
              可实现快速部署脚本到服务器并执行；
     特点:
              1. 通用下载界面，显示任务进度和进度信息；
              2. 通用复选界面，自由选择任务项并显示进度；
              3. 通用状态回显，显示任务完整打印信息；
     版本：      %s
     作者：      %s
     联系方式：linux_bingo@163.com''' % (' '*30, G_TOOL_NAMED, G_VERSION, __author__)



