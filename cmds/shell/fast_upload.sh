#!/bin/bash
source ${g_home_dir}/common_function.sh

SRC_FILE=$1
DEST_PATH=$2
MOD_ATTR=$3
OWN_ATTR=$4

function upload()
{
	[ -z "${SRC_FILE}" -o -z "${DEST_PATH}" -o -z "${MOD_ATTR}" -o -z "${OWN_ATTR}" ] && report_err "40" "invaild args"

	SRC_FILE=${g_upload_dir}/${SRC_FILE}

	[ -f "${SRC_FILE}" ] || report_err "40" "${SRC_FILE} No such file"
	
	[ -d "${DEST_PATH}" ] || report_err "40" "${DEST_PATH} No such directory"

	cd ${g_task_dir}
	local dest_file="${DEST_PATH}/$(basename ${SRC_FILE})"
	
	mv -f ${SRC_FILE} ${dest_file} || report_err "50" "move file to ${DEST_PATH} failed !"
	chmod ${MOD_ATTR} ${dest_file} || report_err "60" "chmod ${MOD_ATTR} ${dest_file} failed !"
	chown ${OWN_ATTR} ${dest_file} || report_err "70" "chown ${OWN_ATTR} ${dest_file} failed !"
	
	chmod -R 777 ${g_task_dir}/*
	report_info "100" "NULL"
}

function main()
{
    upload
}

main &>/dev/null
