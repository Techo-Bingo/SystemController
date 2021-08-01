#!/bin/bash
cd $(dirname $0)
source ./common_function.sh

TYPE=$1

function get_ip_netcard()
{
    local interface=$(ip addr |grep -w "UP"|grep -vw "DOWN"|grep -vw "LOOPBACK"|awk '{print $2}'|sed 's/://g')
    local ip_list=$(ip addr |grep "${interface}"|grep -vw mtu|grep -vw "lo$"|awk '{print $2}'|grep -o -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}")
    echo "${g_split_flag}"
    echo "__NETCARD__ ${g_cache_split} $(echo ${interface}|tr '\n' ' ')"
    echo "__IP__ ${g_cache_split} $(echo ${ip_list}|tr '\n' ' ')"
    echo "${g_split_flag}"
}

function get_resource_name()
{
    echo "${g_split_flag}"
    echo "__RESOURCE__ ${g_cache_split} PROC_1 PROC_2"
    echo "${g_split_flag}"
}

function _default_()
{
    echo "${g_split_flag}"
    echo "${TYPE} ${g_cache_split} ${TYPE}_NOT_FOUNT"
    echo "${g_split_flag}"
}

function main()
{
	if [ "${TYPE}" = '__IP__NETCARD__' ]
	then
		get_ip_netcard
	elif [ "${TYPE}" = '__RESOURCE__' ]
	then
		get_resource_name
	else
	  _default_
	fi
}

main
exit 0


