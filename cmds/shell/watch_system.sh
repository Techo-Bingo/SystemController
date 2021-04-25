#!/bin/bash
cd $(dirname $0)
# source ./common_function.sh

# 129600 = 1min * 60 * 24 * 90 = 3个月
LIMIT_LINES=129600
DOWNLOAD_DIR="__DOWNLOAD__"
STORE_DIR="/opt/Bingo"
MEM_CSV="${STORE_DIR}/__memory__.csv"
CPU_CSV="${STORE_DIR}/__cpu_usage__.csv"
IO_CSV="${STORE_DIR}/__io_util__.csv"
mkdir ${STORE_DIR} ${DOWNLOAD_DIR} 2>/dev/null

function is_running()
{
    [ $(ps -ef|grep -v grep|grep -w "$(basename $0)"|wc -l) -gt 2 ] || return 1
    cp ${STORE_DIR}/*.csv ${DOWNLOAD_DIR}
    chmod 777 ${DOWNLOAD_DIR} ${DOWNLOAD_DIR}/*.csv
    return 0
}

function watch_mem()
{
    local meminfo="/proc/meminfo"
    local MemTotal=$(grep -w MemTotal ${meminfo}|awk -F: '{print $2}'|awk '{print $1}')
    local MemFree=$(grep -w MemFree ${meminfo}|awk -F: '{print $2}'|awk '{print $1}')
    local MemAvailable=$(grep -w MemAvailable ${meminfo}|awk -F: '{print $2}'|awk '{print $1}')
    local Cached=$(grep -w Cached ${meminfo}|awk -F: '{print $2}'|awk '{print $1}')
    local SwapTotal=$(grep -w SwapTotal ${meminfo}|awk -F: '{print $2}'|awk '{print $1}')
    local SwapFree=$(grep -w SwapFree ${meminfo}|awk -F: '{print $2}'|awk '{print $1}')
    local SwapCached=$(grep -w SwapCached ${meminfo}|awk -F: '{print $2}'|awk '{print $1}')

    [ -f "${MEM_CSV}" ] || echo "Date,MemTotal,MemFree,MemAvailable,Cached,SwapTotal,SwapFree,SwapCached" >${MEM_CSV}
    echo "$(date +"%Y-%m-%d %H:%M"),${MemTotal},${MemFree},${MemAvailable},${Cached},${SwapTotal},${SwapFree},${SwapCached}" >>${MEM_CSV}
}

function watch_cpu()
{
    # 依据/proc/stat文件获取并计算CPU使用率
    # CPU时间计算公式：CPU_TIME=user+system+nice+idle+iowait+irq+softirq
    # CPU使用率计算公式：cpu_usage=(idle2-idle1)/(cpu2-cpu1)*100
    LAST_CPU_INFO=$(cat /proc/stat | grep -w cpu | awk '{print $2,$3,$4,$5,$6,$7,$8}')
    LAST_SYS_IDLE=$(echo $LAST_CPU_INFO | awk '{print $4}')
    LAST_TOTAL_CPU_T=$(echo $LAST_CPU_INFO | awk '{print $1+$2+$3+$4+$5+$6+$7}')
    sleep 3
    NEXT_CPU_INFO=$(cat /proc/stat | grep -w cpu | awk '{print $2,$3,$4,$5,$6,$7,$8}')
    NEXT_SYS_IDLE=$(echo $NEXT_CPU_INFO | awk '{print $4}')
    NEXT_TOTAL_CPU_T=$(echo $NEXT_CPU_INFO | awk '{print $1+$2+$3+$4+$5+$6+$7}')
    #系统空闲时间
    SYSTEM_IDLE=$(echo ${NEXT_SYS_IDLE} ${LAST_SYS_IDLE} | awk '{print $1-$2}')
    #CPU总时间
    TOTAL_TIME=$(echo ${NEXT_TOTAL_CPU_T} ${LAST_TOTAL_CPU_T} | awk '{print $1-$2}')
    CPU_USAGE=$(echo ${SYSTEM_IDLE} ${TOTAL_TIME} | awk '{printf "%.2f", 100-$1/$2*100}')

    [ -f "${CPU_CSV}" ] || echo "Date,CPU Usage" >${CPU_CSV}
    echo "$(date +"%Y-%m-%d %H:%M"),${CPU_USAGE}" >> ${CPU_CSV}
}

# IO %util 计算公式： /proc/diskstats 第13列（io_ticks）的差值 / 时间差值 / 10
# 暂时只统计sda硬盘IO情况
function watch_io()
{
    local t_a=$(grep -w 'sda' /proc/diskstats |head -1 |awk '{print $13}')
    sleep 3
    local t_b=$(grep -w 'sda' /proc/diskstats |head -1 |awk '{print $13}')
    local util=$(echo $((t_b - t_a)) 30 | awk '{printf "%.2f", $1/$2}')

    [ -f "${IO_CSV}" ] || echo "Date,%util" >${IO_CSV}
    echo "$(date +"%Y-%m-%d %H:%M"),${util}" >> ${IO_CSV}
}

function watch_disk()
{
    return 0
}

function truncate()
{
    for file in ${MEM_CSV} ${CPU_CSV}
    do
        local lines=$(wc -l ${file}|awk '{print $1}')
        [ ${lines} -gt ${LIMIT_LINES} ] && sed -i '2d' ${file}
    done
}

function start()
{
    watch_mem

    watch_cpu

    watch_io

    watch_disk

    truncate
}

function main()
{
    is_running && return 0

    while true
    do
	    start &

	    sleep 60
	done
}

main &>/dev/null &


