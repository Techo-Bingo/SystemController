#!/bin/bash
source $(dirname $0)/common_function.sh

function get_memory()
{
    local infos=$(free -m)
    local heads=$(echo "${infos}"|head -1)
    local memory=$(echo "${infos}"|grep '^Mem'|awk -F: '{print $2}')
    local swap=$(echo "${infos}"|grep '^Swap'|awk -F: '{print $2}')
    local mem_used=$(echo "${memory}"|awk '{print $2}')
    local mem_free=$(echo "${memory}"|awk '{print $3}')
    local swap_used=$(echo "${swap}"|awk '{print $2}')
    local swap_free=$(echo "${swap}"|awk '{print $3}')
    if [ $(echo "${heads}"|awk '{print $6}') == 'cached' ]
    then
        local buff=$(echo "${memory}"|awk '{print $5}')
        local cache=$(echo "${memory}"|awk '{print $6}')
        local buff_cache=$((buff+cache))
    else
        local buff_cache=$(echo "${memory}"|awk '{print $5}')
    fi
    echo "Used Free Buff/Cache"
    echo "Memory Swap"
    echo "${mem_used} ${swap_used}"
    echo "${mem_free} ${swap_free}"
    echo "${buff_cache} 0"
}

function get_sysinfo()
{
    if [ -f /usr/bin/lsb_release ]
    then
        echo "OS Model:            $(/usr/bin/lsb_release -a |grep Description |awk -F: '{print $2}' |sed 's/^[ \t]*//g')"
    else
        echo "OS Model:            $(cat /etc/issue |sed -n '1p')"
    fi
    echo "Kernel Version:          $(uname -r)"
    echo "CPU Model:               $(grep 'model name' /proc/cpuinfo|uniq|awk -F: '{print $2}'|sed 's/^[ \t]*//g'|sed 's/ \+/ /g')"
    echo "Physical CPUs/CPU Cores: $(grep 'physical id' /proc/cpuinfo|sort|uniq|wc -l) / $(grep 'cpu cores' /proc/cpuinfo|uniq|awk -F: '{print $2}'|sed 's/^[ \t]*//g')"
    echo "Total Memory:            $(($(cat /proc/meminfo|grep 'MemTotal'|awk '{print $2}') / 1024)) MB"
}


function main()
{
    # get_memory
    get_sysinfo
}

main
