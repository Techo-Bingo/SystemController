# -*- coding: UTF-8 -*-

from Model.sc_global import Global
from Model.Data.sc_data import model_gate
from Model.Controller.sc_logger import logger
from Utils.sc_func import Common, Singleton, JSONParser

class Loader(Singleton):

    def check_file(self):
        Global.G_PID_DIR = "{}\\{}".format(Global.G_RUN_DIR, Common.get_pid())
        Common.mkdir(Global.G_RUN_DIR)
        Common.mkdir(Global.G_DOWNLOAD_DIR)
        Common.mkdir(Global.G_PID_DIR)
        logger.info(Global.G_TEXT_LOGO)

        for path in [Global.G_RESOURCE_DIR,
                     Global.G_DEPENDENCE_FILE,
                     Global.G_SETTINGS_FILE,
                     Global.G_SCRIPTS_DIR]:
            if not Common.is_exists(path):
                model_gate.exception_data.set_data("{} is not exist".format(path))
                logger.error("{} is not exist".format(path))
                return False
        return True

    def json_parser(self, reload=False):
        try:
            # dependence.json解析
            _depend_data = JSONParser.parser(Global.G_DEPENDENCE_FILE)
            # settings.json解析
            _setting_data = JSONParser.parser(Global.G_SETTINGS_FILE)
            # 设置数据初始化
            model_gate.settings_data.parser(_setting_data)
            # 界面数据初始化
            model_gate.dependence_data.parser(_depend_data, reload)
        except Exception as e:
            model_gate.exception_data.set_data(e)
            logger.error(e)
            return False
        return True

    def settings_writer(self, key, value):
        settings = JSONParser.parser(Global.G_SETTINGS_FILE)
        settings['Settings'][key] = value
        JSONParser.write(Global.G_SETTINGS_FILE, settings)

    def init(self):
        if self.check_file() and self.json_parser():
            return True
        return False

    def close(self, data=None):
        Common.rm_dir(Global.G_PID_DIR)


loader = Loader()

