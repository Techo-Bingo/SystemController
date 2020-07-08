# -*- coding: UTF-8 -*-
"""
ViewModel板块，处理各种用户操作
"""
from time import sleep
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
            Logger.error('SubLogin_{} ip:{}, err_info:{}'.format(
                seq, ip_passwd_tuple[0], e))
            return False
        else:
            cls._sublogin_status_tig(seq, 'LOGING')
            return True

    @classmethod
    def _login_server(cls, seq, ip_passwd_tuple):
        _retry_times = Global.G_RETRY_TIMES
        _user_login = SSHUtil.user_login
        ip, user, userpwd, rootpwd = ip_passwd_tuple

        for times in range(1, _retry_times + 1):
            ssh = SSH(ip, user, userpwd, rootpwd)
            try:
                ret, err = _user_login(ssh, user)
                if not ret:
                    cls._widget = 'userpwd'
                    raise ExecError("%s %s登录失败!\n详细:%s 重试:%s"
                                    % (ip, user, err, times))
                ret, err = _user_login(ssh, 'root')
                if not ret:
                    cls._widget = 'rootpwd'
                    raise ExecError("%s root登录失败!\n详细:%s 重试:%s"
                                    % (ip, err, times))
            except ExecError as e:
                Logger.warn(e)
                if times == _retry_times:
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
                Utils.top_progress_update("%s 第%s次尝试" % (ip, times+1))
                continue
            else:
                # 记录登录成功IP的ssh实例
                cls._logon_ssh_inst('ADD', {ip: ssh})
                # 登录子模块状态提示器显示成功
                cls._sublogin_status_tig(seq, 'SUCCESS')
                Logger.info("%s login success, retry:%s" % (ip, times))
                return True

    @classmethod
    def _upload_package(cls, args=None):
        pack_path = "%s\\%s" % (Global.G_CMDS_DIR, Global.G_PACKAGE_NAME)
        remote_path = '%s/%s' % (Global.G_SERVER_DIR, Global.G_PACKAGE_NAME)
        unzip_cmd = 'cd {0} && unzip -o {1} && chmod 777 {0}/*'.format(
            Global.G_SERVER_DIR, Global.G_PACKAGE_NAME)
        _retry_times = Global.G_RETRY_TIMES
        # for循环中会对ssh实例字典操作，
        # 所以用一个临时变量接收ssh实例字典数据进行for，否则会报错
        _ip_ssh_dict = {}
        _ip_ssh_dict.update(cls._logon_ssh_inst('QUE', None))

        for ip, ssh in _ip_ssh_dict.items():
            """ 按照重试次数进行上传和解压文件 """
            for times in range(1, _retry_times + 1):
                # 如果上次登录用户跟这次不一致，会导致后面解压失败
                # 这里刚登录时，每次清空目录
                SSHUtil.exec_ret(ssh, 'rm -rf %s/*' % Global.G_SERVER_DIR, root=True)
                try:
                    # 上传文件
                    ret, err = SSHUtil.upload_file(ssh, pack_path, remote_path)
                    if not ret:
                        raise ExecError('%s 上传package失败，详细:%s，重试:%s'
                                        % (ip, err, times))
                    # 解压文件, 成功返回0
                    ret, err = SSHUtil.exec_ret(ssh, unzip_cmd)
                    if ret:
                        raise ExecError('%s 解压package失败，详细:%s，重试:%s'
                                        % (ip, err, times))
                except ExecError as e:
                    # 失败则从字典中删除该IP的ssh实例
                    cls._logon_ssh_inst('SUB', ip)
                    Utils.tell_info(e, level='ERROR')
                    Logger.warn(e)
                    continue
                else:
                    # bug fix
                    # 场景：登录成功，但是第一次上传失败时，上面的Except会删除该IP
                    # 待第二次上传成功后，LOGON_SSH_DICT中其实已经没有该IP,界面将显示为空
                    # 解决：这里成功后也加一次IP
                    cls._logon_ssh_inst('ADD', {ip: ssh})
                    info = '%s 环境准备就绪' % ip
                    Logger.info(info)
                    Utils.tell_info(info)
                    break
        del _ip_ssh_dict

    @classmethod
    def prepare_env(cls):
        Common.create_thread(func=cls._upload_package)

    @classmethod
    def try_login(cls):
        # return True
        cls._ip_list = []
        _input_info = {}

        """ 输入校验 """
        for seq in ViewModel.cache('SUBLOGIN_INDEX_LIST', type='QUE'):
            ip_passwd_tuple = cls._sublogin_callback(
                Global.EVT_GET_LOGIN_INPUT % seq)

            if not cls._check_inputs(seq, ip_passwd_tuple):
                return False
            _input_info[seq] = ip_passwd_tuple

        """ 登录校验，开启进度条 """
        Utils.top_progress_start('登录中')

        for seq, ip_passwd_tuple in _input_info.items():
            if not cls._login_server(seq, ip_passwd_tuple):
                return False

        # 清理用不到的数据，节省内存
        ViewModel.cache('SUBLOGIN_INDEX_LIST', type='DEL')

        """ 关闭进度条并开始后台上传文件 """
        cls.prepare_env()
        Utils.top_progress_stop()
        del _input_info
        return True


class PageHandler:
    """ 页面事件处理类 """
    _collect_state_flag = False

    @classmethod
    def _mutex(cls, ip, evt, lock=True):
        """ 防重入 """
        _lock_file = '%s\\%s-%s.lock' % (Global.G_CMDS_DIR, evt, ip)
        # 释放锁
        if not lock:
            Common.remove(_lock_file)
            return
        # 尝试加锁
        if Common.is_file(_lock_file):
            Utils.tell_info("%s 重复点击，请耐心等待上一次结束" % ip)
            return False
        Common.write_to_file(_lock_file, 'lock')
        return True

    @classmethod
    def _get_ssh(cls, ip=None):
        if ip:
            return ViewModel.cache('LOGON_SSH_DICT', type='QUE')[ip]
        return ViewModel.cache('LOGON_SSH_DICT', type='QUE')

    @classmethod
    def _get_exec_info(cls, ssh, cmd):
        return SSHUtil.exec_info(ssh,
                                 cmd,
                                 root=True
                                 )[0].split('__BINGO__')[1:2][0]

    @classmethod
    def __exec_shell(cls, ssh, ip, shell, param):
        """ 后台执行脚本 """
        event= shell.split('.')[0]
        Utils.tell_info('%s: [0%%] 正在执行任务: %s' % (ip, event))
        cmd = "cd %s && ./%s" % (Global.G_SERVER_DIR, shell)
        cmd = "%s '%s' '%s' &" % (cmd, ip, param)
        SSHUtil.exec_ret(ssh, cmd, root=True)

    @classmethod
    def __get_progress(cls, ssh, callback, ip, event):
        """ 循环读取进度 """
        cmd = "cat %s/%s/progress.txt" % (Global.G_SERVER_DIR, event)
        _last_prog = 1
        __retry = 0
        while True:
            sleep(1)
            try:
                cur_prog, status, info = cls._get_exec_info(ssh, cmd).split('|')
                cur_prog = int(cur_prog) - 10
                if _last_prog == cur_prog:
                    continue
                _last_prog = cur_prog

                if not info:
                    raise ReportError("进度信息为空，重试:%s" % __retry)
                if status == 'FAILED':
                    raise ReportError("任务失败，详细:%s，重试:%s" % (info, __retry))
                if cur_prog == 90:
                    filename = Common.basename(info)
                    Utils.tell_info("%s: [90%%] Download: %s" % (ip, filename))
                    if not SSHUtil.download_file(ssh, remote=info,local=filename):
                        raise ReportError("下载失败，重试:%s" % __retry)
                    callback(ip, 100, False)
                    Utils.tell_info("%s: [100%%] 下载成功" % ip)
                    break
                # 显示进度信息
                callback(ip, _last_prog, False)
                Utils.tell_info("%s: [%s%%] %s" % (ip, _last_prog, info))
            except Exception as e:
                print(e)
                __retry += 1
                if __retry < Global.G_RETRY_TIMES:
                    continue
                callback(ip, _last_prog + 1, 'Red')
                Utils.tell_info("%s %s" % (ip, e), level='ERROR')
                break

    @classmethod
    def _exec_for_download(cls, callback, ip, shell, param):
        """ 本函数中callback为进度条回调 """
        event = shell.split('.')[0]
        if not cls._mutex(ip, event):
            return

        ssh = cls._get_ssh(ip)

        cls.__exec_shell(ssh, ip, shell, param)

        cls.__get_progress(ssh, callback, ip, event)

        cls._mutex(ip, event, False)

    @classmethod
    def _exec_for_collect(cls, callback, ip_list, shell, param):
        event = shell.split('.')[0]
        shell = "%s/%s" % (Global.G_SERVER_DIR, shell)
        while True:
            for ip in ip_list:
                _info_dict = {}
                ssh = cls._get_ssh(ip)
                cmd = "%s '%s' '%s' '%s'" % (shell, event, ip, param)
                try:
                    lines = cls._get_exec_info(ssh, cmd).split('\n')
                    for line in lines:
                        k, v = line.split(':')
                        _info_dict[k] = v
                    callback((ip, _info_dict))
                except Exception as e:
                    Utils.tell_info('%s %s结果异常:%s' % (ip, shell, e),
                                    level='ERROR')
            sleep(10)

    @classmethod
    def _keep_ssh_alive(cls, args=None):
        while 1:
            sleep(60)
            for ip, ssh in cls._get_ssh().items():
                ret, err = SSHUtil.exec_ret(ssh, 'ls')
                Logger.debug("(keepalive) ip:%s ret:%s err:%s" % (ip, ret, err))

    @classmethod
    def default_page_deal(cls):
        Common.create_thread(func=cls._keep_ssh_alive, args=())

    @classmethod
    def start_shell(cls, type, *args):
        function = cls._exec_for_download
        if type == 'collect':
            function = cls._exec_for_collect
        Common.create_thread(func=function, args=args)

    @classmethod
    def collect_state_start(cls, callback, ip_list, shell):
        if cls._collect_state_flag:
            return
        cls._collect_state_flag = True
        cls.start_shell('collect', callback, ip_list, shell, None)

    @classmethod
    def get_halog_start(cls, callback, ip, shell):
        cls.start_shell('download', callback, ip, shell, None)

    @classmethod
    def get_binlog_start(cls, callback, ip, shell, param):
        cls.start_shell('download', callback, ip, shell, param)

    @classmethod
    def get_otherlog_start(cls, callback, ip_list, shell, param):
        for ip in ip_list:
            cls.start_shell('download', callback, ip, shell, param)

