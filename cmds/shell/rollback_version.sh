#!/bin/bash
source $(dirname $0)/common_function.sh

function main()
{
    init
    if [ $(whoami) != 'root' ]
    then
        echo "Please switch root !"
        report_err "20" "Please switch root !"
    fi
    if [ ! -d "/home/upgradeinstall/backup" ]
    then
        echo "Not upgrade yet, can't rollback !"
        report_err "25" "Not upgrade yet, can't rollback !"
    fi
    if [ ! -d "/home/ubp/upgradeinstall/upgrade" ]
    then
        echo "/home/ubp/upgradeinstall/upgrade don't exist, can't rollback !"
        report_err "25" "/home/ubp/upgradeinstall/upgrade don't exist, can't rollback !"
    fi
    cd /home/ubp/upgradeinstall/upgrade
    source upgrade_utils.sh
    upgrade_chattr_rm_i
    cd /home/ubp/upgradeinstall/upgrade/
    restore /home/upgradeinstall/backup ./backup_files_60.conf
    restore /home/upgradeinstall/backup ./backup_web_60.conf
    restore /home/upgradeinstall/backup eapp_upgrade/eapp_backup_files.conf
    ldconfig
    service eappmysql restart
    su - ubp -c "/opt/ubp_websvc/webrestart.sh"
    su - ubp -c ". /opt/UBP/svc_profile.sh; ubp_adm -cmd start"

    report_info "100" "NULL"
}

main 

