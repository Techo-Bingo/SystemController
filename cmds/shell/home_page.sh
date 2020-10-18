#!/bin/bash
source ${g_home_dir}/common_function.sh

OP_TYPE=$1

function get_sysinfo()
{
    if [ -f /usr/bin/lsb_release ]
    then
    echo "OS Model:                $(/usr/bin/lsb_release -a |grep Description |awk -F: '{print $2}' |sed 's/^[ \t]*//g')"
    elif [ -f /etc/redhat-release ]
    then
    echo "OS Model:                $(cat /etc/redhat-release |sed -n '1p')"
    elif [ -f /etc/issue ]
    then
    echo "OS Model:                $(cat /etc/issue |sed -n '1p')"
    fi
    echo "Kernel Version:          $(uname -r)"
    echo "CPU Model:               $(grep 'model name' /proc/cpuinfo|uniq|awk -F: '{print $2}'|sed 's/^[ \t]*//g'|sed 's/ \+/ /g')"
    echo "Physical CPUs/CPU Cores: $(grep 'physical id' /proc/cpuinfo|sort|uniq|wc -l) / $(grep 'cpu cores' /proc/cpuinfo|uniq|awk -F: '{print $2}'|sed 's/^[ \t]*//g')"
    echo "Total Memory:            $(($(cat /proc/meminfo|grep 'MemTotal'|awk '{print $2}') / 1024)) MB"
    echo "IP List:                 $(ip a|grep -w inet|grep -v '127.0.0.1'|awk '{print $2}'|tr '\n' ' ')"
}


function main()
{
    if [ "${OP_TYPE}" = 'ENTER' ]
    then
        get_sysinfo
    fi
}

main
