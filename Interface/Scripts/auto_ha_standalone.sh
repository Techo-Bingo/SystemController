#!/bin/bash
source ${g_home_dir}/common_function.sh

OP_TYPE=$1
ha_common=/opt/UBP/bin/ha/ha_common.pyc
ha_status=/opt/UBP/conf/ha/ha_status_conf.json

function get_ha_status()
{
  [ ! -f "$ha_common" ] && { echo "环境不支持"; exit 1; }
  [ ! -f "$ha_status" ] && { echo "单机"; exit 1; }
  status=$(python $ha_common get_json_value $ha_status HA_STATUS)
  mode=$(python $ha_common get_json_value $ha_status MODE_EX)

  if [ "$mode" = 'LOCAL_ACTIVE' ]
  then
    mode='生产主机'
  elif [ "$mode" = 'LOCAL_STANDBY' ]
  then
    mode='生产备机'
  elif [ "$mode" = 'REMOTE_ACTIVE' ]
  then
    mode='容灾主机'
  elif [ "$mode" = 'REMOTE_STANDBY' ]
  then
    mode='容灾备机'
  else
    mode='单机'
  fi
  [ "$status" = 'OnActive' ] && { echo "$mode   主用机"; exit 0; }
  [ "$status" = 'OnStandby' ] && { echo "$mode   备用机"; exit 0; }
  [ "$status" = 'OnStandalone' ] && { echo "$mode   单机"; exit 0; }
  [ "$status" = 'Unknown' ] && { echo "$mode   未知"; exit 0; }
  echo "单机"
}

function config_standalone()
{
  [ "$(whoami)" != 'ubp' ] && report_err 1 "请使用 ubp 用户执行"
  local_ip=$(python /opt/UBP/bin/get_deploy_hostcfg_field.pyc HA_LOCAL_IP)
  # ha_mode=$(python /opt/UBP/bin/get_deploy_hostcfg_field.pyc HA_MODE)
  # [ "$ha_mode" = 'MASTER' -o "$ha_mode" = "SLAVE" ] || { report_info 100 "NULL"; return 0; }

  report_info 20 "拆单中,请稍候"
  python /opt/UBP/bin/ha/ha_config.pyc no AUTO-HA-STANDALONE@2@admin@2@$(date +'%F-%T')@1@1@1@1@1 <<EOF
STANDALONE $local_ip null null
EOF

  [ $? -ne 0 ] && report_err 90 "拆单失败, 请查看日志/home/ubp/sh_log/ha_config.log"
  report_info 100 NULL
  return 0
}

function main()
{
	if [ "${OP_TYPE}" = 'ENTER' ]
	then
		get_ha_status
	else
	  config_standalone
	fi
}

main
exit 0

