#!/bin/bash
cd $(dirname $0)
DOWNLOAD_DIR="__DOWNLOAD__"
mkdir ${DOWNLOAD_DIR} 2>/dev/null

function main()
{
    cp -f example/*.csv ${DOWNLOAD_DIR}
	chmod 777 ${DOWNLOAD_DIR} ${DOWNLOAD_DIR}/*.csv
}

main
exit 0

