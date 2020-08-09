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
            Logger.error('SubLogin_{} ip:{}, err_info:{}'.format(seq, ip_passwd_tuple[0], e))
            return False
        else:
            cls._sublogin_status_tig(seq, 'LOGING')
            return True

    @classmethod
    def _login_server(cls, seq, ip_passwd_tuple):
        ip, user, userpwd, rootpwd = ip_passwd_tuple
        for times in range(1, Global.G_RETRY_TIMES + 1):
            ssh = SSH(ip, user, userpwd, rootpwd)
            try:
                ret, err = SSHUtil.user_login(ssh, user)
                if not ret:
                    cls._widget = 'userpwd'
                    raise ExecError("%s %s登录失败!\n详细:%s 重试:%s" % (ip, user, err, times))
                ret, err = SSHUtil.user_login(ssh, 'root')
                if not ret:
                    cls._widget = 'rootpwd'
                    raise ExecError("%s root登录失败!\n详细:%s 重试:%s" % (ip, err, times))
            except ExecError as e:
                Logger.warn(e)
                if times == Global.G_RETRY_TIMES:
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
        # 先压缩脚本再上传
        zip_name = "package.zip"
        zip_file = "%s\\%s" % (Global.G_CMDS_DIR, zip_name)
        remote_path = '%s/%s' % (Global.G_SERVER_DIR, zip_name)
        Common.zip_dir(Global.G_SHELL_DIR, zip_file)
        unzip_cmd = '''cd {0}; unzip -o {1}; chmod 777 {0}/*; dos2unix {0}/*'''.format(Global.G_SERVER_DIR, zip_name)
        _ip_del_list = []
        for ip, ssh in cls._logon_ssh_inst('QUE', None).items():
            # 如果上次登录用户跟这次不一致，会导致后面解压失败; 这里每次登录都清空目录
            SSHUtil.exec_ret(ssh, 'rm -rf %s/*' % Global.G_SERVER_DIR, root=True)
            for times in range(1, Global.G_RETRY_TIMES + 1):
                try:
                    # 上传文件
                    ret, err = SSHUtil.upload_file(ssh, zip_file, remote_path)
                    if not ret:
                        raise ExecError('%s 上传package失败，详细:%s，重试:%s' % (ip, err, times))
                    # 解压文件, 成功返回0
                    ret, err = SSHUtil.exec_ret(ssh, unzip_cmd)
                    if ret:
                        raise ExecError('%s 解压package失败，详细:%s，重试:%s' % (ip, err, times))
                except ExecError as e:
                    if times == Global.G_RETRY_TIMES:
                        _ip_del_list.append(ip)
                    Utils.tell_info(e, level='ERROR')
                    Logger.warn(e)
                    continue
                else:
                    info = '%s 环境准备就绪' % ip
                    Logger.info(info)
                    Utils.tell_info(info)
                    break
        [cls._logon_ssh_inst('SUB', ip) for ip in _ip_del_list]
        Common.remove(zip_file)
        # ssh保活
        cls._keep_ssh_alive()

    @classmethod
    def _keep_ssh_alive(cls, args=None):
        while True:
            Common.sleep(60)
            for ip, ssh in cls._logon_ssh_inst('QUE', None).items():
                ret, err = SSHUtil.exec_ret(ssh, 'echo')
                Logger.debug("(keepalive) ip:%s ret:%s err:%s" % (ip, ret, err))

    @classmethod
    def prepare_env(cls):
        Common.create_thread(func=cls._upload_package)

    @classmethod
    def try_login(cls):
        # return True  # DEBUG
        cls._ip_list = []
        _input_info = {}

        # 输入校验
        for seq in ViewModel.cache('SUBLOGIN_INDEX_LIST', type='QUE'):
            ip_passwd_tuple = cls._sublogin_callback(
                Global.EVT_GET_LOGIN_INPUT % seq)

            if not cls._check_inputs(seq, ip_passwd_tuple):
                return False
            _input_info[seq] = ip_passwd_tuple

        # 登录校验，开启进度条
        Utils.top_progress_start('登录中')

        for seq, ip_passwd_tuple in _input_info.items():
            if not cls._login_server(seq, ip_passwd_tuple):
                return False

        # 清理用不到的数据，节省内存
        ViewModel.cache('SUBLOGIN_INDEX_LIST', type='DEL')

        # 关闭进度条并开始后台上传文件
        cls.prepare_env()
        Utils.top_progress_stop()
        del _input_info
        return True


class PageHandler:
    """ 页面事件处理类 """
    _stop_task_ips = {}
    _inner_caller = "sh %s/inner_function.sh" % Global.G_SERVER_DIR

    @classmethod
    def _mutex(cls, ip, task, lock=True):
        """ 防重入 """
        _lock_file = '%s\\%s-%s.lock' % (Global.G_LOCKS_DIR, task, ip)
        # 释放锁
        if not lock:
            try:
                Common.remove(_lock_file)
            except:
                pass
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
    def _stop_task(cls, task, ip, op='get'):
        # 暂停后台循环任务
        if op == 'remove':
            if task not in cls._stop_task_ips:
                cls._stop_task_ips[task] = []
                return
            if ip in cls._stop_task_ips[task]:
                cls._stop_task_ips[task].remove(ip)
        elif op == 'append':
            if task not in cls._stop_task_ips:
                cls._stop_task_ips[task] = []
            if ip not in cls._stop_task_ips[task]:
                cls._stop_task_ips[task].append(ip)
        else:
            return True if ip in cls._stop_task_ips[task] else False
    
    @classmethod
    def _get_exec_info(cls, ssh, cmd, root):
        return SSHUtil.exec_info(ssh, cmd, root)[0].split('__BINGO__')[1:2][0]

    @classmethod
    def _exec_shell(cls, ssh, ip, shell, task, param, run_root, run_back=False):
        """ 后台执行脚本 """
        Utils.tell_info('%s: [0%%] 正在执行任务: %s' % (ip, task))
        if run_back:
            cmd = "{0} async_call_shell {1} {2} {3} {4}".format(cls._inner_caller, ip, task, shell, param)
        else:
            cmd = "{0} sync_call_shell {1} {2} {3} {4}".format(cls._inner_caller, ip, task, shell, param)
        SSHUtil.exec_ret(ssh, cmd, run_root)

    @classmethod
    def _get_progress(cls, ssh, callback, ip, task, run_root):
        """ 循环读取进度 """
        cmd = "cat %s/%s/progress.txt" % (Global.G_SERVER_DIR, task)
        _last_prog = 1
        __retry = 0
        while True:
            Common.sleep(1)
            try:
                cur_prog, status, info = cls._get_exec_info(ssh, cmd, run_root).split('|')
                cur_prog = int(cur_prog) - 10
                if not info:
                    raise ReportError("进度信息为空，重试:%s" % __retry)
                if status == 'FAILED':
                    raise ReportError("任务失败，详细:%s，重试:%s" % (info, __retry))
                if _last_prog == cur_prog:
                    continue
                _last_prog = cur_prog
                # 显示进度信息
                callback(ip, _last_prog, False)
                if cur_prog == 90:
                    if info == 'NULL':
                        callback(ip, 100, False)
                        Utils.tell_info("%s: [100%%] %s执行成功" % (ip, task))
                        break
                    filename = "%s\\%s" % (Global.G_DOWNLOAD_DIR, Common.basename(info))
                    Utils.tell_info("%s: [90%%] 开始下载: %s" % (ip, filename))
                    if not SSHUtil.download_file(ssh, remote=info,local=filename):
                        raise ReportError("下载失败，重试:%s" % __retry)
                    callback(ip, 100, False)
                    Utils.tell_info("%s: [100%%] 下载成功" % ip)
                    break
                Utils.tell_info("%s: [%s%%] %s" % (ip, _last_prog, info))
            except Exception as e:
                __retry += 1
                if __retry < Global.G_RETRY_TIMES:
                    continue
                callback(ip, _last_prog + 1, 'Red')
                Utils.tell_info("%s %s" % (ip, e), level='ERROR')
                break

    @classmethod
    def _get_print(cls, ssh, callback, ip, task, run_root, run_back):
        cmd = "{0} get_task_stdout {1}".format(cls._inner_caller, task)
        def get_print():
            ret_info = SSHUtil.exec_info(ssh, cmd, run_root)[0]
            Utils.tell_info("%s:[100%%] 执行结果：\n%s" % (ip, ret_info))
            if callback:
                try:
                    callback(ret_info)
                except:
                    pass
        if run_back:
            while True:
                if cls._stop_task(task, ip):
                    Utils.tell_info("%s 已停止循环读取" % ip)
                    break
                Common.sleep(2)
                get_print()
        else:
            get_print()

    @classmethod
    def _exec_shell_impl(cls, shell_type, callback, ip, shell, param, run_root=True, run_back=False):
        """
        shell_type:
            download，下载类型的脚本，回调函数为进度条
            showing，打印回显类型的脚本，回调函数为回显框
        """
        task = shell.split('.')[0]
        if not cls._mutex(ip, task):
            return

        ssh = cls._get_ssh(ip)

        cls._exec_shell(ssh, ip, shell, task, param, run_root, run_back)
        
        cls._stop_task(task, ip, 'remove')

        if shell_type == 'download':
            cls._get_progress(ssh, callback, ip, task, run_root)
        elif shell_type == 'showing':
            cls._get_print(ssh, callback, ip, task, run_root, run_back)

        cls._mutex(ip, task, False)

    @classmethod
    def start_shell(cls, *args):
        Common.create_thread(func=cls._exec_shell_impl, args=args)

    @classmethod
    def kill_shell(cls, ip, task, shell):
        ssh = cls._get_ssh(ip)
        SSHUtil.exec_ret(ssh, "{0} kill_shell {1} {2}".format(cls._inner_caller, ip, shell), True)
        cls._mutex(ip, task, False)
        Utils.tell_info("%s 杀死任务%s和子进程成功" % (ip, task))

    @classmethod
    def execute_download_start(cls, callback, ip_list, shell, param):
        for ip in ip_list:
            cls.start_shell('download', callback, ip, shell, param, True, True)

    @classmethod
    def execute_download_stop(cls, ip_list, shell):
        task = shell.split('.')[0]
        for ip in ip_list:
            cls.kill_shell(ip, task, shell)

    @classmethod
    def execute_fast_cmd_start(cls, callback, ip_list, shell, text, run_root, run_back):
        local_path = ".\\%s\\%s" % (Global.G_SHELL_DIR, shell)
        remote_path = "%s/%s" % (Global.G_SERVER_DIR, shell)
        Common.write_to_file(local_path, text)
        for ip in ip_list:
            ssh = cls._get_ssh(ip)
            ret, err = SSHUtil.upload_file(ssh, local_path, remote_path)
            if not ret:
                Utils.tell_info("%s:[50%%] 上传脚本文件失败，执行命令失败！" % ip, level='ERROR')
                callback(ip, 50, 'Red')
                continue
            cls.start_shell('showing', None, ip, shell, None, run_root, run_back)
            callback(ip, 100, False)

    @classmethod
    def execute_fast_cmd_stop(cls, ip_list, shell):
        task = shell.split('.')[0]
        for ip in ip_list:
            cls.kill_shell(ip, task, shell)
            # 暂停循环读取打印线程
            cls._stop_task(task, ip, 'append')

    @classmethod
    def _fast_upload_impl(cls, ip, callback, local, tmp_upload, check_cmd, move_cmd):
        Utils.tell_info("%s:[10%%] 开始上传%s" % (ip, local))
        cls._stop_task('fast_upload', ip, 'remove')
        ssh = cls._get_ssh(ip)
        ret, err = SSHUtil.exec_ret(ssh, check_cmd, True)
        if ret:
            Utils.tell_info("%s:[20%%] 服务器目录不存在" % ip, level='ERROR')
            callback(ip, 20, 'Red')
            return
        callback(ip, 20, False)
        ret, err = SSHUtil.upload_file(ssh, local, tmp_upload)
        if cls._stop_task('fast_upload', ip):
            return
        if not ret:
            Utils.tell_info("%s:[70%%] 上传失败！" % ip, level='ERROR')
            callback(ip, 70, 'Red')
            return
        callback(ip, 70, False)
        ret, err = SSHUtil.exec_ret(ssh, move_cmd, True)
        if ret:
            Utils.tell_info("%s:[90%%] 移动至目标目录失败或修改属性失败" % ip, level='ERROR')
            callback(ip, 90, 'Red')
        callback(ip, 100, False)
        Utils.tell_info("%s:[100%%] %s上传成功" % (ip, local))

    @classmethod
    def execute_fast_upload_start(cls, callback, ip_list, local, remote, chmod, chown):
        base_name = Common.basename(local)
        upload_dir = "%s/UPLOAD" % Global.G_SERVER_DIR
        tmp_upload = "%s/%s" % (upload_dir, base_name)
        dest_path = "%s/%s" % (remote, base_name)
        check_cmd = "{0} upload_prev_check {1} {2}".format(cls._inner_caller, remote, upload_dir)
        move_cmd = "{0} move_file {1} {2} {3} {4}".format(cls._inner_caller, tmp_upload, dest_path, chmod, chown)
        for ip in ip_list:
            args = (ip, callback, local, tmp_upload, check_cmd, move_cmd)
            Common.create_thread(func=cls._fast_upload_impl, args=args)

    @classmethod
    def execute_fast_upload_stop(cls, ip_list):
        task = 'fast_upload'
        for ip in ip_list:
            cls._stop_task(task, ip, 'append')
            Utils.tell_info("%s: 停止%s成功" % (ip, task))

    @classmethod
    def execute_showing_start(cls, callback, ip ,shell, param):
        cls.start_shell('showing', callback, ip, shell, param, True, False)


    '''
    @classmethod
    def _exec_for_collect(cls, callback, ip_list, shell, param):
        shell = "cd %s && ./%s" % (Global.G_SERVER_DIR, shell)
        while True:
            for ip in ip_list:
                _info_dict = {}
                ssh = cls._get_ssh(ip)
                cmd = "%s '%s' '%s'" % (shell, ip, param)
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
    '''

