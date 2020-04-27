#!/bin/bash
. /opt/UBP/svc_profile.sh

g_dir=$1
g_ip=$2
g_logtype=$3
g_home=$(dirname $0)
cd ${g_home}
g_home=$(pwd)
g_dir=${g_home}/${g_dir}
g_my_cnf=/etc/eapp3307/my.cnf

function prev_proc()
{
	ps -ef|grep $(basename $0)|grep -v grep|grep -wv $$|awk '{print $2}'|xargs kill -9
	mkdir ${g_dir}
	chmod 777 ${g_dir}
	rm -rf ${g_dir}/*
}
function _report()
{
	echo __BINGO__"$1|$2|$3"__BINGO__ >${g_dir}/progress.txt
	chmod 777 ${g_dir}/progress.txt
}
function report_info()
{
	_report "$1" "RUNNING" "$2"
}
function report_err()
{
	_report "$1" "FAILED" "$2"
	exit 1
}
function parser_param()
{
	g_message=$(echo ${g_logtype}|awk -F"|" '{print $1}')
	g_mysqlerr=$(echo ${g_logtype}|awk -F"|" '{print $2}')
	g_deploy=$(echo ${g_logtype}|awk -F"|" '{print $3}')
	g_version=$(echo ${g_logtype}|awk -F"|" '{print $4}')
	g_userlog=$(echo ${g_logtype}|awk -F"|" '{print $5}')
	g_alarm=$(echo ${g_logtype}|awk -F"|" '{print $6}')
	g_monitor=$(echo ${g_logtype}|awk -F"|" '{print $7}')
}
function get_message()
{
	[ "${g_message}" = '0' ] && return 0
	cp /var/log/messages* ${g_dir}
	return $?
}
function get_mysqlerr()
{
	[ "${g_mysqlerr}" = '0' ] && return 0
	local datadir=$(grep '^datadir=' $g_my_cnf|cut -d '=' -f 2)
	cp ${datadir}/*.err ${g_dir}
	return $?
}
function get_deploy()
{
	[ "${g_deploy}" = '0' ] && return 0
	cp /opt/UBP/conf/deploy_policy_4.0.xml ${g_dir}
	return $?
}
function get_version()
{
	[ "${g_version}" = '0' ] && return 0
	cp /opt/UBP/conf/version.mdc.ini ${g_dir}
	return $?
}
function get_userlog()
{
	[ "${g_userlog}" = '0' ] && return 0
	exec_sql <<EOF >TBL_UserLog.db
select * from ubpdb.TBL_UserLog\G
EOF
	return $?
}
function get_alarm()
{
	[ "${g_alarm}" = '0' ] && return 0
	exec_sql <<EOF >TBL_UbpSyncSsnAlarm.db
select * from ubpdb.TBL_UbpSyncSsnAlarm\G
EOF
	return $?
}
function get_monitor()
{
	[ "${g_monitor}" = '0' ] && return 0
	cp /home/ubp/logs/ubp_monitor.log* ${g_dir}
	return $? 
}
function compress()
{
	local dst_file=$1
	which 7za &>/dev/null && { echo "${dst_file}.7z"; 7za a ${dst_file}.7z * &>/dev/null && return 0 || return 1; }
	which tar &>/dev/null && { echo "${dst_file}.tar.gz"; tar zcvf ${dst_file}.tar.gz * &>/dev/null && return 0 || return 1; }
	which zip &>/dev/null && { echo "${dst_file}.zip"; zip ${dst_file}.zip * &>/dev/null && return 0 || return 1; }
	return 1
}
function main()
{
	prev_proc
	cd ${g_dir}
	
	parser_param
	report_info '30' 'server perpare OK'

	get_message
	if [ $? -ne 0 ]
	then
		report_err '40' "copy messages failed"
	fi
	report_info '40' "copy messages success"

	get_mysqlerr
	if [ $? -ne 0 ]
	then
		report_err '50' "copy eappmysql.err failed"
	fi
	report_info '50' "copy eappmysql.err success"

	get_deploy
	if [ $? -ne 0 ]
	then
		report_err '55' "copy deploy file failed"
	fi
	report_info '55' "copy deploy success"

	get_version
	if [ $? -ne 0 ]
	then
		report_err '60' "copy version file failed"
	fi
	report_info '60' "copy version file success"

	get_userlog
	if [ $? - ne 0 ]
	then
		report_err '70' "get TBL_UserLog failed"
	fi
	report_info '70' "get TBL_UserLog success"

	get_alarm
	if [ $? - ne 0 ]
	then
		report_err '80' "get active alarm failed"
	fi
	report_info '80' "get active alarm success"
	
	get_monitor
	if [ $? -ne 0 ]
	then
		report_err '90' "copy ubp_monitor.log failed"
	fi
	report_info '90' "copy ubp_monitor.log success"

	local pack_name="other_logs_${g_ip}"
	local pack_name=$(compress ${pack_name})
	if [ $? -ne 0 ]
	then
		report_err '95' "Compress ${pack_name} ${g_dir}/* failed"
	fi
	
	local out=${g_dir}/${pack_name}
	chmod 777 ${out}

	report_info '100' "${out}"
}

main &>/dev/null


