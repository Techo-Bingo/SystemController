# -*- coding: UTF-8 -*-

import os
# import traceback
import paramiko
from time import sleep
from my_base import SSHError


class SSH(object):
    """ paramiko ssh登录服务类 """

    def __init__(self, ip, user, upwd, rpwd):
        self._host_ip = ip
        self._user_name = user
        self._user_pwd = upwd
        self._root_pwd = rpwd
        self._port = 22
        self._ssh_client = None
        self._ftp_client = None

    def execute(self, cmd, root=False):
        if root:
            cmd = '''echo "%s"|su - -c "%s"''' % (self._root_pwd, cmd)
        try:
            if not self._ssh_client:
                self._ssh_client = paramiko.SSHClient()
                self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self._ssh_client.connect(self._host_ip,
                                         username=self._user_name,
                                         password=self._user_pwd
                                         )
            return self._ssh_client.exec_command(cmd)
        except Exception as e:
            raise SSHError(e)

    def upload(self, local_path, server_path):
        try:
            self._sftp_open()
            self._ftp_client.put(local_path, server_path)
            self._sftp_close()
        except Exception as e:
            raise SSHError(e)

    def download(self, server_path, local_path):
        try:
            self._sftp_open()
            self._ftp_client.get(server_path, local_path)
            self._sftp_close()
        except Exception as e:
            raise SSHError(e)

    def _sftp_open(self):
        if not self._ftp_client:
            self._ftp_client = self._ssh_client.open_sftp()

    def _sftp_close(self):
        self._ftp_client.close()
        self._ftp_client = None

    def close(self):
        self._ssh_client.close()


class SSHUtil:
    """ SSH公共方式类 """

    @classmethod
    def exec_info(cls, ssh_inst, cmd, root=False):
        try:
            info = ssh_inst.execute(cmd, root)[1].read().strip()
        except Exception as e:
            return None, e
        else:
            return str(info, encoding='utf-8'), None

    @classmethod
    def exec_ret(cls, ssh_inst, cmd, root=False):
        try:
            info = ssh_inst.execute(cmd, root)[1]
        except SSHError as e:
            return -1, e
        else:
            return info.channel.recv_exit_status(), None

    @classmethod
    def user_login(cls, ssh_inst, user_name):
        root = True if user_name == 'root' else False
        ret, err = cls.exec_ret(ssh_inst,
                                'whoami|grep %s' % user_name,
                                root)
        if ret:
            return False, err
        else:
            return True, None

    @classmethod
    def upload_file(cls, ssh_inst, local, remote):
        path = os.path.split(remote)[0]
        try:
            ssh_inst.execute('mkdir -p {0};chmod 777 {0}'.format(path),
                             root=True
                             )
            # 此处等待一小段时间，否则后面upload会失败
            sleep(0.2)
            ssh_inst.upload(local, remote)
        except SSHError as e:
            return False, e
        else:
            return True, None

    @classmethod
    def download_file(cls, ssh_inst, remote, local):
        try:
            ssh_inst.download(remote, local)
        except SSHError as e:
            return False, e
        else:
            return True, None

