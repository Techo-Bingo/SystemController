#!/bin/bash
. /opt/UBP/svc_profile.sh
g_ha_mode='NA'
g_ha_status='NA'
g_mrs_ha_mode='NA'
g_remote_ip='NA'
g_kpld_status='NA'
g_mysql_status='NA'
g_mysql_sync='NA'
g_file_sync='NA'
g_ssh_trust='NA'
g_vip_status='NA'
g_ha_alarm='NA'

function ps_count()
{
	return $(ps -ef|grep "$1"|grep -v grep|wc -l)
}
function get_deploy()
{
	python /opt/UBP/bin/get_deploy_hostcfg_field.pyc $1
}
function get_ha_mode()
{
	g_ha_mode=$(get_deploy HA_MODE)
}
function get_ha_status()
{
	g_ha_status=$(/opt/add-ons/keepalived/bin/get_kpld_status.sh)
}
function get_mrs_ha_mode()
{
	g_mrs_ha_mode=$(get_deploy MRS_HA_MODE)
	[ -z "${g_mrs_ha_mode}" ] && g_mrs_ha_mode='NA'
}
function get_remote_ip()
{
	g_remote_ip=$(get_deploy HA_BACKUP_IP)
	[ -z "${g_remote_ip}" ] && g_remote_ip='NA'
}
function get_kpld_status()
{
	[ "${g_ha_status}" = 'STANDALONE' ] && return 0
	ps_count 'keepalived -D'
	if [ $? -ne 0 ]
	then
		g_kpld_status='Success'
	else
		g_kpld_status='Fail'
	fi
}
function get_mysql_status()
{
	local count=$(/sbin/service eappmysql status|grep done|wc -l)
	if [ $count -eq 0 ]
	then
		g_mysql_status='Fail'
	else
		g_mysql_status='Success'
	fi
}
function get_mysql_sync()
{
	if [ "${g_mrs_ha_mode}" != 'NA' ]
	then
		[ "${g_remote_ip}" = 'NA' ] && return 0
	else
		[ "${g_ha_status}" = 'STANDALONE' -o "${g_remote_ip}" = 'NA' ] && return 0
	fi
	local state=$(/opt/add-ons/keepalived/bin/ha_functions.sh check_slave_thread)
	if [ "${state}" = 'Yes Yes' ]
	then
		g_mysql_sync='Success'
	else
		g_mysql_sync='Fail'
	fi
}
function get_file_sync()
{
	if [ "${g_ha_status}" = 'MASTER online' ]
	then
		[ "${g_remote_ip}" = 'NA' ] && return 0
		local count=$(ps -ef|grep '/opt/add-ons/keepalived/bin/inotify_sync_one.sh'|grep -v grep|wc -l)
		if [ $count -eq 0 ]
		then
			g_file_sync='Fail'
		else
			g_file_sync='Success'
		fi
	elif [ "${g_ha_status}" = 'SLAVE online' ]
	then
		local count1=$(crontab -l|grep '/opt/add-ons/keepalived/bin/sync_files.sh'|wc -l)
		local count2=$(grep '/opt/add-ons/keepalived/bin/sync_files.sh' /opt/UBP/bin/crontab/etc/crontab_task.ini|wc -l)
		if [ $count1 -eq 0 -a $count2 -eq 0 ]
		then
			g_file_sync='Fail'
		else
			g_file_sync='Success'
		fi
	fi
}
function get_ssh_trust()
{
	if [ "${g_ha_status}" = 'STANDALONE' ]
	then
		return 0
	fi
	local remote_ip=$(get_deploy HA_BACKUP_IP)
	[ -z "${remote_ip}" ] && return 0
	su - ubp -c "/opt/add-ons/keepalived/bin/check_ssh_trust.ex ${remote_ip}"
	if [ $? -eq 0 ]
	then
		g_ssh_trust='Success'
	else
		g_ssh_trust='Fail'
	fi
}
function get_vip_status()
{
	if [ "${g_ha_status}" != 'MASTER online' ]
	then
		return 0
	fi
	g_vip_status='Success'
}
function get_ha_alarm()
{
	local tempallfm="/tmp/tmp_ha_allfm.tmp"
	/opt/UBP/bin/exec_sql <<EOF >$tempallfm
select * from ubpdb.TBL_UbpSyncSsnAlarm\G
EOF
	local nullline=`grep -n "clearTime:" $tempallfm |awk -F: '$3~/^ $/{print $1}'`
	for line in $nullline
	do
		alarmID=$(($line-5))
		alarmSN=$(($line-4))
		v_alarmID=`sed -n "$alarmID p" $tempallfm |awk '{print $2}'`
		v_alarmSN=`sed -n "$alarmSN p" $tempallfm |awk '{print $2}'`
		if [ "$v_alarmID" = "1031" -o "$v_alarmID" = "1040" -o "$v_alarmID" = '1019' -o "${v_alarmID}" = '1017' ]
		then
			[ "${g_ha_alarm}" = 'NA' ] && g_ha_alarm=${v_alarmID} && continue
			g_ha_alarm="${g_ha_alarm}|${v_alarmID}"
		fi
	done
}
main()
{
	get_ha_mode
	get_ha_status
	get_mrs_ha_mode
	get_remote_ip
	get_kpld_status
	get_mysql_status
	get_mysql_sync
	get_file_sync
	get_ssh_trust
	get_vip_status
	get_ha_alarm
}
main >/dev/null 2>&1
echo "__BINGO__HA_MODE:${g_ha_mode}"
echo "HA_STATUS:${g_ha_status}"
echo "MRS_HA_MODE:${g_mrs_ha_mode}"
echo "REMOTE_IP:${g_remote_ip}"
echo "KEEPALIVED_STATUS:${g_kpld_status}"
echo "MYSQL_STATUS:${g_mysql_status}"
echo "MYSQL_SYNC:${g_mysql_sync}"
echo "FILE_SYNC:${g_file_sync}"
echo "SSH_TRUST:${g_ssh_trust}"
echo "VIP_STATUS:${g_vip_status}"
echo "HA_ALARM:${g_ha_alarm}__BINGO__"


