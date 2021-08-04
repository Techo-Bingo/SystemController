#!/bin/bash
cd $(dirname $0)
DOWNLOAD_DIR="__DOWNLOAD__"
mkdir ${DOWNLOAD_DIR} 2>/dev/null

function main()
{
    cp -f /home/ubp/logs/tracecollection/*.csv ${DOWNLOAD_DIR}
    cd ${DOWNLOAD_DIR}
    for file in *.csv
    do
      local new_name="$(echo $file|awk -F. '{print $1}'|sed 's/_info//').csv"
      mv -f $file $new_name
    done
    chmod 777 ${DOWNLOAD_DIR} ${DOWNLOAD_DIR}/*.csv
}

main
exit 0

