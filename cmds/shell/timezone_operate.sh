#!/bin/bash
source $(dirname $0)/common_function.sh

IP=$1
OP_TYPE=$2


function get_info()
{
	local start_end=$(/usr/sbin/zdump -v -c $(date +%Y),$(($(date +%Y)+1)) /etc/localtime|grep isdst=1 |awk -F= '{print $2}'|awk '{print $1" "$2" "$3" "$4}'|tr '\n' '#')
	
}
