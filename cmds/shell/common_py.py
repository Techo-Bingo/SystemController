# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import time
if sys.version[0] == '3':
	import configparser as ConfigParser
else:
	import ConfigParser
g_common_file = '/home/.BINGO//common_py.log'
class Log:
	'''
	全部通过类方法来记录日志。
	usage:  Log.Init('xxx.log')
			Log.info('info.....')
	'''
	@classmethod
	def Init(self,filename):
		self._filename=filename
	@classmethod
	def write_append(self,info):
		if not self._filename:
			self._filename = g_common_file
		write_append_file(self._filename,'%s %s'%(get_nowtime_str(),info))
	@classmethod
	def info(self,info):
		self.write_append('[INFO ] : %s'%(info))
	@classmethod
	def warn(self,info):
		self.write_append('[WARN ] : %s'%(info))
	@classmethod
	def error(self,info):
		self.write_append('[ERROR] : %s'%(info))
	@classmethod
	def debug(self,info):
		self.write_append('[DEBUG] : %s'%(info))
def get_nowtime_str():
	ct=time.time()
	msec=(ct-int(ct))*1000
	return '%s.%03d'%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),msec)
def write_append_file(filename,infos):
	try:
		# python 2.6以下不支持次语法
		#with open(filename,'a+') as f:
		#	f.write(infos+'\n')
		#	return True
		f = open(filename, 'a+')
		f.write(infos+'\n')
		f.close()
		return True
	except:
		return False
def write_to_file(filename,info):
	try:
		#with open(filename,'w') as f:
		#	f.write(info)
		#	return True
		f = open(filename, 'w')
		f.write(info)
		f.close()
		return True
	except:
		return False
def cat_file(filename):
	try:
		#with open(filename,'r') as f:
		#	return f.read()
		f = open(filename, 'r')
		a = f.read()
		f.close()
		return a
	except:
		return ''
def os_cmd(s_cmd_line):
	return os.system(s_cmd_line)
def shell_cmd(s_cmd_line,inmsg=None):
	p= subprocess.Popen(s_cmd_line,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
	if inmsg:
		p.stdin.write(inmsg)
	out,err=p.communicate()
	return p.returncode,out,err
def shell_cmd_ex(s_cmd_line, s_run_path="."):
	s_cur_path = os.getcwd()
	os.chdir(s_run_path)
	nRet, outinfo,errInfo = shell_cmd(s_cmd_line)
	os.chdir(s_cur_path)
	return nRet, outinfo,errInfo
def exec_cmd(cmd):
	return os.popen(cmd).read().replace("\n","")
def file_exist(filepath):
	return os.path.exists(filepath)
