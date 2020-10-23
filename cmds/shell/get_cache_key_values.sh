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

function get_ubp_process_name()
{
	local ubp_list=$(su - ubp -c ". /opt/UBP/svc_profile.sh;ubp_adm -cmd status"|grep -v '^query'|awk -F"(" '{print $1}'|awk -F. '{print $1}'|grep -v 'All Services')
	echo "${g_split_flag}"
	echo "__UBP_PROC__ ${g_cache_split} $(echo ${ubp_list}|tr '\n' ' ')"
	echo "${g_split_flag}"
}

function main()
{
	if [ "${TYPE}" = '__IP__NETCARD__' ]
	then
		get_ip_netcard
	elif [ "${TYPE}" = '__UBP_PROC__' ]
	then
		get_ubp_process_name
	fi
}

main 
