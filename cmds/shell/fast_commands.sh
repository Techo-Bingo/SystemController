#!/bin/bash
source ${g_home_dir}/common_function.sh

FILE_NAME=$1

function main()
{
	local shell_path=${g_task_dir}/run_cmd.sh
	mv -f ${g_upload_dir}/${FILE_NAME} ${shell_path} || report_err "40" "Create shell script failed."

    dos2unix ${shell_path} 2>/dev/null
    chmod +x ${shell_path} 2>/dev/null
    sh ${shell_path}

    rm -f ${shell_path} 2>/dev/null
    report_info "100" "NULL"
}

main 

