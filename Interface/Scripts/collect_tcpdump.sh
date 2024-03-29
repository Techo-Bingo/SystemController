#!/bin/bash
source ${g_home_dir}/common_function.sh

NET=$1
PROTO=$2
HOST=$3
PORT=$4
COUNT=$5
shift 5
OTHER=$*

function main()
{
	[ "$(whoami)" != 'root' ] && report_err "20" "请使用 root 执行"

  [ "${NET}" = '__None__' ] && NET='' || NET="-i ${NET}"
  [ "${PROTO}" = '__None__' ] && PROTO=''
  [ "${PROTO}" = 'TCP' ] && PROTO='tcp'
  [ "${PROTO}" = 'UDP' ] && PROTO='udp'
  [ "${COUNT}" = '__None__' ] && COUNT='' || COUNT="-c ${COUNT}"
  [ "${PORT}" = '__None__' ] && PORT='' || PORT="port ${PORT}"
  if [ "${HOST}" = '__None__' ]
  then
      HOST=''
  else
      if [ -z "${PORT}" -a -z "${PROTO}" ]
      then
          HOST="host ${HOST}"
      else
          HOST="and host ${HOST}"
      fi
  fi
  [ "${OTHER}" = '__None__' ] && OTHER=''

  cd ${g_task_dir}
	report_info '30' "start tcpdump ${PROTO} -vv ${NET} ${COUNT} ${PORT} ${HOST} ${OTHER} -w tcpdump.cap"
	sleep 1
	tcpdump ${PROTO} -vv ${NET} ${COUNT} ${PORT} ${HOST} ${OTHER} -w tcpdump.cap 2>${g_stderr}
	[ $? -ne 0 ] && report_err '90' "tcpdump failed: $(tail -1 ${g_stderr})"

  chmod 777 ${g_task_dir}/*
  report_info "100" "${g_task_dir}/tcpdump.cap"
}

main
exit 0

