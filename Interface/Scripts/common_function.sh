#!/bin/bash
g_print="__print__"
g_error="__error__"
g_call="__call__"
g_progress="__progress__"
g_split_flag="____BINGO_FILTER____"
g_cache_split="____BINGO_CACHE____"


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

function echo_info()
{
  echo "$(date +'%F %T'): $1"
}

function report_func()
{
  local ret=$1
  local info=$2
  local prog=$3
  local print=$4
  if [ $ret -eq 0 ]
  then
    [ -n "${print}" ] && echo_info "${info}    ......成功"
    local _info="${info}    ......成功"
    [ "${prog}" = '100' ] && local _info='NULL'
    report_info "${prog}" "${_info}"
  else
    [ -n "${print}" ] && echo_info "${info}    ......失败"
    report_err "${prog}" "${info}    ......失败"
  fi
}

function compress()
{
    cd ${g_task_dir}
    local dst_file=$1
    which tar &>/dev/null && { echo "${dst_file}.tar.gz"; tar zcvf ${dst_file}.tar.gz * &>/dev/null && { chmod 777 ${dst_file}.tar.gz; return 0; } || return 1; }
    which zip &>/dev/null && { echo "${dst_file}.zip"; zip ${dst_file}.zip * &>/dev/null && { chmod 777 ${dst_file}.zip; return 0; } || return 1; }
    return 1
}

function to_unix()
{
    local files=$*
    for file in ${files}
    do
        cp $file ${file}_tmp
        cat ${file}_tmp | tr -d "\r" >$file
        rm ${file}_tmp &
    done
}

