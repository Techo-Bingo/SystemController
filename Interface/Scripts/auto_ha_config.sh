#!/bin/bash
source ${g_home_dir}/common_function.sh

VIPS=$1
LOCAL_A=$2
LOCAL_S=$3
REMOTE_A=$4
REMOTE_S=$5
UBP_PWD=$6
DB_PWD=$7
# 物理区域 #
WHOAMI=''
# 本机IP #
LOCAL_IP=''
# 目标IP #
REMOTE_IPS=''
# 优先级更高的IP #
PREV_IPS=''
# 等待一小时仍没有完成,则超时退出 #
TIMEOUT=3600
ready_flag='/home/ubp/auto_ha_config.flag'
sudo_wrapper="sudo /opt/UBP/bin/sudo_wrapper.sh"
ssh_trust_tool="/opt/UBP/bin/distribute/ssh-trust.ex"

[ "$LOCAL_A" = '__None__' ] && LOCAL_A=''
[ "$LOCAL_S" = '__None__' ] && LOCAL_S=''
[ "$REMOTE_A" = '__None__' ] && REMOTE_A=''
[ "$REMOTE_S" = '__None__' ] && REMOTE_S=''

function my_report_func()
{
  [ "$1" != '0' ] && echo "FAILED" >"$ready_flag" 2>/dev/null
  report_func "$1" "$2" "$3" Y
}

function who_am_i()
{
  echo "RUNNING" >$ready_flag
  chown ubp:ubpsysm $ready_flag

  bit=$(echo $VIPS | cut -d'/' -f2)
  [ "$bit" -le 32 ] || my_report_func 1 "掩码输入有误" 10
  [ "$bit" -ge 0 ] || my_report_func 1 "掩码输入有误" 10
  [ -z "$LOCAL_A" ] && my_report_func 1 "生产主机IP不能为空" 10
  echo "$LOCAL_A" > aa.ini
  echo "$LOCAL_S" >> aa.ini
  echo "$REMOTE_A" >> aa.ini
  echo "$REMOTE_S" >> aa.ini
  sed -i '/^$/d' aa.ini
  [ $(cat aa.ini | sort | uniq | wc -l) -ne $(cat aa.ini | wc -l) ] && my_report_func 1 "主备容灾IP输入重复" 10

  [ -z "$UBP_PWD" -o -z "$DB_PWD" ] && my_report_func 1 "ubp密码和db密码不能为空" 10
  [ "$(whoami)" != 'ubp' ] && my_report_func 1 '请使用 ubp 用户执行' 15
  [ ! -f '/opt/UBP/bin/ha/ha_config.ini' ] && my_report_func 1 '该版本不支持主备容灾, 请确认' 15
  my_report_func 0 "当前平台版本号: $(grep -w 'InternalID' /opt/UBP/conf/version.isp.ini | cut -d= -f2)" 15
  my_report_func 0 "当前网元版本号: $(grep -w 'InternalID' /opt/UBP/conf/version.mdc.ini | cut -d= -f2)" 15

  local ip_info=$(ip a)
  if [ $(echo "$ip_info" | grep -w "$LOCAL_A" | wc -l) -ne 0 ]
  then
    WHOAMI='LOCAL_ACTIVE'
    LOCAL_IP=$LOCAL_A
    REMOTE_IPS="$LOCAL_S $REMOTE_A $REMOTE_S"
    PREV_IPS=''
  elif [ $(echo "$ip_info" | grep -w "$LOCAL_S" | wc -l) -ne 0 ]
  then
    WHOAMI='LOCAL_STANDBY'
    LOCAL_IP=$LOCAL_S
    REMOTE_IPS="$LOCAL_A $REMOTE_A $REMOTE_S"
    PREV_IPS="$LOCAL_A"
  elif [ $(echo "$ip_info" | grep -w "$REMOTE_A" | wc -l) -ne 0 ]
  then
    WHOAMI='REMOTE_ACTIVE'
    LOCAL_IP=$REMOTE_A
    REMOTE_IPS="$LOCAL_A $LOCAL_S $REMOTE_S"
    PREV_IPS="$LOCAL_A $LOCAL_S"
  elif [ $(echo "$ip_info" | grep -w "$REMOTE_S" | wc -l) -ne 0 ]
  then
    WHOAMI='REMOTE_STANDBY'
    LOCAL_IP=$REMOTE_S
    REMOTE_IPS="$LOCAL_A $LOCAL_S $REMOTE_A"
    PREV_IPS="$LOCAL_A $LOCAL_S $REMOTE_A"
  fi
  [ "$WHOAMI" = '' ] && my_report_func 1 '该环境不是主备容灾组网环境,请勾选正确的IP' 20
}

function check_env()
{
    echo "LOCAL_A $LOCAL_A"
    echo "LOCAL_S $LOCAL_S"
    echo "REMOTE_A $REMOTE_A"
    echo "REMOTE_S $REMOTE_S"
    echo "WHIAMI $WHOAMI"
    echo "LOCAL_IP $LOCAL_IP"
    echo "REMOTE_IPS $REMOTE_IPS"
    echo "PREV_IPS $PREV_IPS"
    local ha_mode=$(python /opt/UBP/bin/get_deploy_hostcfg_field.pyc HA_MODE)
    [ "$ha_mode" = 'SLAVE' -o "$ha_mode" = 'MASTER' ] && my_report_func 1 "该环境非单机,请先拆单后再组主备容灾" 20
    local om_ip=$(python /opt/UBP/bin/get_deploy_hostcfg_field.pyc om_ip)
    [ "$om_ip" != "$LOCAL_IP" ] && my_report_func 1 "$LOCAL_IP 不是 deploy 的 om_ip" 20
}

function set_ubp_trust()
{
  $sudo_wrapper check_ubp_pwd $LOCAL_IP <<EOF
$UBP_PWD
EOF
  my_report_func $? "本地ubp密码校验" 22

  for ip in $REMOTE_IPS
  do
  $sudo_wrapper unlock_ubp
  $ssh_trust_tool <<EOF
ubp/${UBP_PWD}@$ip
EOF
  my_report_func $? "建立互信 $LOCAL_IP --> $ip" 22

  ssh -n ubp@${ip} "$sudo_wrapper unlock_ubp
  $ssh_trust_tool <<EOF
ubp/$UBP_PWD@$LOCAL_IP
EOF"
  my_report_func $? "建立互信 $ip --> $LOCAL_IP" 22

  done
}

function wait_prev_ips()
{
  local start_time=$(date +%s)
  local ip_count=$(echo "$PREV_IPS" | tr ' ' '\n' | wc -l)
  while true
  do
    sleep 30
    [ $(expr $(date +%s) - $start_time) -ge $TIMEOUT ] && my_report_func 1 "等待超时退出" 50

    local ok_num=0
    for ip in $PREV_IPS
    do
      local state=$(ssh -n ubp@$ip "cat $ready_flag")
      echo "wait: $ip $state"

      [ "$state" = 'FAILED' ] && my_report_func 1 "检测到 $ip 失败, 本机退出配置" 50
      [ "$state" = 'DONE' ] && let ok_num++
    done

    [ $ok_num -eq $ip_count ] && break
    my_report_func 0 "正在等待 $PREV_IPS 配置..." 50
  done

  my_report_func 0 "$PREV_IPS 配置完成, 开始配置本机" 60
}

function config_vip()
{
  VIPS=$(echo "$VIPS" | tr ',' ' ')
  local tmp_file=/tmp/auto_ha_config.tmp
  local vip_conf=/opt/UBP/conf/ha/floatIp.cnf
  > $tmp_file
  > $vip_conf
  local dft_gw=$(grep 'default' /etc/sysconfig/network/routes | cut -d ' ' -f2)
  [ -z "dft_gw" ] && my_report_func 1 "默认网关为空" 40
  local cards=$(ip addr |grep -w "UP"|grep -vw "DOWN"|grep -vw "LOOPBACK"|awk '{print $2}'|sed 's/://g')
  for card in $cards
  do
    echo "interface net card: $card "
    for ip_mask in $(ip a | grep -wv lo | grep -w inet | grep -w "$card" | awk '{print $2}')
    do
      ip=$(echo "$ip_mask" | cut -d'/' -f1)
      bit=$(echo "$ip_mask" | cut -d'/' -f2)
      range=$(python <<EOF
import sys
sys.path.append("../")
from function_util import IPv4Address
print('-'.join(IPv4Address().get_range_by_ip_bit("$ip", $bit)))
EOF
)
    gw=$(grep -w "$card" /etc/sysconfig/network/routes | cut -d' ' -f2 | head -1)
    [ -z "$gw" ] && gw=$dft_gw
    echo "$range $card $gw" >>$tmp_file
    done
  done

  id=0
  for vip in $VIPS
  do
    ip=$(echo "$vip" | cut -d'/' -f1)
    bit=$(echo "$vip" | cut -d'/' -f2)
    range=$(python <<EOF
import sys
sys.path.append("../")
from function_util import IPv4Address
print('-'.join(IPv4Address().get_range_by_ip_bit("$ip", $bit)))
EOF
)
  echo "find ip range for net card: $range"
  card=$(grep -w "$range" $tmp_file | awk '{print $2}')
  [ -z "$card" ] && my_report_func 1 "未找到 $ip 对应网卡信息, 浮动IP配置失败" 40

  gw=$(grep -w "$range" $tmp_file | awk '{print $3}')
  broadcast=$(echo $range | cut -d'-' -f2)
  let id++

  my_report_func 0 "设置浮动IP-$id: '$ip $bit $broadcast $card $gw $id'" 40

  echo "$ip $bit $broadcast $card $gw $id" >>$vip_conf
  done
}

function config_start()
{
  if [ "$WHOAMI" = 'LOCAL_ACTIVE' ]
  then
    python /opt/UBP/bin/ha/ha_config.pyc no AUTO-HA-CONFIG@2@admin@2@$(date +'%F-%T')@1@1@1@1@1 <<EOF
LOCAL_ACTIVE $LOCAL_IP $UBP_PWD $DB_PWD
EOF
  elif [ "$WHOAMI" = 'LOCAL_STANDBY' ]
  then
    python /opt/UBP/bin/ha/ha_config.pyc yes AUTO-HA-CONFIG@2@admin@2@$(date +'%F-%T')@1@1@1@1@1 <<EOF
LOCAL_STANDBY $LOCAL_IP $UBP_PWD $DB_PWD
CURR_ACTIVE $LOCAL_A $UBP_PWD $DB_PWD
EOF
  elif [ "$WHOAMI" = 'REMOTE_ACTIVE' ]
  then
    python /opt/UBP/bin/ha/ha_config.pyc yes AUTO-HA-CONFIG@2@admin@2@$(date +'%F-%T')@1@1@1@1@1 <<EOF
REMOTE_ACTIVE $LOCAL_IP $UBP_PWD $DB_PWD
CURR_ACTIVE $LOCAL_A $UBP_PWD $DB_PWD
EOF
  elif [ "$WHOAMI" = 'REMOTE_STANDBY' ]
  then
    python /opt/UBP/bin/ha/ha_config.pyc yes AUTO-HA-CONFIG@2@admin@2@$(date +'%F-%T')@1@1@1@1@1 <<EOF
REMOTE_STANDBY $LOCAL_IP $UBP_PWD $DB_PWD
CURR_ACTIVE $LOCAL_A $UBP_PWD $DB_PWD
EOF
  fi
  my_report_func $? "$WHOAMI 主备容灾配置" 90
}

function post_done()
{
  echo "DONE" > $ready_flag
  chown ubp:ubpsysm $ready_flag
  my_report_func 0 "本机配置完成" 100
}

function main()
{
  who_am_i
  check_env
  set_ubp_trust
  config_vip
  [ -n "$PREV_IPS" ] && wait_prev_ips
  config_start
  post_done
  report_info "100" "NULL"
}

main >> ${g_task_dir}/${g_log} 2>&1
exit 0

