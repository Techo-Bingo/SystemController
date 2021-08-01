# -*- coding: UTF-8 -*-

# from ..sc_global import *
from Binder.sc_topic import *
from Binder.sc_proxy import get_query_data_binder
from Binder.sc_template import DataTemplate, DataCreater

class ExceptionData(DataTemplate):
    pass

class AppCloseData(DataTemplate):
    pass

class TryLoginData(DataTemplate):
    pass

class AddImageData(DataTemplate):
    pass

class StartExecuteData(DataTemplate):
    pass

class StopExecuteData(DataTemplate):
    pass

class EnterExecuteData(DataTemplate):
    pass

class UpdateSettingsData(DataTemplate):
    pass

class ViewGate(object):

    def __init__(self):
        self.query_binder = get_query_data_binder()
        self.app_close_data = DataCreater(AppCloseData)
        self.exception_data = DataCreater(ExceptionData)
        self.try_login_data = DataCreater(TryLoginData)
        self.add_image_data = DataCreater(AddImageData)
        self.start_exec_data = DataCreater(StartExecuteData)
        self.stop_exec_data = DataCreater(StopExecuteData)
        self.enter_exec_data = DataCreater(EnterExecuteData)
        self.update_settings_data = DataCreater(UpdateSettingsData)

    def query_settings_data(self, key=None):
        data = self.query_binder.query(VIEW_QUERY_SETTINGS_DATA)
        return data[key] if key else data

    def query_title_ico_data(self):
        return self.query_binder.query(VIEW_QUERY_TITLE_ICO_DATA)

    def query_env_define_data(self, key):
        return self.query_binder.query(VIEW_QUERY_ENV_DEFINE_DATA, key)

    def query_about_info_data(self):
        return self.query_binder.query(VIEW_QUERY_ABOUT_INFO_DATA)

    def query_photo_image_data(self, key):
        return self.query_binder.query(VIEW_QUERY_PHOTO_IMAGE_DATA, key)

    def query_login_limit_data(self):
        return self.query_binder.query(VIEW_QUERY_LOGIN_LIMIT_DATA)

    def query_preference_ip_data(self):
        return self.query_binder.query(VIEW_QUERY_PREFERENCE_IP_DATA)

    def query_default_pwd_data(self):
        return self.query_binder.query(VIEW_QUERY_DEFAULT_PWD_DATA)

    def query_tree_view_data(self):
        return self.query_binder.query(VIEW_QUERY_TREE_VIEW_DATA)

    def query_widgets_data(self):
        return self.query_binder.query(VIEW_QUERY_WIDGETS_DATA)

    def query_running_task_data(self):
        return self.query_binder.query(VIEW_QUERY_RUNNING_TASK_DATA)

    def query_ips_state_data(self):
        return self.query_binder.query(VIEW_QUERY_IPS_STATE_DATA)

    def query_login_ip_data(self):
        return list(self.query_ips_state_data().keys())

    def query_server_cache_data(self):
        return self.query_binder.query(VIEW_QUERY_SERVER_CACHE_DATA)


view_gate = ViewGate()

