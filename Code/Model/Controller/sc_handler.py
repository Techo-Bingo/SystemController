# -*- coding: UTF-8 -*-

import traceback
from copy import deepcopy
from Model.sc_global import Global
from Model.Controller.sc_loader import loader
from Model.Controller.sc_logger import logger
from Model.Data.sc_data import model_gate
from Utils.sc_ssh import SSH, SSHUtil
from Utils.sc_func import Common, Timer

class LoginHandler(object):
    """ 登录处理类 """

    def login_server(self, ip_data, pack_path):
        def ssh_login():
            ret, err = SSHUtil.user_login(ssh, user)
            if not ret:
                raise Exception("{} {}登录失败\n重试次数:{}\n详细信息:{}".format(ip, user, times, err))
            ret, err = SSHUtil.user_login(ssh, 'root')
            if not ret:
                raise Exception("{} root登录失败\n重试次数:{}\n详细信息:{}".format(ip, times, err))
        def init_server():
            # 如果上次登录用户跟这次不一致，会导致后面解压失败; 这里每次登录都清空目录
            cmd = "rm -rf {0}/*; mkdir {0}; chmod 777 {0}".format(server_dir)
            SSHUtil.exec_ret(ssh, cmd, root=True)
        def upload_package():
            remote_path = "{0}/{1}".format(server_dir, Global.G_PACK_ZIP)
            unzip_cmd = "cd {0} && unzip -o {1} && chmod 777 {0}/*".format(server_dir, Global.G_PACK_ZIP)
            ret, err = SSHUtil.upload_file(ssh, pack_path, remote_path)
            if not ret:
                raise Exception("{} 登录失败\n重试次数:{}\nUpload package failed:{}".format(ip, times, err))
            ret, err = SSHUtil.exec_ret(ssh, unzip_cmd, root=True)
            if not ret:
                raise Exception("{} 登录失败\n重试次数:{}\nDecompression failed:{}".format(ip, times, err))
        def post_handle():
            # dos2unix
            dos2unix_cmd = '''
            for file in {0}/*.sh
            do
                cp $file ${{file}}_tmp
                cat ${{file}}_tmp | tr -d "\\r" >$file
                rm ${{file}}_tmp &
            done
            '''.format(server_dir)
            SSHUtil.exec_ret(ssh, dos2unix_cmd)
        def update_login_data(state):
            login_state_data[ip] = {'PWD': [user, upwd, rpwd],
                                    'SSH': ssh,
                                    'STATE': state}
            model_gate.login_state_data.set_data(login_state_data)

        ip, user, upwd, rpwd = ip_data
        login_state_data = model_gate.login_state_data.get_data()
        retry_times_limit = model_gate.settings_data.retry_times
        server_dir = model_gate.settings_data.server_dir
        for times in range(1, retry_times_limit + 1):
            ssh = SSH(ip, user, upwd, rpwd)
            update_login_data('LOGGING')
            try:
                ssh_login()
                init_server()
                upload_package()
                post_handle()
            except Exception as e:
                logger.warn(e)
                if times == retry_times_limit:
                    update_login_data('FAILED')
                    return False, str(e)
                logger.info('{} retry login times: {}'.format(ip, times))
                continue
            # login success
            update_login_data('SUCCESS')
            logger.info('{} login success'.format(ip))
            break
        return True, None

    def try_login(self, ip_data_list):
        zip_file = "{0}\\{1}".format(Global.G_PID_DIR, Global.G_PACK_ZIP)
        Common.zip_dir(Global.G_SCRIPTS_DIR, zip_file)
        model_gate.login_state_data.set_data({})   # 初始化登录状态数据
        for ip_data in ip_data_list:
            index = ip_data_list.index(ip_data)
            model_gate.login_return_data.set_data([index, 'LOGGING', '{} 登录中...'.format(ip_data[0])])
            ret, err = self.login_server(ip_data, zip_file)
            if ret:
                model_gate.login_return_data.set_data([index, 'SUCCESS', None])
            else:
                model_gate.login_return_data.set_data([index, 'FAILED', None])
                break   # 有失败则停止并返回
        if ret:
            settings_handler.update_prefer_ips()
            TimerHandler()   # 开启定时器任务 #
        model_gate.login_return_data.set_data(['ALL', ret, '登录成功' if ret else err])

class SettingsHandler(object):

    def update_prefer_ips(self):
        # 更新常用IP
        curr_ips = list(model_gate.login_state_data.get_data().keys())
        last_ips = model_gate.settings_data.preference_ip
        new_ips = last_ips + curr_ips
        new_ips = list(set(new_ips))
        new_ips.sort()
        loader.settings_writer('preference_ip', new_ips)

    def update_settings(self, data):
        for key, value in data.items():
            loader.settings_writer(key, value)

class ExecHandler(object):
    """ 任务执行处理类 """
    def __init__(self):
        self.shell = None
        self.in_root = None
        self.in_back = None
        self.task = None
        self.inner_caller = None
        self.is_break = False

    def init(self, script, in_root, in_back):
        self.inner_caller = "sh {0}/inner_function.sh".format(model_gate.settings_data.server_dir)
        self.shell = script
        self.in_root = in_root
        self.in_back = in_back
        self.task = script.split('.')[0].upper()

    def _mutex(self, ip, lock=True):
        """ 防重入 """
        _lock_file = '{0}\\{1}-{2}.lock'.format(Global.G_PID_DIR, self.task, ip)
        # 释放锁
        if not lock:
            try:
                Common.remove(_lock_file)
            except:
                pass
            return True
        # 尝试加锁
        if Common.is_file(_lock_file):
            return False
        Common.write_to_file(_lock_file, 'lock')
        return True

    def get_ssh(self, ip=None):
        return model_gate.login_state_data.get_data()[ip]['SSH']

    def insert_text_info(self, ip, progress, info, level='INFO'):
        if info in [None, "", "NULL"]:
            return
        model_gate.insert_text_data.set_data(["{0} [{1}] ({2}%): {3}".format(ip, self.task, progress, info), level])

    def return_exec_enter_result(self, ip, info):
        model_gate.enter_exec_result_data.set_data([ip, info])

    def return_exec_start_result(self, ip, progress, info, success):
        model_gate.start_exec_result_data.set_data([ip, progress, info, success])

    def execute_out(self, ssh, cmd):
        result = SSHUtil.exec_info(ssh, cmd, True)[0]
        return result.split(Global.G_INNER_SPLIT)[1].strip()

    def exec_shell(self, ssh, params):
        if self.in_back:
            cmd = "{0} async_call_shell {1} {2} {3}".format(self.inner_caller, self.task, self.shell, params)
        else:
            cmd = "{0} sync_call_shell {1} {2} {3}".format(self.inner_caller, self.task, self.shell, params)
        SSHUtil.exec_ret(ssh, cmd, self.in_root)

    def kill_shell(self, ssh):
        cmd = "{0} kill_shell {1} {2}".format(self.inner_caller, self.task, self.shell)
        SSHUtil.exec_ret(ssh, cmd, True)

    def check_result(self, ssh, ip, offset):
        progress_cmd = "{0} get_task_progress {1}".format(self.inner_caller, self.task)
        print_cmd = "{0} get_task_stdout {1}".format(self.inner_caller, self.task)
        progress, last, retry, result = 0, 0, 1, ""
        timeout, consume, period = 10, 0, 0.5
        while True:
            Common.sleep(period)
            try:
                result = self.execute_out(ssh, progress_cmd)
                if not result:
                    if consume > timeout:
                        raise Exception("Timeout for result")
                    consume += period
                    continue
                progress, status, info = result.split('|')
                progress = int(int(progress) * (1-offset/100) + offset)
                result = self.execute_out(ssh, print_cmd)
                if status == 'FAILED':
                    raise Exception(info)
                self.return_exec_start_result(ip, progress, result, True)
                if last == progress:
                    continue
                last = progress
                self.insert_text_info(ip, progress, info)
                if progress == 100:
                    if not self.download_file(ssh, ip, info):
                        raise Exception("Download {} failed !".format(info))
                    break
            except Exception as e:
                retry += 1
                if retry < model_gate.settings_data.retry_times:
                    continue
                self.return_exec_start_result(ip, progress, result, False)
                self.insert_text_info(ip, progress, "{}, retry:{}".format(str(e), retry), 'ERROR')
                break

    def download_file(self, ssh, ip, file):
        if file in ["", "NULL"]:
            self.insert_text_info(ip, 100, 'Success')
            return True
        download_dir = "{0}\\{1}".format(Global.G_DOWNLOAD_DIR, ip)
        filename = "{0}\\{1}".format(download_dir, Common.basename(file))
        Common.mkdir(download_dir)
        self.insert_text_info(ip, 100, 'Downloading to {}'.format(filename))
        if not SSHUtil.download_file(ssh, remote=file, local=filename):
            return False
        self.insert_text_info(ip, 100, "Download success")
        return True

    def upload_file(self, ssh, ip, uploads, offset):
        # 不直接在上传的callback中调用更新状态的Caller,因为会影响上传的速度，
        # callback中只更新内存，状态更新在一个线程中定时去调用
        def upload_back(current, total):
            size[0] = current
            size[1] = total
        def get_progress():
            return int(size[0] / size[1] * offset)
        def update_thread():
            while not is_done:
                self.return_exec_start_result(ip, get_progress(), '', True)
                Common.sleep(0.2)
        size, is_done = [0, 1], False
        server_upload = Global.G_SERVER_UPLOAD % model_gate.settings_data.server_dir
        for local in uploads:
            remote = "{0}/{1}".format(server_upload, Common.basename(local))
            Common.create_thread(func=update_thread, args=())
            self.insert_text_info(ip, get_progress(), 'Uploading {}'.format(local))
            ret, err = SSHUtil.upload_file(ssh, local, remote, upload_back)
            is_done = True
            if not ret:
                self.insert_text_info(ip, get_progress(), 'Upload {} failed: {}'.format(local, err), 'ERROR')
                self.return_exec_start_result(ip, get_progress(), '', False)
                return False
            self.return_exec_start_result(ip, get_progress(), '', True)
        return True

    def exec_enter_impl(self, ip):
        ssh = self.get_ssh(ip)
        self.exec_shell(ssh, 'ENTER')
        print_cmd = "{} get_task_stdout {}".format(self.inner_caller, self.task)
        out_print = self.execute_out(ssh, print_cmd)
        self.return_exec_enter_result(ip, out_print)

    def exec_start_impl(self, ip, uploads, params):
        def combine_params():
            out = ""
            for p in params:
                p = '__None__' if p == '' else p
                out += " '%s'" % p
            return out
        # 上传文件
        if not self._mutex(ip):
            self.insert_text_info(ip, 0, '重复执行, 请等待上个任务执行完毕...', level='WARN')
            return
        ssh = self.get_ssh(ip)
        self.return_exec_start_result(ip, 1, "处理中，请稍候...", True)
        # 文件上传完只是进度的80%
        offset = 80 if uploads else 1
        if not self.upload_file(ssh, ip, uploads, offset):
            self._mutex(ip, False)
            return
        params = combine_params()
        self.insert_text_info(ip, offset, 'Starting execute...')
        self.exec_shell(ssh, params)
        self.check_result(ssh, ip, offset)
        # 清除锁
        self._mutex(ip, False)

    def execute_enter(self, data):
        ips, script = data
        self.init(script, True, False)
        for ip in ips:
            Common.create_thread(func=self.exec_enter_impl, args=(ip,))
            logger.info("execute_enter {} for {}".format(self.task, ip))

    def execute_start(self, data):
        def _execute_now():
            for ip in ips:
                Common.create_thread(func=self.exec_start_impl, args=(ip, uploads[ip], params[ip]))
                logger.info("execute_start {} for {}, params:{}, uploads:{}".format(self.task, ip, params[ip], uploads[ip]))
        def for_delay_loop():
            if delay and not self._mutex('DELAY'):
                model_gate.exception_data.set_data("已经存在延迟任务\n如需重置,请先点击'停止'")
                return
            if loop and not self._mutex('LOOP'):
                model_gate.exception_data.set_data("已经存在循环任务\n如需重置,请先点击'停止'")
                return
            if delay:
                start_time = Common.time()
                while True:
                    if self.is_break:
                        return
                    Common.sleep(1)
                    left_sec = delay * 60 - int(Common.time() - start_time)
                    left_sec = 0 if left_sec < 0 else left_sec
                    model_gate.delay_loop_timer_data.set_data([left_sec, left_sec])
                    if left_sec == 0:
                        self._mutex('DELAY', False)
                        break
            _execute_now()
            if loop:
                start_time = Common.time()
                while True:
                    if self.is_break:
                        return
                    Common.sleep(1)
                    left_sec = loop * 60 - int(Common.time() - start_time)
                    left_sec = 0 if left_sec < 0 else left_sec
                    model_gate.delay_loop_timer_data.set_data([0, left_sec])
                    if left_sec == 0:
                        _execute_now()
                        start_time = Common.time()

        ips, script, root, delay, loop, params, uploads = data
        self.init(script, root, True)
        Common.create_thread(for_delay_loop)

    def execute_stop(self, data):
        ips, script = data
        self.init(script, True, True)
        self.is_break = True
        self._mutex('DELAY', False)
        self._mutex('LOOP', False)
        for ip in ips:
            self.kill_shell(self.get_ssh(ip))
            self._mutex(ip, False)
            self.insert_text_info(ip, 0, "kill success")
            self.return_exec_start_result(ip, 100, '', False)
            logger.info("execute_stop {} for {}".format(self.task, ip))

class TimerHandler(object):
    def __init__(self):
        self.is_first_run = {}
        self.remind_dict = {}
        self.ssh_timer = None
        self.json_timer = None
        self.cache_timer = None
        self.file_timer = None
        self.start()

    def start(self):
        period_c = model_gate.settings_data.refresh_cache['period']
        period_f = model_gate.settings_data.refresh_file['period']
        # ssh保活定时器 #
        self.ssh_timer = Timer(func=self.ssh_keepalive, period=model_gate.settings_data.keepalive_period)
        self.ssh_timer.start()
        # json配置更新定时器 #
        self.json_timer = Timer(func=self.refresh_json_data, period=model_gate.settings_data.refresh_json_period)
        self.json_timer.start()
        # server cache更新定时器 #
        self.cache_timer = Timer(func=self.refresh_cache_data, period=period_c, do_first=True)
        self.cache_timer.start()
        # server file更新定时器 #
        self.file_timer = Timer(func=self.refresh_file_data, period=period_f, do_first=True)
        self.file_timer.start()

    def refresh_json_data(self, args=None):
        def record_change(key, last, curr):
            if last != curr:
                logger.info('[change] {} changed to {}'.format(key, curr))
        logger.debug('[timer] refresh json data start...')
        last_settings = deepcopy(model_gate.settings_data)
        last_widgets = deepcopy(model_gate.dependence_data.widget_data)
        last_trees = deepcopy(model_gate.dependence_data.tree_data)
        if not loader.json_parser(True):
            model_gate.settings_data = deepcopy(last_settings)
            model_gate.dependence_data.widget_data = deepcopy(last_widgets)
            model_gate.dependence_data.tree_data = deepcopy(last_trees)
            del last_settings
            del last_widgets
            del last_trees
            return
        curr_settings = model_gate.settings_data
        curr_dependence = model_gate.dependence_data
        try:
            logger.change_level(curr_settings.log_level)
            record_change('log_level', last_settings.log_level, curr_settings.log_level)
            record_change('tool_alias', last_settings.tool_alias, curr_settings.tool_alias)
            record_change('tool_version', last_settings.tool_version, curr_settings.tool_version)
            record_change('keepalive_period', self.ssh_timer.period, curr_settings.keepalive_period)
            record_change('refresh_json_period', self.json_timer.period, curr_settings.refresh_json_period)
            record_change("refresh_cache['period']", self.cache_timer.period, curr_settings.refresh_cache['period'])
            record_change("refresh_cache['scripts']", last_settings.refresh_cache['scripts'], curr_settings.refresh_cache['scripts'])
            record_change("refresh_file['period']", self.file_timer.period, curr_settings.refresh_file['period'])
            record_change("refresh_cache['scripts']", last_settings.refresh_file['scripts'], curr_settings.refresh_file['scripts'])

            self.ssh_timer.update_period(curr_settings.keepalive_period)
            self.json_timer.update_period(curr_settings.refresh_json_period)
            self.cache_timer.update_period(curr_settings.refresh_cache['period'])
            self.file_timer.update_period(curr_settings.refresh_file['period'])
            if last_settings.tool_alias != curr_settings.tool_alias or \
                    last_settings.tool_version != curr_settings.tool_version:
                title = '{} v{}'.format(curr_settings.tool_alias, curr_settings.tool_version)
                model_gate.app_title_data.set_data((title, None))
                logger.info('[change] tool title changed to {}'.format(title))
            if last_trees != curr_dependence.tree_data:
                model_gate.app_trees_data.set_data(curr_dependence.tree_data)
                logger.info('[change] tool trees changed')
            if last_widgets != curr_dependence.widget_data:
                model_gate.app_widgets_data.set_data(curr_dependence.widget_data)
                logger.info('[change] tool widgets changed')
        except:
            logger.error('Exception apply: {}'.format(traceback.format_exc()))
        del last_settings
        del last_widgets
        del last_trees
        logger.debug('[timer] refresh json data end')

    def ssh_keepalive(self, args=None):
        def ssh_check():
            for t in range(1, retry_times + 1):
                ret1 = SSHUtil.user_login(ssh, user)[0]
                ret2 = SSHUtil.user_login(ssh, 'root')[0]
                ret3 = SSHUtil.exec_ret(ssh, 'echo')[0]
                ret4 = SSHUtil.upload_file(ssh, Global.G_SETTINGS_FILE, remote_file)[0]
                if all([ret1, ret2, ret3, ret4]):
                    return True
            return False
        logger.debug('[timer] ssh keepalive timer start...')
        remote_file = "{0}/__SSH__/1".format(model_gate.settings_data.server_dir)
        retry_times = model_gate.settings_data.retry_times
        remind_dict, success_ip_ssh, failed_ip_ssh = {}, {}, {}
        login_state_data = model_gate.login_state_data.get_data()
        for ip, data in login_state_data.items():
            ssh = data['SSH']
            user, upwd, rpwd = data['PWD']
            if not ssh_check():
                if (ip not in self.remind_dict) or (not self.remind_dict[ip]):
                    logger.warn("(keepalive) ssh instance of {0} is invalid, rebuild now".format(ip))
                    model_gate.insert_text_data.set_data(["{0} is disconnected, Re-login now".format(ip), 'WARN'])
                    self.remind_dict[ip] = True
                # 尝试重新建立ssh
                del ssh
                ssh = SSH(ip, user, upwd, rpwd)
                if ssh_check():
                    logger.info("(keepalive) rebuild ssh instance of {0} success".format(ip))
                    model_gate.insert_text_data.set_data(["{0} Re-login success".format(ip), 'INFO'])
                    self.remind_dict[ip] = False
                    success_ip_ssh[ip] = ssh
                else:
                    failed_ip_ssh[ip] = ssh
            else:
                if login_state_data[ip]['STATE'] != 'SUCCESS':
                    success_ip_ssh[ip] = ssh
        # 刷新ssh实例和状态
        for ip, ssh in success_ip_ssh.items():
            login_state_data[ip]['SSH'] = ssh
            login_state_data[ip]['STATE'] = 'SUCCESS'
        for ip, ssh in failed_ip_ssh.items():
            login_state_data[ip]['SSH'] = ssh
            login_state_data[ip]['STATE'] = 'FAILED'
        if success_ip_ssh or failed_ip_ssh:       # 有数据变更才更新, 避免频繁刷新
            model_gate.login_state_data.set_data(login_state_data)
        logger.debug('[timer] ssh keepalive end, login_state_data: {}'.format(login_state_data))

    def refresh_cache_data(self, args=None):
        logger.debug('[timer] refresh cache data start...')
        server_dir = model_gate.settings_data.server_dir
        scripts = model_gate.settings_data.refresh_cache['scripts']
        server_cache_data = model_gate.server_cache_data.get_data()
        try:
            for ip, data in model_gate.login_state_data.get_data().items():
                ssh = data['SSH']
                for script in scripts:
                    cmd = "{}/{}".format(server_dir, script)
                    result = SSHUtil.exec_info(ssh, cmd, True)[0]
                    result = result.split(Global.G_INNER_SPLIT)[1].strip()
                    for line in result.split('\n'):
                        key, value = line.split(Global.G_CACHE_SPLIT)
                        key = key.strip()
                        value = value.strip().split()
                        logger.debug("modify cache: {}: {}".format(ip, {key: value}))
                        if ip in server_cache_data:
                            server_cache_data[ip][key] = value
                        else:
                            server_cache_data[ip] = {}
                            server_cache_data[ip][key] = value
            model_gate.server_cache_data.set_data(server_cache_data)
        except Exception as e:
            logger.error("refresh_cache_data {}".format(traceback.format_exc()))
        logger.debug('[timer] refresh cache data end, server_cache_data: {}'.format(server_cache_data))

    def refresh_file_data(self, args=None):
        logger.debug('[timer] refresh file data start...')
        server_dir = model_gate.settings_data.server_dir
        scripts = model_gate.settings_data.refresh_file['scripts']
        server_download = Global.G_SERVER_DOWNLOAD % server_dir
        try:
            for ip, data in model_gate.login_state_data.get_data().items():
                ssh = data['SSH']
                local_download = "{}\\{}".format(Global.G_DOWNLOAD_DIR, ip)
                data_dir = "{}\\__FILE_DATA__".format(local_download)
                Common.mkdir(local_download)
                Common.mkdir(data_dir)
                # 初始运行时先把之前已经运行的进程杀死，每次都用最新代码跑
                if ip not in self.is_first_run:
                    [SSHUtil.exec_ret(ssh, "killall {}".format(script), True) for script in scripts]
                    self.is_first_run[ip] = True
                cmd = ''
                for script in scripts:
                    cmd = "{0}\n{1}/{2}".format(cmd, server_dir, script)
                    SSHUtil.exec_ret(ssh, cmd, True)
                # 再压缩DOWNLOAD目录
                cmd = 'cd {0} && zip refresh_file.zip *;chmod 777 *.zip'.format(server_download)
                SSHUtil.exec_ret(ssh, cmd, True)
                # 然后下载文件
                SSHUtil.download_file(ssh,
                                      "{}/refresh_file.zip".format(server_download),
                                      '{}\\refresh_file.zip'.format(local_download))
                # 最后解压
                Common.unzip_file('{}\\refresh_file.zip'.format(local_download), data_dir)
        except Exception as e:
            logger.error("RefreshTimer refresh_file_impl {}".format(str(e)))
        logger.debug('[timer] refresh file data end')

login_handler = LoginHandler()
execute_handler = ExecHandler()
settings_handler = SettingsHandler()
