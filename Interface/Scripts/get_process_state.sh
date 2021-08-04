#!/bin/bash
source ${g_home_dir}/common_function.sh

OP_TYPE=$1

function get_status()
{
  [ ! -f /opt/UBP/svc_profile.sh ] && report_err 10 "环境不支持"
	. /opt/UBP/svc_profile.sh
	ubp_adm -cmd status
}

function main()
{
	if [ "${OP_TYPE}" = 'ENTER' ]
	then
		get_status
	fi
}

main
exit 0

