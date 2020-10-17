#!/bin/bash
source ${g_home_dir}/common_function.sh

OP_TYPE=$1
ZONE_INFO=$OP_TYPE


function get_status()
{
	local time_zone="(UTC$(date -R|awk '{print $NF}')) $(ls -l /etc/localtime|cut -d'/' -f7-)"
	local start_end=$(/usr/sbin/zdump -v -c $(date +%Y),$(($(date +%Y)+1)) /etc/localtime|grep isdst=1 |awk -F= '{print $2}'|awk '{print $1" "$2" "$3" "$4}'|tr '\n' '#')
	[ -z "${start_end}" ] && local start_end='NA#NA'
	local start_time=$(echo "${start_end}"| cut -d'#' -f1)
    local end_time=$(echo "${start_end}"| cut -d'#' -f2)
	echo "  TimeZone: ${time_zone}  StartTime: ${start_time}  EndTime: ${end_time}"
	return 0
}

function set_timezone()
{
	python $(dirname $0)/set_timezone.py ${ZONE_INFO}
	local ret=$?
	if [ $ret -ne 0 ]
	then
	    report_err "90" "Set Timezone failed, errno:$ret"
	fi
	report_info "100" "NULL"
	return 0
}

function main()
{
	if [ "${OP_TYPE}" = 'ENTER' ]
	then
		get_status
    else
		set_timezone
	fi
	return $?
}

main
exit $?

