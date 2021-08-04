#!/bin/bash
source ${g_home_dir}/common_function.sh

VERSION_PACK=$1
UPGRADE_PACK=$2
UPLOAD_PATH='/home/ubp/upload/swm'

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
      [ $(ps -ef|grep -v grep|grep -c 'upgrade.sh') -eq 0 ] && break
  done
  rm -f ${tmp_file} 2>/dev/null
}

function prev_check()
{
	[ $(whoami) != 'root' ] && report_func 1 "请勾选root执行" 15
  [ ! -f "${g_upload_dir}/${VERSION_PACK}" ] && report_func 1 "版本包文件缺失" 20
  [ ! -f "${g_upload_dir}/${UPGRADE_PACK}" ] && report_func 1 "升级包文件缺失" 20

  local ne_ver_ini='/opt/UBP/conf/version.mdc.ini'
  local isp_ver_ini='/opt/UBP/conf/version.isp.ini'
  [ -f "${ne_ver_ini}" ] && echo_info "Current NE Version: $(grep "InternalID" ${ne_ver_ini} |cut -d"=" -f 2)"
  [ -f "${isp_ver_ini}" ] && echo_info "Current ISP Version: $(grep "InternalID" ${isp_ver_ini} |cut -d"=" -f 2)"

  rm -rf ${UPLOAD_PATH}/*
  mkdir -p ${UPLOAD_PATH} /home/ubp/upgradeinstall/
  chown ubp:ubpsysm ${UPLOAD_PATH} /home/ubp/upgradeinstall/
  mv ${g_upload_dir}/${VERSION_PACK} ${UPLOAD_PATH}
  mv ${g_upload_dir}/${UPGRADE_PACK} ${UPLOAD_PATH}

  tar -zxmf ${UPLOAD_PATH}/${UPGRADE_PACK} -C /home/ubp/upgradeinstall/
  report_func "$?" "升级包解压" 20

  chown ubp:ubpsysm /home/ubp/upgradeinstall/upgrade
  chown ubp:ubpsysm /home/ubp/upgradeinstall/upgrade/* -R
  chmod 750 /home/ubp/upgradeinstall/upgrade/* -R
  cd /home/ubp/upgradeinstall/upgrade/

  /home/ubp/upgradeinstall/upgrade/clean_result.sh uploade &>/dev/null
  report_func "$?" "升级包上传、升级路径校验" 30

  /home/ubp/upgradeinstall/upgrade/clean_result.sh &>/dev/null

  /home/ubp/upgradeinstall/upgrade/upgradecheck.sh &>/dev/null
  report_func "$?" "升级前检查" 30

  print_progress_info &

  /home/ubp/upgradeinstall/upgrade/upgrade.sh &>/dev/null
  report_func "$?" "升级结束" 100

  [ -f "${ne_ver_ini}" ] && echo_info "Current NE Version: $(grep "InternalID" ${ne_ver_ini} |cut -d"=" -f 2)"
  [ -f "${isp_ver_ini}" ] && echo_info "Current ISP Version: $(grep "InternalID" ${isp_ver_ini} |cut -d"=" -f 2)"

}

function main()
{
  prev_check
}

main
exit 0
