# -*- coding: UTF-8 -*-
"""
ViewModel板块，处理各种用户操作
"""
import my_global as Global
from my_logger import Logger
from my_viewmodel import ViewModel
from my_bond import Caller
from my_util import Utils
from my_common import Common
from my_ssh import SSH, SSHUtil
from my_base import InputError, ExecError, ReportError


class LoginHandler:
    """ 登录处理类 """
    _ip_list = []
    _cache_passwds = {}
    _widget = None

    @classmethod
    def _logon_ssh_inst(cls, type, data):
        return ViewModel.cache('LOGON_SSH_DICT', type=type, data=data)

    @classmethod
    def _sublogin_callback(cls, event, msg=None):
        """ SubLogin事件回调(caller类) """
        return Caller.call(event=event, msg=msg)

    @classmethod
    def _sublogin_status_tig(cls, seq, status):
        cls._sublogin_callback(Global.EVT_CHG_LOGIN_TIG_COLOR % seq, status)

    @classmethod
    def _sublogin_entry_tig(cls, seq, widget):
        cls._sublogin_callback(Global.EVT_SUBLOGIN_ENTRY_TIG % seq, widget)

    @classmethod
    def _check_ip_passwd_vaild(cls, ip):
        cls._widget = 'ip'
        if not ip:
            raise InputError("请输入服务器IP地址")
        if not Common.is_ip(ip):
            raise InputError("请输入正确的IP地址")
        if ip in cls._ip_list:
            raise InputError("%s 输入重复" % ip)
        cls._ip_list.append(ip)

    @classmethod
    def _check_user_and_password(cls, ip_tuple):
        if not ip_tuple[1]:
            cls._widget = 'user'
            raise InputError("请输入用户名")
        if not ip_tuple[2]:
            cls._widget = 'userpwd'
            raise InputError("请输入用户密码")
        if not ip_tuple[3]:
            cls._widget = 'rootpwd'
            raise InputError("请输入root密码")

    @classmethod
    def _check_inputs(cls, seq, ip_passwd_tuple):
        try:
            cls._check_ip_passwd_vaild(ip_passwd_tuple[0])
            cls._check_user_and_password(ip_passwd_tuple)
        except InputError as e:
            # 登录子模块状态提示器显示红色(失败)
            cls._sublogin_status_tig(seq, 'FAILED')
            # 对应输入框控件闪烁提示
            cls._sublogin_entry_tig(seq, cls._widget)
            # window弹窗提示
            Utils.windows_error(e)
            Logger.error('SubLogin_{0} ip:{1}, err_info:{2}'.format(seq, ip_passwd_tuple[0], e))
            return False
        else:
            cls._sublogin_status_tig(seq, 'LOGING')
            return True

    @classmethod
    def _login_server(cls, seq, ip_passwd_tuple):
        ip, user, userpwd, rootpwd = ip_passwd_tuple
        for retry in range(1, Global.G_RETRY_TIMES + 1):
            ssh = SSH(ip, user, userpwd, rootpwd)
            try:
                ret, err = SSHUtil.user_login(ssh, user)
                if not ret:
                    cls._widget = 'userpwd'
                    raise ExecError("%s %s登录失败!\n详细:%s 重试:%s" % (ip, user, err, retry))
                ret, err = SSHUtil.user_login(ssh, 'root')
                if not ret:
                    cls._widget = 'rootpwd'
                    raise ExecError("%s root登录失败!\n详细:%s 重试:%s" % (ip, err, retry))
            except ExecError as e:
                Logger.warn(e)
                if retry == Global.G_RETRY_TIMES:
                    # 删除IP对应的ssh实例
                    cls._logon_ssh_inst('SUB', ip)
                    # 登录子模块状态提示器显示失败
                    cls._sublogin_status_tig(seq, 'FAILED')
                    # 对应输入框控件闪烁提示
                    cls._sublogin_entry_tig(seq, cls._widget)
                    # 顶层进度窗停止
                    Utils.top_progress_stop()
                    # window弹窗提示
                    Utils.windows_error(e)
                    return False
                # 更新顶层进度窗信息
                Utils.top_progress_update("%s 第%s次尝试" % (ip, retry+1))
                continue
            else:
                # 记录登录成功IP的ssh实例
                cls._logon_ssh_inst('ADD', {ip: ssh})
                # 登录子模块状态提示器显示成功
                cls._sublogin_status_tig(seq, 'SUCCESS')
                Logger.info("%s login success, retry:%s" % (ip, retry))
                return True

    @classmethod
    def _upload_package(cls, args=None):
        # 先压缩脚本再上传
        zip_name = "package.zip"
        zip_file = "{0}\\{1}".format(Global.G_CMDS_DIR, zip_name)
        remote_path = "{0}/{1}".format(Global.G_SERVER_DIR, zip_name)
        Common.zip_dir(Global.G_SHELL_DIR, zip_file)
        unzip_cmd = "cd {0}; unzip -o {1}; chmod 777 {0}/*; dos2unix {0}/*".format(Global.G_SERVER_DIR, zip_name)
        _ip_del_list = []
        for ip, ssh in cls._logon_ssh_inst('QUE', None).items():
            # 如果上次登录用户跟这次不一致，会导致后面解压失败; 这里每次登录都清空目录
            SSHUtil.exec_ret(ssh, "rm -rf {0}/*; mkdir {0}; chmod 777 {0}".format(Global.G_SERVER_DIR), root=True)
            for retry in range(1, Global.G_RETRY_TIMES + 1):
                try:
                    # 上传文件
                    ret, err = SSHUtil.upload_file(ssh, zip_file, remote_path)
                    if not ret:
                        raise ExecError("{0}: Upload package failed:{1}, retry:{2}".format(ip, err, retry))
                    # 解压文件, 成功返回0
                    ret, err = SSHUtil.exec_ret(ssh, unzip_cmd)
                    if ret:
                        raise ExecError("{0} Decompression failed:{1}, retry:{2}".format(ip, err, retry))
                except ExecError as e:
                    if retry == Global.G_RETRY_TIMES:
                        _ip_del_list.append(ip)
                    Utils.tell_info(e, level='ERROR')
                    Logger.warn(e)
                    continue
                else:
                    info = "{0} Environment prepare OK".format(ip)
                    Logger.info(info)
                    Utils.tell_info(info)
                    break
        [cls._logon_ssh_inst('SUB', ip) for ip in _ip_del_list]
        Common.remove(zip_file)
        # 启动数据更新定时器
        RefreshTimer.start_timer()
        # ssh保活
        cls._keep_ssh_alive()

    @classmethod
    def _keep_ssh_alive(cls, args=None):
        send_ips = []
        def if_send(_ip):
            if _ip not in send_ips:
                send_ips.append(_ip)
                return True
            return False
        while True:
            Common.sleep(5)
            new_ip_ssh_instance = {}
            for ip, ssh in cls._logon_ssh_inst('QUE', None).items():
                ret = SSHUtil.exec_ret(ssh, 'echo')[0]
                if not ret:
                    continue
                if if_send(ip):
                    Logger.warn("(keepalive) ssh instance of {0} is invalid, rebuild now".format(ip))
                    Utils.tell_info("{0} is disconnected, Re-login now".format(ip), level='WARN')
                user, userpwd, rootpwd = cls._cache_passwds[ip]
                new_ssh = SSH(ip, user, userpwd, rootpwd)
                ret1 = SSHUtil.user_login(new_ssh, user)[0]
                ret2 = SSHUtil.user_login(new_ssh, 'root')[0]
                if not ret1 or not ret2:
                    continue
                new_ip_ssh_instance[ip] = new_ssh
                Logger.info("(keepalive) rebuild ssh instance of {0} success".format(ip))
                Utils.tell_info("{0} Re-login success".format(ip))
            # 刷新ssh实例
            for ip, ssh in new_ip_ssh_instance.items():
                cls._logon_ssh_inst('ADD', {ip: ssh})

    @classmethod
    def prepare_env(cls):
        Common.create_thread(func=cls._upload_package)

    @classmethod
    def try_login(cls):
        # return True  # DEBUG
        cls._ip_list, _input_info = [], {}
        # 输入校验
        for seq in ViewModel.cache('SUBLOGIN_INDEX_LIST', type='QUE'):
            ip_passwd_tuple = cls._sublogin_callback(Global.EVT_GET_LOGIN_INPUT % seq)
            if not cls._check_inputs(seq, ip_passwd_tuple):
                return False
            _input_info[seq] = ip_passwd_tuple
        # 登录校验，开启进度条
        Utils.top_progress_start('登录中')
        for seq, ip_passwd_tuple in _input_info.items():
            if not cls._login_server(seq, ip_passwd_tuple):
                return False
            cls._cache_passwds[ip_passwd_tuple[0]] = ip_passwd_tuple[1:]
        # 清理用不到的数据，节省内存
        ViewModel.cache('SUBLOGIN_INDEX_LIST', type='DEL')
        # 关闭进度条并开始后台上传文件
        cls.prepare_env()
        Utils.top_progress_stop()
        del _input_info
        return True


class RefreshTimer:

    @classmethod
    def refresh_cache_impl(cls, interval, interface):
        while True:
            try:
                for ip, ssh in ViewModel.cache('LOGON_SSH_DICT', type='QUE').items():
                    PageHandler.cache_server_info(ip, ssh, interface)
            except Exception as e:
                Logger.error("RefreshTimer refresh_cache_impl {}".format(str(e)))
            Common.sleep(interval)

    @classmethod
    def refresh_file_impl(cls, interval, interface):
        first = {}
        while True:
            try:
                for ip, ssh in ViewModel.cache('LOGON_SSH_DICT', type='QUE').items():
                    local_download = "{}\\{}".format(Global.G_DOWNLOAD_DIR, ip)
                    data_dir = "{}\\__FILE_DATA__".format(local_download)
                    Common.mkdir(local_download)
                    Common.mkdir(data_dir)
                    # 初始运行时先把之前已经运行的进程杀死，每次都用最新代码跑
                    if ip not in first:
                        [SSHUtil.exec_ret(ssh, "killall {}".format(inter), True) for inter in interface]
                        first[ip] = True
                    # 再跑脚本
                    cmd = ''
                    for inter in interface:
                        cmd = "{0}\n{1}/{2}".format(cmd, Global.G_SERVER_DIR, inter)
                        SSHUtil.exec_ret(ssh, cmd, True)
                    # 再压缩DOWNLOAD目录
                    cmd = 'cd {0} && zip refresh_file.zip *'.format(Global.G_SERVER_DOWNLOAD)
                    SSHUtil.exec_ret(ssh, cmd, True)
                    # 然后下载文件
                    SSHUtil.download_file(ssh,
                                          "{}/refresh_file.zip".format(Global.G_SERVER_DOWNLOAD),
                                          '{}\\refresh_file.zip'.format(local_download))
                    # 最后解压
                    Common.unzip_file('{}\\refresh_file.zip'.format(local_download), data_dir)
            except Exception as e:
                Logger.error("RefreshTimer refresh_file_impl {}".format(str(e)))
            Common.sleep(interval)

    @classmethod
    def start_timer(cls):
        try:
            data = ViewModel.cache('REFRESH_TIMER_DICT', type='QUE')
            refresh_cache, refresh_file = data['RefreshCache'], data['RefreshFile']
            interval_c = int(refresh_cache['Interval'])
            interface_c = refresh_cache['Interface']
            interval_f = int(refresh_file['Interval'])
            interface_f = refresh_file['Interface']
        except Exception as e:
            Logger.error("RefreshTimer Exception for parser Timer data: {}".format(str(e)))
            return
        Common.create_thread(func=cls.refresh_cache_impl, args=(interval_c, interface_c))
        Common.create_thread(func=cls.refresh_file_impl, args=(interval_f, interface_f))


class PageHandler(object):
    """ 页面事件处理类 """
    server_cache_key = []
    inner_caller = "sh {0}/inner_function.sh".format(Global.G_SERVER_DIR)

    def __init__(self, ip_list, shell, in_root, in_back):
        self.ip_list = ip_list
        self.shell = shell
        self.in_root = in_root
        self.in_back = in_back
        self.task = shell.split('.')[0].upper()

    @classmethod
    def _mutex(cls, ip, task, lock=True):
        """ 防重入 """
        _lock_file = '{0}\\{1}-{2}.lock'.format(Global.G_TEMP_DIR, task, ip)
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

    @classmethod
    def _get_ssh(cls, ip=None):
        if ip:
            return ViewModel.cache('LOGON_SSH_DICT', type='QUE')[ip]
        return ViewModel.cache('LOGON_SSH_DICT', type='QUE')

    @classmethod
    def _execute_out(cls, ssh, cmd):
        result = SSHUtil.exec_info(ssh, cmd, True)[0]
        return result.split(Global.G_SPLIT_FLAG)[1].strip()

    def _exec_shell(self, ssh, params):
        if self.in_back:
            cmd = "{0} async_call_shell {1} {2} {3}".format(self.inner_caller, self.task, self.shell, params)
        else:
            cmd = "{0} sync_call_shell {1} {2} {3}".format(self.inner_caller, self.task, self.shell, params)
        SSHUtil.exec_ret(ssh, cmd, self.in_root)

    def _kill_shell(self, ssh):
        cmd = "{0} kill_shell {1} {2}".format(self.inner_caller, self.task, self.shell)
        SSHUtil.exec_ret(ssh, cmd, True)

    def tell_info(self, ip, progress, info, level='INFO'):
        if info in [None, "", "NULL"]:
            return
        Utils.tell_info("{0} [{1}] ({2}%): {3}".format(ip, self.task, progress, info), level)

    def _check_result(self, ssh, ip, callback):
        progress_cmd = "{0} get_task_progress {1}".format(self.inner_caller, self.task)
        print_cmd = "{0} get_task_stdout {1}".format(self.inner_caller, self.task)
        progress, last, retry, out_print = 0, 0, 1, ""
        while True:
            Common.sleep(0.5)
            try:
                progress, status, info = self._execute_out(ssh, progress_cmd).split('|')
                progress = int(progress)
                out_print = self._execute_out(ssh, print_cmd)
                if status == 'FAILED':
                    raise ReportError(info)
                callback(ip, progress, True, out_print)
                if last == progress:
                    continue
                last = progress
                self.tell_info(ip, progress, info)
                if progress == 100:
                    if not self._download_file(ssh, ip, info):
                        raise ReportError("Download {0} failed !".format(info))
                    break
            except Exception as e:
                retry += 1
                if retry < Global.G_RETRY_TIMES:
                    continue
                callback(ip, progress, False, out_print)
                self.tell_info(ip, progress, "{0}, retry:{1}".format(str(e), retry), 'ERROR')
                break

    def _download_file(self, ssh, ip, file):
        if file in ["", "NULL"]:
            self.tell_info(ip, 100, 'Success')
            return True
        download_dir = "{0}\\{1}".format(Global.G_DOWNLOAD_DIR, ip)
        filename = "{0}\\{1}".format(download_dir, Common.basename(file))
        Common.mkdir(download_dir)
        self.tell_info(ip, 100, 'Downloading {}'.format(filename))
        if not SSHUtil.download_file(ssh, remote=file, local=filename):
            return False
        self.tell_info(ip, 100, "Download success")
        return True

    def _upload_file(self, ssh, ip, uploads):
        for local in uploads:
            remote = "{0}/{1}".format(Global.G_SERVER_UPLOAD, Common.basename(local))
            self.tell_info(ip, 1, 'Uploading {}'.format(local))
            ret, _ = SSHUtil.upload_file(ssh, local, remote)
            if not ret:
                self.tell_info(ip, 5, 'Upload {} failed !'.format(local), 'ERROR')
                return False
        return True

    def _exec_enter_impl(self, ip, callback):
        ssh = self._get_ssh(ip)
        self._exec_shell(ssh, 'ENTER')
        print_cmd = "{0} get_task_stdout {1}".format(self.inner_caller, self.task)
        out_print = self._execute_out(ssh, print_cmd)
        callback(ip, out_print)

    def _exec_start_impl(self, ip, uploads, params, callback):
        def combine_params():
            out = ""
            for p in params:
                out += " '%s'" % p
            return out
        # 上传文件
        if not self._mutex(ip, self.task):
            self.tell_info(ip, 0, 'Repeat, please wait...', level='WARN')
            return
        ssh = self._get_ssh(ip)
        callback(ip, 1, True, "文件上传中，请稍候...")
        if not self._upload_file(ssh, ip, uploads):
            callback(ip, 5, False, "")
            self._mutex(ip, self.task, False)
            return
        # 执行脚本
        params = combine_params()
        self.tell_info(ip, 10, 'Starting execute...')
        self._exec_shell(ssh, params)
        self._check_result(ssh, ip, callback)
        # 清除锁
        self._mutex(ip, self.task, False)

    def execute_enter(self, callback):
        for ip in self.ip_list:
            Common.create_thread(func=self._exec_enter_impl, args=(ip, callback))
            Logger.info("execute_enter {} for {}".format(self.task, ip))

    def execute_start(self, callback, params, uploads):
        for ip in self.ip_list:
            Common.create_thread(func=self._exec_start_impl, args=(ip, uploads[ip], params[ip], callback))
            Logger.info("execute_start {} for {}, params:{}, uploads:{}".format(self.task, ip, params[ip], uploads[ip]))

    def execute_stop(self, callback):
        for ip in self.ip_list:
            self._kill_shell(self._get_ssh(ip))
            self._mutex(ip, self.task, False)
            self.tell_info(ip, 0, "kill success")
            callback(ip, 0, True, "")
            Logger.info("execute_stop {} for {}".format(self.task, ip))

    @classmethod
    def get_server_cache(cls, ip, which):
        try:
            return ViewModel.cache('SERVER_CACHE_DICT', 'QUE')[ip][which]
        except:
            return []

    @classmethod
    def cache_server_info(cls, ip, ssh, interface):
        for shell in interface:
            print_cmd = "{}/{}".format(Global.G_SERVER_DIR, shell)
            out_print = cls._execute_out(ssh, print_cmd)
            split_str = '____BINGO_CACHE____'
            for line in out_print.split('\n'):
                try:
                    key, value = line.split(split_str)
                    key = key.strip()
                    value = value.strip().split()
                except Exception as e:
                    Logger.error("cache_server_info {}".format(str(e)))
                    continue
                cls.server_cache_key.append(key)
                Logger.debug("modify cache: {}: {}".format(ip, {key: value}))
                all_data = ViewModel.cache('SERVER_CACHE_DICT', 'QUE')
                ip_data = all_data[ip] if ip in all_data else {}
                ip_data.update({key: value})
                ViewModel.cache('SERVER_CACHE_DICT', 'ADD', {ip: ip_data})
        Logger.debug("query cache: {}".format(ViewModel.cache('SERVER_CACHE_DICT', 'QUE')))

