#!/bin/bash
source ${g_home_dir}/common_function.sh

LOG_FLAGS=$1

function parser_param()
{
	FLAG1=$(echo ${LOG_FLAGS}|awk -F"@" '{print $1}')
	FLAG2=$(echo ${LOG_FLAGS}|awk -F"@" '{print $2}')
	FLAG3=$(echo ${LOG_FLAGS}|awk -F"@" '{print $3}')
	FLAG4=$(echo ${LOG_FLAGS}|awk -F"@" '{print $4}')
	report_info '20' 'server perpare OK'
}

function compress_pack()
{
	cd ${g_task_dir}
	local pack_name="quick_logs"
	report_info '92' "Compress ${pack_name} start..."
	local pack_name=$(compress ${pack_name})
	[ $? -ne 0 ] && report_err '95' "Compress ${pack_name} failed"
	report_info '100' "${g_task_dir}/${pack_name}"
}

function collect()
{
	cd ${g_task_dir}

	[ "${FLAG1}" = 1 ] && echo "CALL_COLLECT_FLAG1"

	[ "${FLAG2}" = 1 ] && echo "CALL_COLLECT_FLAG2"

	[ "${FLAG3}" = 1 ] && echo "CALL_COLLECT_FLAG3"

	[ "${FLAG4}" = 1 ] && echo "CALL_COLLECT_FLAG4"
}

function main()
{
	parser_param
	collect
	compress_pack
}

main
exit 0



