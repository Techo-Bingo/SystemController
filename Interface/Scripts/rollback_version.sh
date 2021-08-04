#!/bin/bash
source ${g_home_dir}/common_function.sh

function print_progress_info()
{
  rm -f ${tmp_file} 2>/dev/null
  local tmp_file='/home/ubp/sh_log/bingo_tmp_print.log'
  local info_file='/home/ubp/sh_log/descinfo.log'
  for i in {1..720}
  do
      sleep 5
      if [ ! -f "${tmp_file}" ]
      then
          cp ${info_file} ${tmp_file}
          cat ${tmp_file} |grep -v '^total'
          continue
      fi
      diff ${tmp_file} ${info_file} |grep '> ' |awk -F"> " '{print $2}' |grep -v '^total'
      cp ${info_file} ${tmp_file}
      [ $(ps -ef|grep -v grep|grep -c 'restore.sh') -eq 0 ] && break
  done
  rm -f ${tmp_file} 2>/dev/null
}

function main()
{
    if [ $(whoami) != 'root' ]
    then
        echo "Please switch root !"
        report_err "20" "Please switch root !"
    fi
    if [ ! -d "/home/upgradeinstall/backup" ]
    then
        echo "Not upgrade yet, can't rollback !"
        report_err "25" "Not upgrade yet, can't rollback !"
    fi
    if [ ! -d "/home/ubp/upgradeinstall/upgrade" ]
    then
        echo "/home/ubp/upgradeinstall/upgrade don't exist, can't rollback !"
        report_err "25" "/home/ubp/upgradeinstall/upgrade don't exist, can't rollback !"
    fi

    local ne_ver_ini='/opt/UBP/conf/version.mdc.ini'
    local isp_ver_ini='/opt/UBP/conf/version.isp.ini'
    [ -f "${ne_ver_ini}" ] && echo_info "Current NE Version: $(grep "InternalID" ${ne_ver_ini} |cut -d"=" -f 2)"
    [ -f "${isp_ver_ini}" ] && echo_info "Current ISP Version: $(grep "InternalID" ${isp_ver_ini} |cut -d"=" -f 2)"

    print_progress_info &

    /home/ubp/upgradeinstall/upgrade/clean_result.sh &>/dev/null

    /home/ubp/upgradeinstall/upgrade/restore.sh 'web' &>/dev/null

    [ -f "${ne_ver_ini}" ] && echo_info "Current NE Version: $(grep "InternalID" ${ne_ver_ini} |cut -d"=" -f 2)"
    [ -f "${isp_ver_ini}" ] && echo_info "Current ISP Version: $(grep "InternalID" ${isp_ver_ini} |cut -d"=" -f 2)"

    report_info "100" "NULL"
}

main 
exit 0
