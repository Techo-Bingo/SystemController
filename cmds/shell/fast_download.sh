#!/bin/bash
source $(dirname $0)/common_function.sh

FILE_PATH=$1

function download()
{
	if [ ! -e "${FILE_PATH}" ]
	then
		report_err "20" "${FILE_PATH} No such file or directory"
	fi
	
	cd ${g_task_dir}
	local file_name=$(basename ${FILE_PATH})
	local pack_name=${file_name}
	if [ -f "${FILE_PATH}" ]
	then
		report_info "30" "Copying file..."
		cp -f ${FILE_PATH} ./${pack_name} 2>__error__
		[ $? -ne 0 ] && report_err '60' "$(head -1 __error__)"
	else
		report_info "30" "Copying directory..."
		cp -rf ${FILE_PATH} ./ 2>__error__
		[ $? -ne 0 ] && report_err '60' "$(head -1 __error__)"
		report_info "90" "Compress start"
		local pack_name=$(compress ${pack_name})
		[ $? -ne 0 ] && report_err '95' "Compress ${pack_name} failed"
	fi
	
	chmod -R 777 ${g_task_dir}/*
	report_info "100" "${g_task_dir}/${pack_name}"
}

function main()
{
    init
    download
}

main &>/dev/null
