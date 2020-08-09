#!/bin/bash
source $(dirname $0)/common_function.sh

IP=$1

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


function main()
{
    get_memory

}

main
