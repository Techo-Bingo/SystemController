#!/bin/bash
g_dir=$1
g_ip=$2
g_home=$(dirname $0)
cd ${g_home}
g_home=$(pwd)
g_dir=${g_home}/${g_dir}
g_kpld_dir=/home/ubp/logs/keepalived

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
	report_info '40' 'server perpare OK'
	
	cd $g_kpld_dir
	local pack_name="ha_logs_${g_ip}"
	
	local pack_name=$(compress ${pack_name})
	if [ $? -ne 0 ]
	then
		report_err '70' "Compress ${pack_name} failed"
	else
		report_info '70' "Compress ${pack_name} success"
	fi

	mv ${pack_name} ${g_dir}
	if [ $? -ne 0 ]
	then
		report_err '90' "mv ${pack_name} ${g_dir}"
	fi
	
	local out=${g_dir}/${pack_name}
	chmod 777 ${out}
	
	report_info '100' "${out}"
}

main &>/dev/null 
