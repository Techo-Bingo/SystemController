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
    local params=$3
    make_task_dir ${task}
    cd ${g_task_dir}
    dos2unix ${g_home_dir}/${shell}
    echo "sh ${g_home_dir}/${shell} ${params}" >${g_task_dir}/__call__.txt
    sh ${g_home_dir}/${shell} "${params}" >${g_task_dir}/__print__.txt 2>&1
    return $?
}

function async_call_shell()
{
    local task=$1
    local shell=$2
    local params=$3
    make_task_dir ${task}
    cd ${g_task_dir}
    dos2unix ${g_home_dir}/${shell}
    echo "sh ${g_home_dir}/${shell} ${params}" >${g_task_dir}/__call__.txt
    sh ${g_home_dir}/${shell} "${params}" >${g_task_dir}/__print__.txt 2>&1 &
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

function upload_prev_check()
{
    local dest_dir=$1
    local upload_dir=$2
    [ -d "${dest_dir}" ] || return 1
    mkdir ${upload_dir}
    chmod 777 ${upload_dir}
    return 0
}

function move_file()
{
    local src_file=$1
    local dest_file=$2
    local mod_attr=$3
    local own_attr=$4
    [ -f ${src_file} ] || return 1
    mv -f ${src_file} ${dest_file} || return 2
    chmod ${mod_attr} ${dest_file} || return 3
    chown ${own_attr} ${dest_file} || return 4
    return 0
}

$*
exit $?

