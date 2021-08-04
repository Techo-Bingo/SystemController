# -*- coding: utf-8 -*-
import os
# import sys
import subprocess
import time

"""
if sys.version[0] == '3':
    import configparser as ConfigParser
else:
    import ConfigParser
"""
g_common_log = '/home/Bingo/common_function.log'


class Log:
    @classmethod
    def Init(cls, filename):
        cls._filename = filename

    @classmethod
    def write_append(cls, info):
        if not cls._filename:
            cls._filename = g_common_log
        write_append_file(cls._filename, '%s %s' % (get_nowtime_str(), info))

    @classmethod
    def info(cls, info):
        cls.write_append('[INFO ] : %s' % (info))

    @classmethod
    def warn(cls, info):
        cls.write_append('[WARN ] : %s' % (info))

    @classmethod
    def error(cls, info):
        cls.write_append('[ERROR] : %s' % (info))

    @classmethod
    def debug(cls, info):
        cls.write_append('[DEBUG] : %s' % (info))


def get_nowtime_str():
    ct = time.time()
    msec = (ct - int(ct)) * 1000
    return '%s.%03d' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msec)


def write_append_file(filename, infos):
    try:
        with open(filename, 'a+') as f:
            f.write(infos + '\n')
            return True
    except:
        return False


def write_to_file(filename, info):
    try:
        with open(filename, 'w') as f:
            f.write(info)
            return True
    except:
        return False


def cat_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except:
        return ''


def os_cmd(s_cmd_line):
    return os.system(s_cmd_line)


def shell_cmd(s_cmd_line, inmsg=None):
    p = subprocess.Popen(s_cmd_line, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if inmsg:
        p.stdin.write(inmsg)
    out, err = p.communicate()
    return p.returncode, out, err


def shell_cmd_ex(s_cmd_line, s_run_path="."):
    s_cur_path = os.getcwd()
    os.chdir(s_run_path)
    ret, out, err = shell_cmd(s_cmd_line)
    os.chdir(s_cur_path)
    return ret, out, err


def exec_cmd(cmd):
    return os.popen(cmd).read().replace("\n", "")


def file_exist(filepath):
    return os.path.exists(filepath)

class IPv4Address(object):

    #  in: 11000000101010000000000000000001
    # out: 192.168.0.1
    def _bin_to_ip_str(self, ip_bin):
        start, out = 0, []
        while len(ip_bin) >= start + 8:
            end = start + 8
            a = ip_bin[start:end]
            start += 8
            b = int(a, 2)
            out.append(str(b))
        return '.'.join(out)

    #  in: 192.168.0.1
    # out: 11000000101010000000000000000001
    def _ip_str_to_bin(self, ip_str):
        out = []
        for i in ip_str.split('.'):
            out.append(bin(int(i)).replace('0b', '').rjust(8, '0'))
        return ''.join(out)

    #  in: 192.168.0.1, 255.255.255.0
    # out: ['192.168.0.0', '192.168.0.255']
    def get_range_by_ip_mask(self, ip_str, mask_str):
        ip_bin = self._ip_str_to_bin(ip_str)
        mask_bin = self._ip_str_to_bin(mask_str)
        one_index = mask_bin.find('0')
        mask_bin = mask_bin[0:one_index]
        ip_bin = ip_bin[0:one_index]
        net_int_addr = int(mask_bin, 2) & int(ip_bin, 2)
        with_bin_net = bin(net_int_addr).replace('0b', '').rjust(one_index, '0')
        # 起始网络地址二进制 #
        net_bin_addr = self._bin_to_ip_str(with_bin_net.ljust(32, '0'))
        # 广播地址二进制 #
        broad_bin_addr = self._bin_to_ip_str(with_bin_net.ljust(32, '1'))
        return [net_bin_addr, broad_bin_addr]

    #  in: 192.168.0.1, 24
    # out: ['192.168.0.1', '192.168.0.255']
    def get_range_by_ip_bit(self, ip_str, mask_bit):
        mask_str = self.bit_to_mask_str(mask_bit)
        return self.get_range_by_ip_mask(ip_str, mask_str)

    #  in: 24
    # out: 255.255.255.0
    def bit_to_mask_str(self, bit):
        if not isinstance(bit, int) or not (0 < bit < 32):
            return ''
        bin_data = '1' * bit + '0' * (32 - bit)
        start, end = 0, 8
        bin_list = []
        while len(bin_data) >= end:
            a = bin_data[start:end]
            start += 8
            end += 8
            b = int(a, 2)
            bin_list.append(str(b))
        return '.'.join(bin_list)

    #  in: 255.255.255.0
    # out: 24
    def mask_str_to_bit(self, mask_str):
        return sum([bin(int(i)).count('1') for i in mask_str.split('.')])

