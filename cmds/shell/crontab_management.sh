#!/bin/bash
source ${g_home_dir}/common_function.sh

OP_TYPE=$1

function get_cron_list()
{
	crontab -l
}

function main()
{
	if [ "${OP_TYPE}" = 'ENTER' ]
	then
		get_cron_list
	fi
}

main 
