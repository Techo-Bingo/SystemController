#!/bin/bash
source $(dirname $0)/common_function.sh

SHELL_PATH=$1

function main()
{
    init
    dos2unix ${SHELL_PATH} 2>/dev/null
    chmod +x ${SHELL_PATH} 2>/dev/null
    sh ${SHELL_PATH}

    chmod -R 777 ${g_task_dir}/* 2>/dev/null
    rm -f ${SHELL_PATH} 2>/dev/null
    report_info "100" "NULL"
}

main 

