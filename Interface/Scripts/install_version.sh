#!/bin/bash
source ${g_home_dir}/common_function.sh

PACK_NAME=$1
LANG=$2
PRODUCT=$3
PROTO=$4
MDC_IP=$5
UDC_IP=$6
NE='MDC'
NE_LIST='MDC:BCC+BDC'

function param_check()
{
	if [ -z "${MDC_IP}" ]
	then
		echo_info "MDC IP不可为空"
		report_err '10' "MDC IP不可为空"
	fi
	
	[ "${PRODUCT}" = '无线专网(PWI)' ] && PRODUCT='PWI' || PRODUCT='ICP'
	[ "${PROTO}" = '3GPP' ] && PROTO='2' || PROTO='4'
	if [ "${UDC_IP}" = '__None__' ]
	then
	  UDC_IP=''
	else
		NE_LIST="${NE_LIST}|UDC:UDC_normal"
		NE="${NE}+UDC"
	fi

	local info="请勾选root执行"
	if [ $(whoami) != 'root' ]
	then
		echo_info "${info}"
		report_err "20" "${info}"
	fi
	
	local info="版本包文件缺失，请重新上传"
	if [ ! -f "${g_upload_dir}/${PACK_NAME}" ]
	then
		echo_info ${info}
		report_err "25" "${info}"
	fi

	return 0
}

function main()
{
	mv ${g_upload_dir}/${PACK_NAME} ${g_task_dir}
	cd ${g_task_dir}
	tar xzmf ${PACK_NAME}
	report_func "$?" "解压版本安装包" 30 'Y'

	if [ ! -f "eApp.sha512" ] || [ $(sha512sum -c eApp.sha512 &>/dev/null && echo 0 || echo 1) != '0' ]
	then
		report_func "1" "校验版本包完整性" 35 'Y'
	else
		report_func "0" "校验版本包完整性" 35 'Y'
	fi
	
	if [ -f /opt/UBP/uninstall.sh ]
	then
		cp /opt/UBP/uninstall.sh ./
		./uninstall.sh -d 0 >>__install.log 2>&1
		report_func '0' "旧版本卸载" 50 'Y'
	fi

	local udc_id="4$(cat /dev/urandom|head -n 10|cksum |head -c 8)"
	local udc_pwd="3B17446263D9A2E7D8A1A5CA59E8FA96F7605A8CD9E0954B18BBE6E5743B84FD448AB974FD667EA8A8C26827CBEA552E2239A435F09CB793F1469B8E5BFD5295"
	local setup_shell='./setup_ch.sh'
	[ "${LANG}" = '中文' ] && local setup_shell='./setup_en.sh'
	local setup_udc_ip=${UDC_IP}
	[ -z "${setup_udc_ip}" ] && local setup_udc_ip=${MDC_IP}
	echo "${setup_shell} -d ${NE} -u '0' \"${udc_id}\" \"${udc_pwd}\" -i \"${MDC_IP}\" \"${setup_udc_ip}\" -s \"${PROTO}\" -n N -a \"${PRODUCT}\"" >>__install.log 2>&1
	${setup_shell} -d ${NE} -u '0' "${udc_id}" "${udc_pwd}" -i "${MDC_IP}" "${setup_udc_ip}" -s "${PROTO}" -n N -a "${PRODUCT}" >>__install.log 2>&1
	report_func "$?" "安装新版本" 70 'Y'

	echo "/opt/UBP/bin/mod_hostname.sh \"$(hostname)\" \"\" \"${MDC_IP}\" \"${MDC_IP}\" \"${MDC_IP}\" \"${UDC_IP}\" \"${UDC_IP}\" \"${UDC_IP}\" \"${UDC_IP}\" \"\" \"\" \"\" \"${NE_LIST}\" \"NO\" \"127.0.0.1\" \"${PROTO}\" \"customScene\" \"\" \"\"" >>__install.log 2>&1
	/opt/UBP/bin/mod_hostname.sh "$(hostname)" "" "${MDC_IP}" "${MDC_IP}" "${MDC_IP}" "${UDC_IP}" "${UDC_IP}" "${UDC_IP}" "${UDC_IP}" "" "" "" "${NE_LIST}" "NO" "127.0.0.1" "${PROTO}" "customScene" "" "" >>__install.log 2>&1
	report_func "$?" "应用模式切换" 80 'Y'

	/opt/UBP/bin/udc_install/mod_udc_service.sh "${PROTO}" >>__install.log 2>&1
	su - ubp -c ". /opt/UBP/svc_profile.sh; ubp_adm -cmd start" >>__install.log 2>&1
	su - ubp -c "/opt/ubp_websvc/webrestart.sh" >>__install.log 2>&1

  local count=0
  for ((i=0;i<30;i++))
  do
	  . /opt/UBP/svc_profile.sh >>__install.log 2>&1
	  local count=$(ubp_adm -cmd status|grep -w 'Not Running: 0'|wc -l)
	  [ ${count} -eq 1 ] && break
	  sleep 10
	done
	if [ ${count} -ne 1 ]
	then
		report_func '1' "启动服务" 95 'Y'
	else
		report_func '0' "启动服务" 95 'Y'
	fi

	local ne_ver_ini='/opt/UBP/conf/version.mdc.ini'
  local isp_ver_ini='/opt/UBP/conf/version.isp.ini'
  [ -f "${ne_ver_ini}" ] && echo_info "Current NE Version: $(grep "InternalID" ${ne_ver_ini} |cut -d"=" -f 2)"
  [ -f "${isp_ver_ini}" ] && echo_info "Current ISP Version: $(grep "InternalID" ${isp_ver_ini} |cut -d"=" -f 2)"
	
	echo_info "清理安装目录"
	ls |grep -v "__*"|xargs rm -rf >>__install.log 2>&1
  report_info "100" "${g_task_dir}/__install.log"
}

param_check
main
exit 0

