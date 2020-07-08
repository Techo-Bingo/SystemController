#!/bin/bash
cd $(dirname $0)
g_home_path=$(pwd)
g_task_dir=''


function init()
{
	ps -ef|grep $(basename $0)|grep -v grep|grep -wv $$|awk '{print $2}'|xargs kill -9
	local task_name=$(echo $(basename $0)|awk -F"." '{print $1}')
	local task_dir=${g_home_path}/${task_name}
	mkdir ${task_dir}
	chmod 777 ${task_dir}
	rm -rf ${task_dir}/*
	g_task_dir=${task_dir}
}

function _report()
{
	echo __BINGO__"$1|$2|$3"__BINGO__ >${g_task_dir}/progress.txt
	chmod 777 ${g_task_dir}/progress.txt
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
	cd ${g_task_dir}
	local dst_file=$1
	which 7za &>/dev/null && { echo "${dst_file}.7z"; 7za a ${dst_file}.7z * &>/dev/null && { chmod 777 ${dst_file}.7z; return 0; } || return 1; }
	which tar &>/dev/null && { echo "${dst_file}.tar.gz"; tar zcvf ${dst_file}.tar.gz * &>/dev/null && { chmod 777 ${dst_file}.tar.gz; return 0; } || return 1; }
	which zip &>/dev/null && { echo "${dst_file}.zip"; zip ${dst_file}.zip * &>/dev/null && { chmod 777 ${dst_file}.zip; return 0; } || return 1; }
	return 1
}
