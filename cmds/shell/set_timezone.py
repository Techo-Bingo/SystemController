# -*- coding: utf-8 -*-
# 
# -------------------------- #
# 
# 全区域覆盖的智能夏令时机制
# 
# -------------------------- #
#
__author__ = 'LiBin'
import sys
import time
import common_py as omucom
g_logfile = "time_zone.log"
g_rulefile = "CustomsizeTZ.rule"
g_all_optskey = ['ZONET','DST','SMODE','SMONTH','SWSEQ','SWEEK','SDAY','STIME','EMODE','EMONTH','EWSEQ','EWEEK','EDAY','ETIME','METHOD']
g_opts_dict = {}
logger = ''
g_isdst = ''
g_date_type = ''
g_this_year=time.strftime("%Y", time.localtime())
g_last_year=2038
#======= 退出值定义 =======
# 存在空值
EXIST_NULL_VALUE=1
# 开始时间类型或结束时间类型的值不合法
INVAILD_SMODE_EMODE_VALUE=2
# 月份值非法
INVAILD_MONTH_RANGE=3
# 开始月份或结束月份，SMONTH或EMONTH的值非法
INVAILD_SMONTH_EMONTH_VALUE=4
# 日期，SDAY或EDAY的值非法
INVAILD_SDAY_EDAY_VALUE=5
# 2月份的日期，SDAY或EDAY的值非法
INVAILD_DAY_RANGE_2=6
# 4,6,9,11月份的日期，SDAY或EDAY的值非法
INVAILD_DAY_RANGE_4_11=7
# 开始日期中，第SWSEQ个星期SWEEK，SWSEQ或SWEEK的值非法
INVAILD_SWSEQ_SWEEK_VALUE=8
# 结束日期中，第EWSEQ个星期EWEEK，EWSEQ或EWEEK的值非法
INVAILD_EWSEQ_EWEEK_VALUE=9
# 时区规则写入文件失败
WRITE_RULE_FILE_ERR=10
# 夏令时跳变值非法
INVAILD_METHOD_VALUE=11
# 夏令时跳入的时间或者跳出的时间值非法
INVAILD_STIME_ETIME_VALUE=12
# 夏令时时区的值非法
INVAILD_ZONET_VALUE=13
# 编译时区规则文件失败
BUILD_RULEFILE_ERR=14
# 链接时区文件失败
RELINK_TIMEZONE_ERR=15
# 参数错误
INVAILD_OPTIONS=99
# 内部错误
INNER_OCCUR_ERROR=88
def usage():
	argv0 = sys.argv[0]
	usg = '''
Usage:
  |__ Examples:
  |     |__ python %s "ZONET=+0800,DST=NO"
  |     |__ python %s "ZONET=-0930,DST=YES,SMODE=DATE,SMONTH=3,SDAY=12,STIME=02:00:00,EMODE=DATE,EMONTH=10,EDAY=25,ETIME=23:00:00,METHOD=65"
  |     |__ python %s "ZONET=+1020,DST=YES,SMODE=DATE,SMONTH=3,SDAY=12,STIME=02:00:00,EMODE=WEEK,EMONTH=10,EWSEQ=5,SWEEK=6,ETIME=23:00:00,METHOD=65"
  |     |__ python %s "ZONET=-1320,DST=YES,SMODE=WEEK,SMONTH=3,SWSEQ=2,SWEEK=3,STIME=02:00:00,EMODE=DATE,EMONTH=10,EDAY=25,ETIME=23:00:00,METHOD=65"
  |     |__ python %s "ZONET=+1130,DST=YES,SMODE=WEEK,SMONTH=3,SWSEQ=2,SWEEK=3,STIME=02:00:00,EMODE=WEEK,EMONTH=10,EWSEQ=5,SWEEK=6,ETIME=23:00:00,METHOD=65"
  |     |__ ...
  |
  |__ Explain:
  |     |__ start time means :at this time,system time will jump METHOD (minutes). [ > 0: jump backward ]
  |     |__ end time means   :at this time,system time will jump METHOD (minutes). [ < 0: jump forward  ]
  |
  |__ Options:
        |________ ZONET         :timezone  range:[-1400,+1400] 
        |           |__ <ZONET=-0830|ZONET=+0830|ZONET=0830>...
        |________ DST           :if Daylight-Saving
        |           |__ <YES|NO>
        |________ SMODE/EMODE   :start/end time mode 
        |           |__ <DAY|WEEK>
        |________ SMONTH/EMONTH :start/end time of the month
        |           |__ <1|2|3|4|5|6|7|8|9|10|11|12> 
        |   
        |   _____ SDAY/EDAY     :start/end time of the day
        |  |        |__ <1~31>|<1~28>|<1~30>
        |__|
        |  |  +-+ SWSEQ/EWSEQ   :start/end time of the seq week. (x month's first/second/third/fourth/last week)
        |  |__|     |__ <1|2|3|4|5> 
        |     +-+ SWEEK/EWEEK   :start/end time at the week
        |           |__ <1|2|3|4|5|6|7>
        |________ STIME/ETIME   :start/end time clock.  format:02:00:00  
        |           |__ <02:00:00|01:30:30>
        |________ METHOD        :the offset of time will jump. (minute)
                    |__ <-120~-1>|<1~120>
'''%(argv0,argv0,argv0,argv0,argv0)
	print(usg)
	sys.exit(INVAILD_OPTIONS)
def init():
	global logger
	global g_opts_dict
	logger = omucom.Log
	logger.Init(g_logfile)
	para_options = sys.argv[1]
	logger.info("< start > options:%s"%(para_options))
	try:
		# python 2.6 不支持这个语法...
		#g_opts_dict={i.split('=')[0]:i.split('=')[1] for i in sys.argv[1].split(',')}
		for i in para_options.split(','):
			g_opts_dict[i.split('=')[0]] = i.split('=')[1]
	except:
		logger.error("invaild para options:%s"%(para_options))
		sys.exit(INVAILD_OPTIONS)
	# 值不能为空	
	for k,v in g_opts_dict.items():
		if not v:
			logger.error("the value of %s is NULL..."%(k))
			sys.exit(EXIST_NULL_VALUE)
def exist_key(k,inlist=g_opts_dict):
	return k in inlist
def is_sublist(a,b):
	return set(a).issubset(set(b))
def get_min_optskey(pa,pb):
	global g_date_type
	tmp_min = g_all_optskey
	if pa == 'DATE' and pb == 'DATE':
		tmp_min.remove('SWSEQ')
		tmp_min.remove('SWEEK')
		tmp_min.remove('EWSEQ')
		tmp_min.remove('EWEEK')
		g_date_type = 'SDAY+EDAY'
	elif pa == 'DATE' and pb == 'WEEK':
		tmp_min.remove('SWSEQ')
		tmp_min.remove('SWEEK')
		tmp_min.remove('EDAY')
		g_date_type = 'SDAY+EWEEK'
	elif pa == 'WEEK' and pb == 'DATE':
		tmp_min.remove('SDAY')
		tmp_min.remove('EWSEQ')
		tmp_min.remove('EWEEK')
		g_date_type = 'SWEEK+EDAY'
	elif pa == 'WEEK' and pb == 'WEEK':
		tmp_min.remove('SDAY')
		tmp_min.remove('EDAY')
		g_date_type = 'SWEEK+EWEEK'
	else:
		logger.warn("the value of SMODE or EMODE is invaild...")
		tmp_min = []
	return tmp_min
def match_month(i):
	'''
	月份序号转换成英文简写
	'''
	mon_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
	return mon_list[int(i)-1]
def match_week(i):
	'''
	星期序号转换成英文简写
	'''
	week_list = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
	return week_list[int(i)-1]
def minute_to_clock(m):
	'''
	跳变的分钟数改成 小时:分钟 的格式
	'''
	return "%s:%s"%(int(m/60),m%60)
def format_bin_name():
	'''
	设置Rule规则中的编译后的时区文件名称
	'''
	return "GMT%s"%(g_opts_dict['ZONET'].replace(':',''))
def is_leapyear(year=g_this_year):
	'''
	判断是否是闰年
	'''
	if ((year%4 == 0) and (year%100 != 0)) or (year%400 == 0):
		return True
	return False
def calculate_rule_date():
	'''
	获取具体的日期
	eg: 
		第一个星期日   Sun>=1
				12号   12
	'''
	s_month = int(g_opts_dict['SMONTH'])
	e_month = int(g_opts_dict['EMONTH'])
	s_day_max = 31
	e_day_max = 31
	# 先获取到最大的天数
	if s_month == 2:
		s_day_max = 28
	elif s_month in [4,6,9,11]:
		s_day_max = 30
	
	if e_month == 2:
		e_day_max = 28
	elif e_month in [4,6,9,11]:
		e_day_max = 30

	# 根据开始时间和结束时间的日期类型
	# 计算Rule中的日期时间
	out_s_date = ''
	out_e_date = ''
	if g_date_type == 'SDAY+EDAY':
		return g_opts_dict['SDAY'],g_opts_dict['EDAY']
	elif g_date_type == 'SDAY+EWEEK':
		out_s_date = g_opts_dict['SDAY']
		e_seq = int(g_opts_dict['EWSEQ'])
		e_week = int(g_opts_dict['EWEEK'])
		week_en = match_week(e_week)
		if e_seq == 5:
			# 最后一个周x算法:
			# <=(当月最大天数)
			out_e_date = "%s<=%s"%(week_en,e_day_max)
		else:
			# 第n个周x算法:
			# >=( n - 1 ) * 7 + 1
			out_e_date = "%s>=%s"%(week_en,(e_seq-1)*7+1)
	elif g_date_type == 'SWEEK+EDAY':
		out_e_date = g_opts_dict['EDAY']
		s_seq = int(g_opts_dict['SWSEQ'])
		s_week = int(g_opts_dict['SWEEK'])
		week_en = match_week(s_week)
		if s_seq == 5:
			out_s_date = "%s<=%s"%(week_en,s_day_max)
		else:
			out_s_date = "%s>=%s"%(week_en,(s_seq-1)*7+1)
	elif g_date_type == 'SWEEK+EWEEK':
		s_seq = int(g_opts_dict['SWSEQ'])
		s_week = int(g_opts_dict['SWEEK'])
		e_seq = int(g_opts_dict['EWSEQ'])
		e_week = int(g_opts_dict['EWEEK'])
		s_week_en = match_week(s_week)
		e_week_en = match_week(e_week)
		if s_seq == 5:
			out_s_date = "%s<=%s"%(s_week_en,s_day_max)
		else:
			out_s_date = "%s>=%s"%(s_week_en,(s_seq-1)*7+1)
		if e_seq == 5:
			out_e_date = "%s<=%s"%(e_week_en,e_day_max)
		else:
			out_e_date = "%s>=%s"%(e_week_en,(e_seq-1)*7+1)
	else:
		logger.error('!! Inner Error !!')
		sys.exit(INNER_OCCUR_ERROR)
	return out_s_date,out_e_date
def check_zone_format():
	'''
	由于时区规则中并没有规定时区范围和必须要是整点或者半点
	因此此处不做严格的匹配
	满足 -1400 <= zone_area <= 1400即可
	'''
	zone_area = g_opts_dict['ZONET']
	try:
		if list(zone_area)[0] in ['+','-']: # eg: -0800 or +0800
			if len(zone_area) != 5:raise
			if -1400 <= int(zone_area[1:]) <= 1400:
				g_opts_dict['ZONET'] = "%s:%s"%(zone_area[:3],zone_area[3:])
			else:
				raise
		elif -1400 <= int(zone_area) <= 1400:  # eg: 0800
			if len(zone_area) != 4:raise
			g_opts_dict['ZONET'] = "+%s:%s"%(zone_area[:2],zone_area[2:])
		else:
			raise
	except:
		logger.error("the value of ZONET(%s) is bad format..."%(zone_area))
		sys.exit(INVAILD_ZONET_VALUE)

	#logger.debug("value of ZONET is %s"%(g_opts_dict['ZONET']))
def check_time_format():
	'''
	必须为时间戳格式  02:00:00
	'''
	s_time = g_opts_dict['STIME']
	e_time = g_opts_dict['ETIME']
	try:
		# 小时
		if (0 <= int(s_time.split(':')[0]) <= 23) and (0 <= int(e_time.split(':')[0]) <= 23):
			pass
		else:
			raise
		# 分钟
		if (0 <= int(s_time.split(':')[1]) <= 59) and (0 <= int(e_time.split(':')[1]) <= 59):
			pass
		else:
			raise
		# 秒
		if (0 <= int(s_time.split(':')[2]) <= 59) and (0 <= int(e_time.split(':')[2]) <= 59):
			pass
		else:
			raise
	except:
		logger.error("the value of STIME(%s) or ETIME(%s) is bad format..."%(s_time,e_time))
		sys.exit(INVAILD_STIME_ETIME_VALUE)
def check_para_range(min_opts):
	'''
	主要检查参数options中的值（value）是否合法
	'''
	try:
		s_month = int(g_opts_dict['SMONTH'])
		e_month = int(g_opts_dict['EMONTH'])
	except:
		logger.error("the value of SMONTH or EMONTH is invaild...")
		sys.exit(INVAILD_SMONTH_EMONTH_VALUE)
	if 1 <= s_month <= 12 and 1 <= e_month <= 12:
		pass
	else:
		logger.error("SMONTH range error! should be 1-12")
		sys.exit(INVAILD_MONTH_RANGE)
	# 开始时间为日期类型
	if not exist_key('SWEEK',min_opts):
		try:
			s_day = int(g_opts_dict['SDAY'])
			if 1 <= s_day <= 31:
				pass
			else:
				raise 
		except:
			logger.error("the value of SDAY is invaild...")
			sys.exit(INVAILD_SDAY_EDAY_VALUE)
		if s_month == 2 and s_day > 28:
			logger.error("step in SDAY,month of 2 no more then 28 days...")
			sys.exit(INVAILD_DAY_RANGE_2)
		elif s_month in [4,6,9,11] and s_day >= 31:
			logger.error("step in SDAY,month of %s no more then 30 days..."%(s_month))
			sys.exit(INVAILD_DAY_RANGE_4_11)
	# 结束时间为日期类型
	if not exist_key('EWEEK',min_opts):
		try:
			e_day = int(g_opts_dict['EDAY'])
			if 1 <= e_day <= 31:
				pass
			else:
				raise 
		except:
			logger.error("the value of EDAY is invaild...")
			sys.exit(INVAILD_SDAY_EDAY_VALUE)
		if e_month == 2 and e_day > 28:
			logger.error("step in EDAY,month of 2 no more then 28 days...")
			sys.exit(INVAILD_DAY_RANGE_2)
		elif e_month in [4,6,9,11] and e_day >= 31:
			logger.error("step in EDAY,month of %s no more then 30 days..."%(s_month))
			sys.exit(INVAILD_DAY_RANGE_4_11)		
	# 开始时间为星期类型
	if not exist_key('SDAY',min_opts):
		try:
			s_wseq = int(g_opts_dict['SWSEQ'])
			s_week = int(g_opts_dict['SWEEK'])
			if 1 <= s_wseq <= 5 and 1 <= s_week <= 7:
				pass
			else:
				raise
		except:
			logger.error("the value of SWSEQ or SWEEK is invaild...")
			sys.exit(INVAILD_SWSEQ_SWEEK_VALUE)
	
	if not exist_key('EDAY',min_opts):
		try:
			e_wseq = int(g_opts_dict['EWSEQ'])
			e_week = int(g_opts_dict['EWEEK'])
			if 1 <= e_wseq <= 5 and 1 <= e_week <= 7:
				pass
			else:
				raise
		except:
			logger.error("the value of EWSEQ or EWEEK is invaild...")
			sys.exit(INVAILD_EWSEQ_EWEEK_VALUE)

	# 判断夏令时偏移
	# 夏令时时间跳变范围 1-120 minutes
	if g_isdst:
		try:
			offset = int(g_opts_dict['METHOD'])
			if 1 <= offset <= 120 or -120 <= offset <= -1:
				pass
			else:
				raise
		except:
			logger.error("the value of METHOD is invaild...")
			sys.exit(INVAILD_METHOD_VALUE)
def check_para_vaild():
	'''
	主要检查参数options中的键（key）是否合法
	'''
	global g_isdst
	para_keylist = g_opts_dict.keys()
	# 判断传入的参数的key是否是在给定的列表范围内
	# (子列表判断)
	if not is_sublist(para_keylist,g_all_optskey):
		logger.error("Unknown options key found,please check...")
		sys.exit(INVAILD_OPTIONS)
	# 判断是否包含必要的option
	if not is_sublist(['ZONET','DST'],para_keylist):
		logger.error("options less necessary key('ZONET','DST')...")
		sys.exit(INVAILD_OPTIONS)
	# 检查时区 ZONET的值的格式
	check_zone_format()
	# 不需要夏令时,直接进入设置
	if g_opts_dict['DST'] == 'NO':
		g_isdst = False
		return 
	# 需要夏令时
	g_isdst = True
	# 需要根据开始时间类型和结束时间类型，确定key的最小集
	#if not is_sublist(['SMODE','EMODE'],para_keylist):
	if not exist_key('SMODE') or not exist_key('EMODE'):
		logger.error("options less necessary key('SMODE','EMODE')...")
		sys.exit(INVAILD_OPTIONS)
	min_optskey = get_min_optskey(g_opts_dict['SMODE'],g_opts_dict['EMODE'])
	if not min_optskey:
		logger.error("get NULL min_optskey...")
		sys.exit(INVAILD_SMODE_EMODE_VALUE)
	# 判断参数options的key是否包含最小集
	if not is_sublist(min_optskey,para_keylist):
		less_list = []
		for i in min_optskey:
			if i not in para_keylist:
				less_list.append(i)
		logger.error("options less necessary keys:%s"%(less_list))
		#logger.debug('para_keylist  = %s'%(para_keylist))
		logger.debug('must include %s'%(min_optskey))
		sys.exit(INVAILD_OPTIONS)
	# 检查 STIME和ETIME的格式是否非法
	# 由于STIME和ETIME不管在那种类型下都是必然存在的
	# 所以两个都要检查
	check_time_format()
	# 检查传入的值的范围 
	check_para_range(min_optskey)
def create_zonerule():
	zone = g_opts_dict['ZONET']
	zone_name = format_bin_name()
	zone_line = "Zone HUBDST/%s %s HUBDST HUB%sT"%(zone_name,zone,"%s")
	if not g_isdst:
		# 无夏令时
		rule = "Rule HUBDST 1917 only - Jan 1 0:01 0 -"
		rule_infos = "%s\n%s\n"%(rule,zone_line)
	else:
		# 有夏令时 
		s_time = g_opts_dict['STIME']
		e_time = g_opts_dict['ETIME']
		offset = minute_to_clock(int(g_opts_dict['METHOD']))
		s_month_en = match_month(int(g_opts_dict['SMONTH']))
		e_month_en = match_month(int(g_opts_dict['EMONTH']))
		s_day_week,e_day_week = calculate_rule_date()
		rule_s = "Rule HUBDST %s %s - %s %s %s %s D"%(g_this_year,g_last_year,s_month_en,s_day_week,s_time,offset)
		rule_e = "Rule HUBDST %s %s - %s %s %s 0  S"%(g_this_year,g_last_year,e_month_en,e_day_week,e_time)
		rule_infos = "%s\n%s\n%s\n"%(rule_s,rule_e,zone_line)
	if omucom.write_to_file(g_rulefile,rule_infos):
		logger.info("write rule file success,DaylightSaving=%s"%(g_isdst))
	else:
		logger.error("write rule file failed !! DaylightSaving=%s"%(g_isdst))
		sys.exit(WRITE_RULE_FILE_ERR)
def build_timezone():
	'''
	用zic命令编译时区规则文件
	'''
	cmd = "/usr/sbin/zic %s"%(g_rulefile)
	ret,info,err = omucom.shell_cmd(cmd)
	if ret:
		logger.error("build timezone rule file failed !(info:%s) (error:%s)"%(info,err))
		logger.debug("------- cat %s -------"%(g_rulefile))
		logger.debug(omucom.cat_file(g_rulefile))
		sys.exit(BUILD_RULEFILE_ERR)
def relink_localtime():
	cmd = "chmod 755 /usr/share/zoneinfo/HUBDST;chmod 644 /usr/share/zoneinfo/HUBDST/*;ln -sf /usr/share/zoneinfo/HUBDST/%s /etc/localtime && hwclock --systohc >/dev/null 2>&1 &"%(format_bin_name())
	ret,info,err = omucom.shell_cmd(cmd)
	if ret:
		logger.error("relink localtime failed !(info:%s) (error:%s)"%(info,err))
		sys.exit(RELINK_TIMEZONE_ERR)
def print_time_infos():
	cmd = "zdump -v -c %s,%s /etc/localtime"%(g_this_year,int(g_this_year)+1)
	ret,info,err=omucom.shell_cmd(cmd)
	logger.debug("%s"%(cmd))
	logger.debug("%s"%(info))
	logger.info("All done Success !")
	print('SUCCESS')
if __name__ == '__main__':
	if len(sys.argv) < 2:usage()
	init()
	check_para_vaild()
	create_zonerule()
	build_timezone()
	relink_localtime()
	print_time_infos()
	
