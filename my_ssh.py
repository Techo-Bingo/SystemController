# -*- coding: UTF-8 -*-

import os
import time
import paramiko
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

    def execute(self, cmd, root=False):
        if root:
            cmd = '''echo "%s"|su - -c "%s"''' % (self._root_pwd, cmd)
        try:
            if not self._ssh_client:
                self._ssh_client = paramiko.SSHClient()
                self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self._ssh_client.connect(self._host_ip, username=self._user_name, password=self._user_pwd)
            return self._ssh_client.exec_command(cmd)
        except Exception as e:
            raise SSHError(e)

    def upload(self, local_path, server_path, callback=None):
        try:
            trans = paramiko.Transport(self._host_ip, self._port)
            trans.connect(username=self._user_name, password=self._user_pwd)
            # 可以解决大文件上传问题
            with paramiko.SFTPClient.from_transport(trans) as ftp:
                ftp.put(local_path, server_path, callback=callback)
        except Exception as e:
            raise SSHError(e)

    def download(self, server_path, local_path, callback=None):
        try:
            trans = paramiko.Transport(self._host_ip, self._port)
            trans.connect(username=self._user_name, password=self._user_pwd)
            with paramiko.SFTPClient.from_transport(trans) as ftp:
                ftp.get(server_path, local_path, callback=callback)
        except Exception as e:
            raise SSHError(e)

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
        try:
            return str(info, encoding='UTF-8'), None   # , errors='ignore'
        except:
            return str(info, encoding='GBK', errors='ignore'), None

    @classmethod
    def exec_ret(cls, ssh_inst, cmd, root=False):
        try:
            info = ssh_inst.execute(cmd, root)[1]
            return info.channel.recv_exit_status(), None
        except SSHError as e:
            return -1, e

    @classmethod
    def user_login(cls, ssh_inst, user_name):
        root = True if user_name == 'root' else False
        ret, err = cls.exec_ret(ssh_inst, 'whoami|grep %s' % user_name, root)
        if ret:
            return False, err
        else:
            return True, None

    @classmethod
    def upload_file(cls, ssh_inst, local, remote, callback=None):
        path = os.path.split(remote)[0]
        try:
            ssh_inst.execute('rm -f {1};mkdir -p {0};chmod 777 {0}'.format(path, remote), root=True)
            time.sleep(0.2)
            ssh_inst.upload(local, remote, callback)
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

