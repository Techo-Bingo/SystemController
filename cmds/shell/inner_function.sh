#!/bin/bash
g_task_dir=''
g_home_dir=$(dirname $0)
g_split_flag='____BINGO_FILTER____'
cd ${g_home_dir}


function make_task_dir()
{
    local task=$1
    cd ${g_home_dir}
    mkdir -p ${task} 2>/dev/null
    chmod 777 ${task} 2>/dev/null
    chmod 777 ${task}/* 2>/dev/null
    g_task_dir=${g_home_dir}/${task}
    rm -rf ${g_task_dir}/*
}

function sync_call_shell()
{
    local task=$1
    local shell=$2
    shift 2
    local params=$*
    make_task_dir ${task}
    cd ${g_task_dir}
    dos2unix ${g_home_dir}/${shell}
    echo "sh ${g_home_dir}/${shell} ${params}" >${g_task_dir}/__call__.txt
    sh ${g_home_dir}/${shell} ${params} >${g_task_dir}/__print__.txt 2>&1
    return $?
}

function async_call_shell()
{
    local task=$1
    local shell=$2
    shift 2
    local params=$*
    make_task_dir ${task}
    cd ${g_task_dir}
    dos2unix ${g_home_dir}/${shell}
    echo "sh ${g_home_dir}/${shell} ${params}" >${g_task_dir}/__call__.txt
    sh ${g_home_dir}/${shell} ${params} >${g_task_dir}/__print__.txt 2>&1 &
}

# 有些环境登陆后可能会预先打印用户环境信息，获取打印信息会造成混乱，
# 加一个特殊字段过滤，使用____BINGO_FILTER____分割后的第二个字段的值
function get_task_progress()
{
    local task=$1
    echo "${g_split_flag}"
    cat ${g_home_dir}/${task}/__progress__.txt
	echo "${g_split_flag}"
}

function get_task_stdout()
{
    local task=$1
    echo "${g_split_flag}"
    cat ${g_home_dir}/${task}/__print__.txt
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

