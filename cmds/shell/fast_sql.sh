#!/bin/bash
source ${g_home_dir}/common_function.sh

FILE_NAME=$1

function runsql()
{
    [ ! -f "/opt/UBP/bin/exec_sql" ] && report_err "20" "exec_sql don't exist !"
    local sql=$(cat ${g_upload_dir}/${FILE_NAME})
    . /opt/UBP/svc_profile.sh
    /opt/UBP/bin/exec_sql <<EOF
${sql};
EOF

	report_info "100" "NULL"
}

function main()
{
    runsql
}

main
exit 0

