#!/bin/bash
. /opt/UBP/svc_profile.sh
g_dir=$1
g_ip=$2
g_day=$3
g_home=$(dirname $0)
cd ${g_home}
g_home=$(pwd)
g_dir=${g_home}/${g_dir}
g_my_cnf=/etc/eapp3307/my.cnf
g_binlog_list=/tmp/binary_logs_list.tmp
# 10GB
g_limit_binlog_size=10737418240

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
function get_date()
{
	date -d "-${g_day} DAY" '+%Y-%m-%d'
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
	report_info '20' 'server perpare OK'

	if [ ! -f "$g_my_cnf" ] || [ ! -f /opt/UBP/conf/deploy_policy_4.0.xml ] || [ ! -f /opt/UBP/bin/get_deploy_hostcfg_field.pyc ]
	then
		report_err '25' 'Miss necessary file...'
	fi
	
	local install_pack=$(python /opt/UBP/bin/get_deploy_hostcfg_field.pyc 'install_package')
	if [ "$install_pack" = "MRS" ]
	then
		local mrs_ha=$(python /opt/UBP/bin/get_deploy_hostcfg_field.pyc 'MRS_HA_MODE')
		if [ "$mrs_ha" != 'MASTER' -a "$mrs_ha" != 'SLAVE' ]
		then
			report_err '30' 'Is MRS of STANDALONE'
		fi
	else
		local ha_mode=$(python /opt/UBP/bin/get_deploy_hostcfg_field.pyc 'HA_MODE')
		if [ "$ha_mode" = 'STANDALONE' ]
		then
			report_err '30' 'eAPP is STANDALONE'
		fi
	fi
	report_info '30' 'HA mode is correct'
	
	/opt/UBP/bin/exec_sql<<EOF >$g_binlog_list 2>/dev/null
show binary logs\G
EOF
	if [ $? -ne 0 ]
	then
		report_err '45' 'exec sql failed'
	fi
	if [ ! -s "${g_binlog_list}" ]
	then
		report_err '50' 'No binlog found'
	fi
	
	cd $(grep '^datadir=' $g_my_cnf|cut -d '=' -f 2)
	local binlog_list=$(grep 'Log_name:' $g_binlog_list |awk '{print $2}')
	local start_day="$(get_date)"
	local now_day="$(date +'%Y-%m-%d')"
	local start_time="${start_day} 00:00:00"
	local end_time="$now_day 23:59:59"
	local binlog_store_file="$g_dir/binlog_events.log"

	for log in $binlog_list
	do
		echo "=========== mysql-bin: $log =============" >>$binlog_store_file
		mysqlbinlog --no-defaults -vv --base64-output=DECODE-ROWS --start-datetime="$start_time" --stop-datetime="$end_time" $log >>$binlog_store_file
	done
	if [ $? -ne 0 ]
	then
		report_err '60' 'mysqlbinlog exec failed'
	fi
	report_info '60' 'mysqlbinlog to file finish'
	
	if [ $(ls -l ${binlog_store_file}|awk '{print $5}') -gt ${g_limit_binlog_size} ]
	then
		rm -rf ${binlog_store_file}
		report_err '70' "Binlog file bigger than ${g_limit_binlog_size}"
	fi
	
	cd $g_dir/
	local pack_name="binlog_${g_ip}_$(echo ${start_day}|sed 's/-//g')_$(echo ${now_day}|sed 's/-//g')"
	
	local pack_name=$(compress ${pack_name})
	if [ $? -ne 0 ]
	then
		report_err '95' "Compress ${pack_name} failed"
	fi
	rm -rf ${binlog_store_file}
	local out=${g_dir}/${pack_name}
	chmod 777 ${out}

	report_info '100' "${out}"
}
main >/dev/null 2>&1

