#!/bin/bash
source $(dirname $0)/common_function.sh
source /opt/UBP/svc_profile.sh
source /etc/profile

IP=$1
DAYS_INDEX=$2
if [ "${DAYS_INDEX}" = '0' ]
then
	DAYS=1
elif [ "${DAYS_INDEX}" = '1' ]
then
	DAYS=3
elif [ "${DAYS_INDEX}" = '2' ]
then
	DAYS=7
fi
LIMIT_SIZE=2147483648
START_DATE="$(date -d "-${DAYS} DAY" '+%Y-%m-%d') 00:00:00"
END_DATE="$(date +'%Y-%m-%d') 23:59:59"


function get_binlog()
{
	[ -d "${EAPP_MYSQL_DATADIR}" ] || report_err "25" "EAPP_MYSQL_DATADIR error"

	cd ${g_task_dir}
	local binlog_list='binlog_list.ini'
	/opt/UBP/bin/exec_sql<<EOF >${binlog_list} 2>/dev/null
show binary logs\G
EOF
	if [ $? -ne 0 ]
	then
		report_err '35' 'Exec sql failed'
	fi
	if [ ! -s "${binlog_list}" ]
	then
		report_err '40' 'No binlog found'
	fi

	local binlog_store='binlog_events.log'
	for log in $(grep 'Log_name:' ${binlog_list} |awk '{print $2}')
	do
		echo "=========== mysql-bin: $log =============" >>${binlog_store}
		mysqlbinlog --no-defaults -vv --base64-output=DECODE-ROWS --start-datetime="${START_DATE}" --stop-datetime="${END_DATE}" ${EAPP_MYSQL_DATADIR}/${log} >>${binlog_store}
	done
	if [ $? -ne 0 ]
	then
		report_err '70' 'mysqlbinlog exec failed'
	fi
	report_info '70' 'mysqlbinlog to file finish'

	if [ $(ls -l ${binlog_store}|awk '{print $5}') -gt ${LIMIT_SIZE} ]
	then
		rm -rf ${binlog_store}
		report_err '75' "Binlog file bigger than ${LIMIT_SIZE}"
	fi
}

function compress_pack()
{
	cd ${g_task_dir}
	local pack_name="binlog_${IP}"
	report_info '92' "Compress ${pack_name} start..."
	local pack_name=$(compress ${pack_name})
	[ $? -ne 0 ] && report_err '95' "Compress ${pack_name} failed"
	report_info '100' "${g_task_dir}/${pack_name}"
}

function main()
{
	init
	get_binlog
	compress_pack
}

main &>/dev/null
exit 0


