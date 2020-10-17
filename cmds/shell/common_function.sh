#!/bin/bash
g_print="__print__"
g_error="__error__"
g_call="__call__"
g_progress="__progress__"
g_split_flag="____BINGO_FILTER____"


function _report()
{
	echo "$1|$2|$3" >${g_task_dir}/${g_progress}
	chmod 777 ${g_task_dir}/__*
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
	which tar &>/dev/null && { echo "${dst_file}.tar.gz"; tar zcvf ${dst_file}.tar.gz * &>/dev/null && { chmod 777 ${dst_file}.tar.gz; return 0; } || return 1; }
	which zip &>/dev/null && { echo "${dst_file}.zip"; zip ${dst_file}.zip * &>/dev/null && { chmod 777 ${dst_file}.zip; return 0; } || return 1; }
	return 1
}


