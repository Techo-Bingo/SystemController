#!/bin/bash
source $(dirname $0)/common_function.sh

IP=$1
ATTR_INFO=$2

function parser_param()
{
	UPLOAD_FILE=$(echo ${ATTR_INFO}|awk -F"|" '{print $1}')
	DEST_DIR=$(echo ${ATTR_INFO}|awk -F"|" '{print $2}')
	CHMOD=$(echo ${ATTR_INFO}|awk -F"|" '{print $3}')
	CHOWN=$(echo ${ATTR_INFO}|awk -F"|" '{print $4}')
	# report_info '70' 'server perpare OK'
}

function move_to()
{
	if [ ! -f ${UPLOAD_FILE} ]
	then
		echo "${UPLOAD_FILE} not exist !"
		echo "${UPLOAD_FILE} not exist !" >/home/Bingo/aaa.log
	fi
	mv -f ${UPLOAD_FILE} ${DEST_DIR} 
	chmod ${CHMOD} ${DEST_DIR}/$(basename ${UPLOAD_FILE})
	chown ${CHOWN} ${DEST_DIR}/$(basename ${UPLOAD_FILE})
	echo "upload $(basename ${UPLOAD_FILE}) to ${DEST_DIR} success"
}

function main()
{
    init
    parser_param
    move_to
}

main 
