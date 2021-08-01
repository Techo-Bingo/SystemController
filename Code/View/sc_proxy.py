# -*- coding: UTF-8 -*-

from View.sc_app import app_gate
from View.sc_module import WidgetTip
from View.Datamation.sc_provide import view_gate
from Binder.sc_topic import *
from Binder.sc_proxy import get_active_data_binder, get_passive_data_binder

def printf(data):
    print('View got data: ', data)

def init():
    # 界面数据变更绑定后端处理方法 #
    active_binder = get_active_data_binder()
    active_binder.bind(view_gate.app_close_data.get_provider(), VIEW_NOTIFY_APP_CLOSE_DATA)
    active_binder.bind(view_gate.exception_data.get_provider(), VIEW_NOTIFY_EXCEPTION_DATA)
    active_binder.bind(view_gate.try_login_data.get_provider(), VIEW_NOTIFY_TRY_LOGIN_DATA)
    active_binder.bind(view_gate.add_image_data.get_provider(), VIEW_NOTIFY_ADD_IMAGE_DATA)
    active_binder.bind(view_gate.enter_exec_data.get_provider(), VIEW_NOTIFY_ENTER_EXEC_DATA)
    active_binder.bind(view_gate.start_exec_data.get_provider(), VIEW_NOTIFY_START_EXEC_DATA)
    active_binder.bind(view_gate.stop_exec_data.get_provider(), VIEW_NOTIFY_STOP_EXEC_DATA)
    active_binder.bind(view_gate.update_settings_data.get_provider(), VIEW_NOTIFY_UPDATE_SETTINGS_DATA)

    # 界面处理方法绑定后端数据变更 #
    passive_binder = get_passive_data_binder()
    passive_binder.bind(MODEL_NOTIFY_EXCEPTION_DATA, WidgetTip.error)
    passive_binder.bind(MODEL_NOTIFY_APP_TITLE_DATA, app_gate.update_app_title)
    passive_binder.bind(MODEL_NOTIFY_APP_TREES_DATA, app_gate.update_app_trees)
    passive_binder.bind(MODEL_NOTIFY_APP_WIDGETS_DATA, app_gate.update_app_widgets)
    passive_binder.bind(MODEL_NOTIFY_LOGIN_RETURN_DATA, app_gate.update_login_return)
    passive_binder.bind(MODEL_NOTIFY_LOGIN_STATE_DATA, app_gate.update_login_state)
    passive_binder.bind(MODEL_NOTIFY_INSERT_TEXT_DATA, app_gate.insert_text_info)
    passive_binder.bind(MODEL_NOTIFY_ENTER_EXEC_RESULT_DATA, app_gate.update_enter_exec_result)
    passive_binder.bind(MODEL_NOTIFY_START_EXEC_RESULT_DATA, app_gate.update_start_exec_result)
    passive_binder.bind(MODEL_NOTIFY_DELAY_LOOP_TIMER_DATA, app_gate.update_delay_loop_timer)


    return True


def app_run():
    app_gate.run()


