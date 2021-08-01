# -*- coding: UTF-8 -*-

from copy import deepcopy
from PIL import Image, ImageTk
from Model.sc_global import Global
from Utils.sc_func import Common
from Binder.sc_template import DataTemplate, DataCreater

class Settings(object):
    def __init__(self):
        self.tool_alias = None
        self.tool_version = None
        self.log_level = None
        self.server_dir = None
        self.retry_times = None
        self.login_count_limit = None
        self.keepalive_period = None
        self.refresh_json_period = None
        self.default_passwords = None
        self.refresh_cache = None
        self.refresh_file = None

    def parser(self, settings_data):
        self.globals(settings_data['Settings'])
        self.timer(settings_data['Timer'])

    def globals(self, global_data):
        self.tool_alias = global_data['tool_alias']
        self.tool_version = global_data['tool_version']
        self.log_level = global_data['log_level']
        self.server_dir = global_data['server_home']
        self.retry_times = global_data['retry_times']
        self.login_count_limit = global_data['login_count_limit']
        self.keepalive_period = global_data['keepalive_period']
        self.refresh_json_period = global_data['refresh_json_period']
        self.about_info = '\n'.join(global_data['about_information'])
        self.preference_ip = global_data['preference_ip']
        _default_pwd = global_data['passwords']
        self.default_passwords = [_default_pwd['username'], _default_pwd['userpassword'], _default_pwd['rootpassword']]

    def timer(self, timer_data):
        self.refresh_cache = timer_data['refresh_cache']
        self.refresh_file = timer_data['refresh_file']
        self.refresh_cache['period'] = int(self.refresh_cache['period'])
        self.refresh_file['period'] = int(self.refresh_file['period'])
        if 'scripts' not in self.refresh_cache:
            raise Exception("scripts not found in refresh_cache of Settings")
        if 'scripts' not in self.refresh_file:
            raise Exception("scripts not found in refresh_file of Settings")

    def get_about_info(self):
        info = '''
    名称:    {}
    版本:    {}
{}
    作者:    {}
    联系:    {}
                '''.format(self.tool_alias,
                           self.tool_version,
                           self.about_info,
                           Global.G_AUTHOR_NAME,
                           Global.G_CONTACT_ME)
        return info

class Depandence(object):
    def __init__(self):
        self.photo_images = {}
        self.tree_data = None
        self.widget_data = None

    def parser(self, dependence_data, reload):
        if not reload:     # 定时器刷新时不重新加载image数据, 否则界面会出问题
            self.images(dependence_data['Images'])
        self.tree(dependence_data['Trees'])
        self.widgets(dependence_data['Widgets'])

    def images(self, image_data):
        for key, path in image_data.items():
            path = "{}\\{}".format(Global.G_RESOURCE_DIR, path)
            if not Common.is_file(path):
                raise Exception("%s is not exist !" % path)
            self.append_photo_image((key, path))

    def append_photo_image(self, data):
        key, path = data
        self.photo_images[key] = path if key == 'ICO' else ImageTk.PhotoImage(image=Image.open(path))

    def tree(self, tree_data):
        self.tree_data = tree_data

    def widgets(self, widget_data):
        self.widget_data = widget_data

class AppTitleData(DataTemplate):
    pass

class AppTreesData(DataTemplate):
    pass

class AppWidgetsData(DataTemplate):
    pass

class ExceptionData(DataTemplate):
    pass

class LoginReturnData(DataTemplate):
    ''' 单个IP尝试登录的结果数据 '''
    pass

class LoginStateData(DataTemplate):
    ''' 所有IP登录状态数据 '''
    pass

class InsertTextData(DataTemplate):
    pass

class ServerCacheData(DataTemplate):
    def __init__(self):
        self.init({})

class StartExecResultData(DataTemplate):
    pass

class EnterExecResultData(DataTemplate):
    pass

class DelayLoopTimerData(DataTemplate):
    pass

class ModelGate(object):

    def __init__(self):
        self.settings_data = Settings()
        self.dependence_data = Depandence()
        self.app_title_data = DataCreater(AppTitleData)
        self.app_trees_data = DataCreater(AppTreesData)
        self.app_widgets_data = DataCreater(AppWidgetsData)
        self.exception_data = DataCreater(ExceptionData)
        self.login_return_data = DataCreater(LoginReturnData)
        self.login_state_data = DataCreater(LoginStateData)
        self.insert_text_data = DataCreater(InsertTextData)
        self.server_cache_data = DataCreater(ServerCacheData)
        self.enter_exec_result_data = DataCreater(EnterExecResultData)
        self.start_exec_result_data = DataCreater(StartExecResultData)
        self.delay_loop_timer_data = DataCreater(DelayLoopTimerData)

    def query_settings_data(self, args=None):
        return deepcopy(self.settings_data)

    def query_title_ico_data(self, args=None):
        title = '{} v{}'.format(self.settings_data.tool_alias, self.settings_data.tool_version)
        return (title, self.dependence_data.photo_images['ICO'])

    def query_env_define_data(self, args):
        return eval('Global.{}'.format(args))

    def query_about_info_data(self, args=None):
        return self.settings_data.get_about_info()

    def query_photo_image_data(self, args):
        return self.dependence_data.photo_images[args]

    def query_login_limit_data(self, args=None):
        return self.settings_data.login_count_limit

    def query_preference_ip_data(self, args=None):
        return self.settings_data.preference_ip

    def query_default_pwd_data(self, args=None):
        return self.settings_data.default_passwords

    def query_tree_view_data(self, args=None):
        return self.dependence_data.tree_data

    def query_widgets_data(self, args=None):
        return self.dependence_data.widget_data

    def query_running_task_data(self, args=None):
        return Common.exist_suffix_file(Global.G_PID_DIR, '.lock')[1]

    def query_ips_state_data(self, args=None):
        login_data = self.login_state_data.get_data()
        out = {}
        for ip, item in login_data.items():
            out[ip] = item['STATE']
        return out

    def query_server_cache_data(self, args=None):
        return self.server_cache_data.get_data()


model_gate = ModelGate()

