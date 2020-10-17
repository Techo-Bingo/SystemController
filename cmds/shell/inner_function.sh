#!/bin/bash
cd $(dirname $0)
export g_home_dir=$(pwd)
export g_upload_dir=${g_home_dir}/UPLOAD
source ./common_function.sh


function init_task()
{
    local task=$1
    [ -z "${task}" ] && return 1
    mkdir -p ${task} 2>/dev/null
    rm -rf ${task}/* 2>/dev/null

    export g_task_dir=${g_home_dir}/${task}
    cd ${g_task_dir}
    report_info "10" "server init ok"
}

function sync_call_shell()
{
    local task=$1
    local shell=$2
    shift 2
    local params=$*
    init_task ${task}
    dos2unix ${g_home_dir}/${shell}
    echo "$(whoami): sh ${g_home_dir}/${shell} ${params}" >${g_task_dir}/${g_call}
    sh ${g_home_dir}/${shell} ${params} >${g_task_dir}/${g_print} 2>&1
    return $?
}

function async_call_shell()
{
    local task=$1
    local shell=$2
    shift 2
    local params=$*
    init_task ${task}
    dos2unix ${g_home_dir}/${shell}
    echo "$(whoami): sh ${g_home_dir}/${shell} ${params}" >${g_task_dir}/${g_call}
    sh ${g_home_dir}/${shell} ${params} >${g_task_dir}/${g_print} 2>&1 &
    return $?
}

# 有些环境登陆后可能会预先打印用户环境信息，获取打印信息会造成混乱，
# 加一个特殊字段过滤，使用____BINGO_FILTER____分割后的第二个字段的值
function get_task_progress()
{
    local task=$1
    echo "${g_split_flag}"
    cat ${g_home_dir}/${task}/${g_progress}
    echo "${g_split_flag}"
}

function get_task_stdout()
{
    local task=$1
    echo "${g_split_flag}"
    cat ${g_home_dir}/${task}/${g_print}
    echo "${g_split_flag}"
}

function kill_shell()
{
    local shell=$1
    local top_pid=$(ps -ef|grep -w "${shell}"|awk '{print $2}'|head -1)
    pstree ${top_pid} -p|tr '(' '\n'|grep '^[0-9]'|cut -d')' -f1|xargs kill -9
}

$*
exit $?

