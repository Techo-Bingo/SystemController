# -*- coding: UTF-8 -*-

from Model.Data.sc_data import model_gate
from Model.Controller.sc_logger import logger
from Model.Controller.sc_loader import loader
from Model.Controller.sc_handler import login_handler, execute_handler, settings_handler
from Binder.sc_topic import *
from Binder.sc_proxy import get_active_data_binder, get_passive_data_binder, get_query_data_binder

def printf(data):
    print('Model got data: ', data)

def init():

    active_binder = get_active_data_binder()
    active_binder.bind(model_gate.app_title_data.get_provider(), MODEL_NOTIFY_APP_TITLE_DATA)
    active_binder.bind(model_gate.app_trees_data.get_provider(), MODEL_NOTIFY_APP_TREES_DATA)
    active_binder.bind(model_gate.app_widgets_data.get_provider(), MODEL_NOTIFY_APP_WIDGETS_DATA)
    active_binder.bind(model_gate.exception_data.get_provider(), MODEL_NOTIFY_EXCEPTION_DATA)
    active_binder.bind(model_gate.login_return_data.get_provider(), MODEL_NOTIFY_LOGIN_RETURN_DATA)
    active_binder.bind(model_gate.login_state_data.get_provider(), MODEL_NOTIFY_LOGIN_STATE_DATA)
    active_binder.bind(model_gate.insert_text_data.get_provider(), MODEL_NOTIFY_INSERT_TEXT_DATA)
    active_binder.bind(model_gate.enter_exec_result_data.get_provider(), MODEL_NOTIFY_ENTER_EXEC_RESULT_DATA)
    active_binder.bind(model_gate.start_exec_result_data.get_provider(), MODEL_NOTIFY_START_EXEC_RESULT_DATA)
    active_binder.bind(model_gate.delay_loop_timer_data.get_provider(), MODEL_NOTIFY_DELAY_LOOP_TIMER_DATA)

    passive_binder = get_passive_data_binder()
    passive_binder.bind(VIEW_NOTIFY_EXCEPTION_DATA, logger.error)
    passive_binder.bind(VIEW_NOTIFY_APP_CLOSE_DATA, loader.close)
    passive_binder.bind(VIEW_NOTIFY_APP_CLOSE_DATA, logger.truncate)
    passive_binder.bind(VIEW_NOTIFY_TRY_LOGIN_DATA, login_handler.try_login)
    passive_binder.bind(VIEW_NOTIFY_ADD_IMAGE_DATA, model_gate.dependence_data.append_photo_image)
    passive_binder.bind(VIEW_NOTIFY_ENTER_EXEC_DATA, execute_handler.execute_enter)
    passive_binder.bind(VIEW_NOTIFY_START_EXEC_DATA, execute_handler.execute_start)
    passive_binder.bind(VIEW_NOTIFY_STOP_EXEC_DATA, execute_handler.execute_stop)
    passive_binder.bind(VIEW_NOTIFY_UPDATE_SETTINGS_DATA, settings_handler.update_settings)

    query_binder = get_query_data_binder()
    query_binder.bind(VIEW_QUERY_TITLE_ICO_DATA, model_gate.query_title_ico_data)
    query_binder.bind(VIEW_QUERY_ENV_DEFINE_DATA, model_gate.query_env_define_data)
    query_binder.bind(VIEW_QUERY_LOGIN_LIMIT_DATA, model_gate.query_login_limit_data)
    query_binder.bind(VIEW_QUERY_PREFERENCE_IP_DATA, model_gate.query_preference_ip_data)
    query_binder.bind(VIEW_QUERY_DEFAULT_PWD_DATA, model_gate.query_default_pwd_data)
    query_binder.bind(VIEW_QUERY_PHOTO_IMAGE_DATA, model_gate.query_photo_image_data)
    query_binder.bind(VIEW_QUERY_ABOUT_INFO_DATA, model_gate.query_about_info_data)
    query_binder.bind(VIEW_QUERY_TREE_VIEW_DATA, model_gate.query_tree_view_data)
    query_binder.bind(VIEW_QUERY_WIDGETS_DATA, model_gate.query_widgets_data)
    query_binder.bind(VIEW_QUERY_RUNNING_TASK_DATA, model_gate.query_running_task_data)
    query_binder.bind(VIEW_QUERY_IPS_STATE_DATA, model_gate.query_ips_state_data)
    query_binder.bind(VIEW_QUERY_SERVER_CACHE_DATA, model_gate.query_server_cache_data)
    query_binder.bind(VIEW_QUERY_SETTINGS_DATA, model_gate.query_settings_data)

    if not loader.init():
        return False

    return True


