#!/bin/bash
source ${g_home_dir}/common_function.sh

LOG_FLAGS=$1

function parser_param()
{
	ISP_FLAG=$(echo ${LOG_FLAGS}|awk -F"@" '{print $1}')
	MDC_FLAG=$(echo ${LOG_FLAGS}|awk -F"@" '{print $2}')
	UDC_FLAG=$(echo ${LOG_FLAGS}|awk -F"@" '{print $3}')
	MRS_FLAG=$(echo ${LOG_FLAGS}|awk -F"@" '{print $4}')
	SDS_SSC_FLAG=$(echo ${LOG_FLAGS}|awk -F"@" '{print $5}')
	SYS_FLAG=$(echo ${LOG_FLAGS}|awk -F"@" '{print $6}')

	if [ "${SYS_FLAG}" = '1' ]
	then
    [ "$(whoami)" != "root" ] && report_err 10 "系统日志采集需要 root 执行"
	fi

}

function get_isp_logs()
{
	cd ${g_task_dir} && mkdir isp_log ; cd isp_log
	report_info '25' "collect ISP script logs start..."
	cp -rf /home/ubp/sh_log ./
	cp -rf /home/ubp/logs/keepalived ./
	cp -rf /home/ubp/logs/oam_log ./
	cp -rf /home/ubp/logs/gap ./
	cp -rf /home/ubp/logs/rsync ./
	cp -rf /home/ubp/logs/consul ./
	cp -rf /home/ubp/logs/ruling_server ./
	cp -rf /home/ubp/logs/ubp_collect.log ./
	cp -rf /home/ubp/logs/eapp_ntp*.log ./
	cp -rf /home/ubp/logs/database_backup.log ./
	cp -rf /home/ubp/logs/ubp_trunc_logs.log ./
	cp -rf /home/ubp/logs/whitename.log ./
	cp -rf /home/ubp/logs/setdns_init.log ./
	cp -rf /home/ubp/logs/sca_monitor.log ./
	cp -rf /home/ubp/logs/ubp_monitor_3rd_svcs.log ./
	cp -rf /home/ubp/logs/ubp_log_back_sh.log ./
	cp -rf /home/ubp/logs/rm_userlog_devlog.log ./
	cp -rf /home/ubp/logs/auto_add_route.log ./
	cp -rf /home/ubp/logs/change_dbmpwd.log ./
	cp -rf /home/ubp/logs/start_ubp.log ./
	cp -rf /home/ubp/logs/mod_pw.log ./
	cp -rf /home/ubp/logs/modify_route.log ./
	cp -rf /home/ubp/logs/modify_ip.log ./
	cp -rf /home/ubp/logs/ubp_config_service_mod.log ./
	cp -rf /home/ubp/logs/deploy_config.log ./
	cp -rf /home/ubp/logs/sca_killsvc.log ./
	cp -rf /home/ubp/logs/sca_adm_killall_svc.log ./
	cp -rf /home/ubp/logs/config_service_mod.log ./
	cp -rf /home/ubp/logs/rsync_monitor.log ./
	cp -rf /home/ubp/logs/inotify_rsync_caller.log ./
	cp -rf /home/ubp/logs/inotify_rsync_daemon.log ./
	cp -rf /home/ubp/logs/inotify_rsync_dir.log ./
	cp -rf /home/ubp/logs/inotify_rsync_file.log ./
	cp -rf /home/ubp/logs/manual_daemon_rsync_dir.log ./
	cp -rf /home/ubp/logs/redis_cmd.log ./
	cp -rf /home/ubp/logs/qc.log ./
	cp -rf /home/ubp/logs/nhc.log ./
	cp -rf /home/ubp/logs/ubp_exportdb.log ./
	cp -rf /home/ubp/logs/ubp_importdb.log ./
	cp -rf /home/ubp/logs/slaveoperate.log ./
	cp -rf /home/ubp/logs/nginx_log/nginxaccess.log ./
	cp -rf /opt/UBP/conf/deploy_policy_4.0.xml ./
	cp -rf /opt/UBP/conf/version.*.ini ./
	cp -rf ${EAPP_MYSQL_DATADIR}/*.err ./
	report_info '30' "collect ISP C++ logs start..."
	cp -rf /home/ubp/logs/ubp_cm.log ./
	cp -rf /home/ubp/logs/ubp_ad.log ./
	cp -rf /home/ubp/logs/ubp_lm.log ./
	cp -rf /home/ubp/logs/ubp_fm.log ./
	cp -rf /home/ubp/logs/ubp_daem.log ./
	cp -rf /home/ubp/logs/ubp_lic_man.log ./
	cp -rf /home/ubp/logs/ubp_maintain.log ./
	cp -rf /home/ubp/logs/ubp_monitor.log ./
	cp -rf /home/ubp/logs/ubp_mq_broker.log ./
	cp -rf /home/ubp/logs/ubp_omu.log ./
	cp -rf /home/ubp/logs/ubp_pfm.log ./
	cp -rf /home/ubp/logs/ubp_swm.log ./
	cp -rf /home/ubp/logs/ubp_adm.log ./
	cp -rf /home/ubp/logs/ubp_gap_crossing.log ./
	cp -rf /home/ubp/logs/ubp_security.log ./
	report_info '33' "collect ISP web logs start..."
	cp -rf /opt/ubp_websvc/tomcat6/logs/catalina.out ./
	cp -rf /opt/ubp_websvc/tomcat6/webapps/ROOT/WEB-INF/classes/*.properties
	report_info '35' "collect ISP logs success"
}

function get_mdc_logs()
{
	cd ${g_task_dir} && mkdir mdc_log ; cd mdc_log
	report_info '40' "collect MDC logs start..."
	cp -rf /home/ubp/logs/ubp_bcc*.log ./
	cp -rf /home/ubp/logs/ubp_bdc*.log ./
	cp -rf /home/ubp/logs/ubp_dec_vgw.log ./
	cp -rf /home/ubp/logs/ubp_confmgr.log ./
	cp -rf /opt/UBP/conf/BccFlowControl.txt ./
	cp -rf /home/ubp/logs/ubp_diam_*.log ./
	cp -rf /home/ubp/logs/ubp_pres.log ./
	cp -rf /home/ubp/logs/ubp_km.log ./
	cp -rf /home/ubp/logs/ubp_sds_dataman.log ./
	cp -rf /home/ubp/logs/ubp_sslb.log ./
	cp -rf /home/ubp/logs/ubp_tas.log ./
	cp -rf /home/ubp/logs/ubp_nfsq.log ./
	cp -rf /home/ubp/logs/ubp_sdk_agent_ds.log ./
	cp -rf /home/ubp/logs/cdr ./
	cp -rf /home/ubp/logs/rtcp ./
	cp -rf /home/ubp/logs/ds ./
	report_info '45' "collect MDC logs success"
}

function get_udc_logs()
{
	cd ${g_task_dir} && mkdir udc_log ; cd udc_log
	report_info '50' "collect UDC logs start..."
	cp -rf /home/ubp/logs/devlog ./
	cp -rf /home/ubp/logs/userlog ./
	cp -rf /opt/UBP/logs/udc_java/tis ./
	cp -rf /opt/UBP/logs/udc_java/idms* ./
	cp -rf /opt/UBP/logs/udc_java/web ./
	cp -rf /opt/UBP/logs/udc_java/omp ./
	cp -rf /opt/UBP/logs/udc_java/bs ./
	cp -rf /opt/UBP/logs/udc_java/med ./
	cp -rf /opt/UBP/logs/udc_java/tem ./
	cp -rf /opt/UBP/logs/udc_java/ftp ./
	cp -rf /opt/UBP/logs/udc_java/push ./
	cp -rf /opt/UBP/logs/udc_java/ota ./
	cp -rf /opt/UBP/logs/udc_java/monitor ./
	cp -rf /home/ubp/logs/udc_*.log ./
	cp -rf /home/ubp/logs/xcap_*.log ./
	report_info '55' "collect UDC logs success"
}

function get_mrs_logs()
{
	cd ${g_task_dir} && mkdir mrs_log ; cd mrs_log
	report_info '60' "collect MRS logs start..."
	cp -rf /home/ubp/logs/ubp_mrs_*.log ./
	cp -rf /opt/mrs_web/tomcat6/logs/catalina.out ./
	report_info '65' "collect MRS logs success"
}

function get_sds_ssc_logs()
{
	cd ${g_task_dir} && mkdir sds_ssc_log ; cd sds_ssc_log
	report_info '70' "collect SDS/SSC logs start..."
	cp -rf /opt/UBP/logs/gisserver ./
	cp -rf /opt/UBP/logs/sds_logs ./
	cp -rf /opt/UBP/logs/ubp_sds_dataman.log ./
	cp -rf /opt/UBP/logs/ubp_nfsq.log ./
	report_info '75' "collect SDS/SSC logs success"
}

function get_sys_logs()
{
	cd ${g_task_dir} && mkdir system_log ; cd system_log
	report_info '80' "collect SYSTEM logs start..."
	cp -rf /etc/sysconfig/network/ifcfg* ./
	cp -rf /etc/sysconfig/network/route* ./
	cp -rf /etc/ntp.conf ./
	cp -rf /etc/resolv.conf ./
	cp -rf /etc/host.conf ./
	cp -rf /etc/named.conf ./
	cp -rf /var/log/messages* ./
	cp -rf /var/log/auth.log ./
	cp -rf /var/log/ntp ./
	cp -rf /var/log/sudo.log ./
	cp -rf /var/log/lastlog ./
	cp -rf /var/log/cron ./
	cp -rf /var/log/boot.msg ./
	cp -rf /var/log/kernel.log ./
	cp -rf /var/log/secure.log ./
	report_info '85' "collect SYSTEM state info start..."
	local sysinfofile=./SysInfo.log
	date '+%Y-%m-%d %H:%M:%S' > $sysinfofile
	echo "===uname -a info start==============================================" >> $sysinfofile
	uname -a >> $sysinfofile    
	echo "===uname -a info end================================================" >> $sysinfofile    
	echo >> $sysinfofile
	echo "===io info start==============================================" >> $sysinfofile    
	echo "/proc/sys/vm/dirty_ratio=$(cat /proc/sys/vm/dirty_ratio)" >> $sysinfofile  
	echo "/proc/sys/vm/dirty_writeback_centisecs=`cat /proc/sys/vm/dirty_writeback_centisecs`" >> $sysinfofile  
	for device in $(ls /sys/block/)
	do
		echo "/sys/block/$device/queue/scheduler=$(cat /sys/block/$device/queue/scheduler)" >> $sysinfofile  
	done
	echo "===io info end================================================" >> $sysinfofile
	echo >> $sysinfofile

	echo "===df -h info start=============================================="  >> $sysinfofile
	df -h >> $sysinfofile    
	echo "===df -h info end================================================"  >> $sysinfofile    
	echo >> $sysinfofile

	echo "===cat /proc/cpuinfo start=============================================="  >> $sysinfofile
	cat /proc/cpuinfo >> $sysinfofile    
	echo "===cat /proc/cpuinfo end================================================"  >> $sysinfofile    
	echo >> $sysinfofile

	echo "===cat /proc/meminfo start=============================================="  >> $sysinfofile
	cat /proc/meminfo >> $sysinfofile    
	echo "===cat /proc/meminfo end================================================"  >> $sysinfofile    
	echo >> $sysinfofile

	echo "===cat /proc/vmstat start=============================================="  >> $sysinfofile
	cat /proc/vmstat >> $sysinfofile    
	echo "===cat /proc/vmstat end================================================"  >> $sysinfofile    
	echo >> $sysinfofile

	echo "===chkconfig --list start=============================================="  >> $sysinfofile
	/sbin/chkconfig --list >> $sysinfofile    
	echo "===chkconfig --list end================================================"  >> $sysinfofile    
	echo >> $sysinfofile
	
	echo "===IP info start================================================="  >> $sysinfofile
	/sbin/ifconfig -a >> $sysinfofile    
	echo "===IP info end==================================================="  >> $sysinfofile
	echo >> $sysinfofile

	echo "===cat /etc/hosts start================================================="  >> $sysinfofile
	cat /etc/hosts >> $sysinfofile    
	echo "===cat /etc/hosts end==================================================="  >> $sysinfofile
	echo >> $sysinfofile
	
	echo "===cat /var/log/firewall start================================================="  >> $sysinfofile
	cat /var/log/firewall >> $sysinfofile    
	echo "===cat /var/log/firewall end==================================================="  >> $sysinfofile
	echo >> $sysinfofile

	echo "===top -d 2 -n 3 -b start=============================================="  >> $sysinfofile
	top -d 2 -n 3 -b >> $sysinfofile    
	echo "===top -d 2 -n 3 -b end================================================"  >> $sysinfofile    
	echo >> $sysinfofile
	
	echo "===dmesg info start=============================================="  >> $sysinfofile
	dmesg >> $sysinfofile    
	echo "===dmesg info end================================================"  >> $sysinfofile    
	echo >> $sysinfofile
	
	echo "===arp info start=============================================="  >> $sysinfofile
	arp >> $sysinfofile    
	echo "===arp info end================================================"  >> $sysinfofile    
	echo >> $sysinfofile
	
	echo "===cat /var/log/mcelog start================================================="  >> $sysinfofile
	cat /var/log/mcelog >> $sysinfofile
	echo "===cat /var/log/mcelog end================================================="  >> $sysinfofile
	echo >> $sysinfofile
	
	echo "===cat /var/log/mail.info start================================================="  >> $sysinfofile
	cat /var/log/mail.info >> $sysinfofile
	echo "===cat /var/log/mail.info end================================================="  >> $sysinfofile
	echo >> $sysinfofile
	
	echo "===cat /var/log/boot.msg start================================================="  >> $sysinfofile
	cat /var/log/boot.msg >> $sysinfofile
	echo "===cat /var/log/boot.msg end================================================="  >> $sysinfofile
	echo >> $sysinfofile

	echo "===env start================================================="  >> $sysinfofile
	env >> $sysinfofile
	echo "===env end================================================="  >> $sysinfofile
	echo >> $sysinfofile
	
	echo "===cat /etc/SuSE-release start================================================="  >> $sysinfofile
	cat /etc/SuSE-release >> $sysinfofile
	echo "===cat /etc/SuSE-release end================================================="  >> $sysinfofile
	echo >> $sysinfofile

	local allportsfile=./PortsInfo.csv
	date "+%F_%T" > $allportsfile
	echo "Proto,Recv-Q,Send-Q,Local-Address,Foreign-Address,State,PID/Program-name" >> $allportsfile
	# TCP ports
	netstat -atnp|tail -n +3|awk '{print $1","$2","$3","$4","$5","$6","$7}' >> $allportsfile
	# UDP ports
	netstat -aunp|tail -n +3|awk '{print $1","$2","$3","$4","$5",-,"$6}' >> $allportsfile
	report_info '90' "collect SYSTEM logs success"
}

function compress_pack()
{
	cd ${g_task_dir}
	local pack_name="quick_logs"
	report_info '92' "Compress ${pack_name} start..."
	local pack_name=$(compress ${pack_name})
	[ $? -ne 0 ] && report_err '95' "Compress ${pack_name} failed"
	report_info '100' "${g_task_dir}/${pack_name}"
}

function collect()
{
	cd ${g_task_dir}
	
	[ "${ISP_FLAG}" = '1' ] && get_isp_logs

	[ "${MDC_FLAG}" = '1' ] && get_mdc_logs
	
	[ "${UDC_FLAG}" = '1' ] && get_udc_logs
	
	[ "${MRS_FLAG}" = '1' ] && get_mrs_logs

	[ "${SDS_SSC_FLAG}" = '1' ] && get_sds_ssc_logs

	[ "${SYS_FLAG}" = '1' ] && get_sys_logs
}

function main()
{
	parser_param
	collect
	compress_pack
}

main
exit 0
