# -*- coding: UTF-8 -*-
"""
全局定义
"""
__author__ = 'LiBin (Bingo)'
G_LOGO = '''Welcome 
        
            ____  _                       
           / __ )(_)___  ____ _____ 
          / __  / / __ \/ __ `/ __ \\
         / /_/ / / / / / /_/ / /_/ /
        /_____/_/_/ /_/\__, /\____/ 
                      /____/        
        
        '''
# 版权信息
G_COPYRIGHT_INFO = 'Copyright©2019-2021 Bingo. All Rights Reserved.'
# 分隔符
G_SPLIT_FLAG= '____BINGO_FILTER____'
# 工具名称
G_TOOL_NAMED = ''
# 工具版本
G_VERSION = ''
# 默认字体 
G_FONT = '微软雅黑'
# 登录/上传等失败重试次数
G_RETRY_TIMES = 1
# 工具标题
G_TITLE = ''
# 关于信息
G_ABOUT_INFO = ''
# 欢迎信息
G_WELCOME_INFO = ''
# 默认密码
G_DEFAULT_PASSWORDS = []
# 控件默认颜色
G_DEFAULT_COLOR = 'Snow'
# 默认背景色
G_DEFAULT_BG = 'Gray94'
# 操作窗(pages)背景色
G_MAIN_OPER_BG = 'Gray94' #''Snow'
# 一键登录按钮的前景色
G_LGN_BTN_FG_COLOR = 'Gray30'
# 登录界面宽高
G_LGN_WIN_WIDTH = 600
G_LGN_WIN_HEIGHT = 450
# 登陆界面图片栏高度
G_LGN_HEAD_HEIGHT = 160
# 登陆界面按钮栏高度
G_LGN_FOOT_HEIGHT = 60
# 登录界面登录窗高度
G_LGN_FUNC_HEIGHT = G_LGN_WIN_HEIGHT - G_LGN_HEAD_HEIGHT - G_LGN_FOOT_HEIGHT
# 登录界面批量登录个数限制
G_LGN_COUNT_LIMIT = 4
# 主界面宽高
G_MAIN_WIN_WIDTH = 1500
G_MAIN_WIN_HEIGHT = 900
# 主界面操作窗(pages)高度
G_MAIN_OPER_HEIGHT = 600
# 主界面信息提示栏高度
G_MAIN_INFO_HEIGHT = G_MAIN_WIN_HEIGHT - G_MAIN_OPER_HEIGHT
# 主界面树形导航栏宽度
G_MAIN_TREE_WIDTH = 250
# 主界面操作窗(pages)宽度
G_MAIN_OPER_WIDTH = 900
# 主界面外部扩展栏宽度
G_MAIN_HELP_WIDTH = G_MAIN_WIN_WIDTH - G_MAIN_TREE_WIDTH - G_MAIN_OPER_WIDTH
G_INFOWIN_LEVEL_COLOR = {'INFO': 'Blue',  # 'DarkGreen',
                         'TIPS': 'Blue',
                         'WARN': 'DarkOrange',
                         'ERROR': 'Red'}
# 登录结果提示的前景色
G_TIG_FG_COLOR = {'DEFAULT': 'Snow',
                  'SUCCESS': 'SeaGreen1',
                  'LOGING': 'DarkGrey',
                  'FAILED': 'OrangeRed'}
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
# 运行环境相关定义
G_LOG_DIR = '.\\log'
G_CONF_DIR = '.\\conf'
G_CMDS_DIR = '.\\cmds'
G_SHELL_DIR = '.\\cmds\\shell'
G_TEMP_DIR = '.\\cmds\\temp'
G_PID_FILE = '.\\cmds\\temp\\tool.pid'
G_DOWNLOAD_DIR = '.\\download'
G_SERVER_DIR = '/home/Bingo'
G_SERVER_UPLOAD = ''
G_SERVER_DOWNLOAD = ''
# 日志回滚大小
G_LOG_SIZE = 10485760
G_LOG_PATH = '\\'.join([G_LOG_DIR, 'tool.log'])
G_DEPEND_FILE = '\\'.join([G_CONF_DIR, 'dependance.json'])
G_SETTING_FILE = '\\'.join([G_CONF_DIR, 'settings.json'])
G_LOG_LEVEL = 'info'

# 事件相关定义
G_EVT_NAME_SUBLOGIN = 'SubLogin_%s'
G_EVT_NAME_GUI = 'Gui'
G_EVT_NAME_INFOWIN = 'InfoWindow'
EVT_LOGIN_GUI = 'event_login_gui'
EVT_MAIN_GUI = 'event_main_gui'
EVT_SEE_PSWD_ON = 'event_see_pswd_on'
EVT_SEE_PSWD_OFF = 'event_see_pswd_off'
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
EVT_ADD_IMAGE = 'event_add_image'
EVT_REFRESH_GUI = 'event_refresh_gui'
EVT_PAGE_INTERFACE = 'event_page_interface'
EVT_CLOSE_GUI = 'event_close_gui'
EVT_UPLOAD_PROGRESS_UPDATE = 'event_upload_progress_update'


def reload():
    global G_TITLE
    global G_WELCOME_INFO
    global G_SERVER_UPLOAD
    global G_SERVER_DOWNLOAD
    G_TITLE = '%s V%s' % (G_TOOL_NAMED, G_VERSION)
    G_WELCOME_INFO= ' ' * 70 + '【 欢迎使用%s 】' % G_TOOL_NAMED
    G_SERVER_UPLOAD = '%s/__UPLOAD__' % G_SERVER_DIR
    G_SERVER_DOWNLOAD = '%s/__DOWNLOAD__' % G_SERVER_DIR


