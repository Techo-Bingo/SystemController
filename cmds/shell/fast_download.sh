#!/bin/bash
source ${g_home_dir}/common_function.sh

FILE_PATH=$1

function download()
{
	if [ ! -e "${FILE_PATH}" ]
	then
		report_err "20" "${FILE_PATH} No such file or directory"
	fi
	
	local pack_name=$(basename ${FILE_PATH})
	if [ -f "${FILE_PATH}" ]
	then
		report_info "30" "Copying file..."
		cp -f ${FILE_PATH} ${g_task_dir}/${pack_name} 2>${g_error}
		[ $? -ne 0 ] && report_err '60' "$(head -1 ${g_error})"
	else
		report_info "30" "Copying directory..."
		cp -rf ${FILE_PATH} ${g_task_dir}/ 2>${g_error}
		[ $? -ne 0 ] && report_err '60' "$(head -1 ${g_error})"
		
		report_info "90" "Compress start"
		local pack_name=$(compress ${pack_name})
		[ $? -ne 0 ] && report_err '95' "Compress ${pack_name} failed"
	fi
	
	report_info "100" "${g_task_dir}/${pack_name}"
}

function main()
{
    download
}

main &>/dev/null
