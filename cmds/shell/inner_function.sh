#!/bin/bash
g_task_dir=''
g_home_dir=$(dirname $0)
cd ${g_home_dir}


function make_task_dir()
{
    local task=$1
    cd ${g_home_dir}
    mkdir -p ${task} 2>/dev/null
    chmod 777 ${task} 2>/dev/null
    # dos2unix ${task}/* 2>/dev/null
    chmod 777 ${task}/* 2>/dev/null
    g_task_dir=${g_home_dir}/${task}
}

function sync_call_shell()
{
    local ip=$1
    local task=$2
    local shell=$3
    local params=$4
    make_task_dir ${task}
    cd ${g_task_dir}
    dos2unix ${g_home_dir}/${shell}
    echo "sh ${g_home_dir}/${shell} ${ip} ${params}" >${g_task_dir}/call.txt
    sh ${g_home_dir}/${shell} "${ip}" "${params}" >${g_task_dir}/print.txt 2>&1
    return $?
}

function async_call_shell()
{
    local task=$1
    local shell=$2
    local ip=$3
    local params=$4
    make_task_dir ${task}
    cd ${g_task_dir}
    dos2unix ${g_home_dir}/${shell}
    echo "sh ${g_home_dir}/${shell} ${ip} ${params}" >${g_task_dir}/call.txt
    sh ${g_home_dir}/${shell} "${ip}" "${params}" >${g_task_dir}/print.txt 2>&1 &
}

function get_task_stdout()
{
    local task=$1
    cat ${g_home_dir}/${task}/print.txt
}

function kill_shell()
{
    local shell=$1
    killall ${shell}
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

