#!/bin/bash
source $(dirname $0)/common_function.sh

SHELL_PATH=$1

function main()
{
    init
    chmod +x ${SHELL_PATH}
    sh ${SHELL_PATH}

    chmod -R 777 ${g_task_dir}/*
	  report_info "100" "NULL"
}

main 

