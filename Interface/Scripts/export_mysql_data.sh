#!/bin/bash
source ${g_home_dir}/common_function.sh

DB_NAME=$1
TBL_NAME=$2

function main()
{
	[ ! -f "/opt/UBP/bin/exec_sql" ] && report_err "20" "exec_sql don't exist !"

  [ "${TBL_NAME}" = '__None__' ] && TBL_NAME=''

	cd ${g_task_dir}
	. /opt/UBP/svc_profile.sh
	/opt/UBP/bin/exec_sql --op mysqldumpex --all "${DB_NAME} ${TBL_NAME} --force --xml" >${DB_NAME}-${TBL_NAME}.sql 2>${g_stderr}
	[ $? -ne 0 ] && report_err "50" "export failed ! $(tail -1 ${g_stderr})"

	chmod 777 ${g_task_dir}/*
  report_info "100" "${g_task_dir}/${DB_NAME}-${TBL_NAME}.sql"
}

main
exit 0

