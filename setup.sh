#!/usr/bin/env bash
## 2022 - RackunSec
## This script installs dependencies used by Summon.py
##
##
gitinstall=1 ## by default we will install this
pipinstall=1 ## By default we will install this
printf "\n[i] Welcome to Summon! (2022 @RackunSec)\n"
if [ $EUID -ne 0 ]
then
    printf "[!] Please run this script as root. You are EUID: ${EUID}\n"
    exit 1
else
    if [[ $(which pip|wc -l) == "1" ]]
    then
        printf "[i] Python PIP already installed.\n"
        pipinstall=0
    fi
    if [[ $(which git|wc -l) == "1" ]]
    then
        printf "[i] Git already installed.\n"
        gitinstall=0
    fi
    printf "[i] This script installs the following dependencies used by Summon:\n"
    if [[ $pipinstall -eq 1 ]]
    then
        printf "  -- python3-pip\n"
    fi
    if [[ $gitinstall -eq 1 ]]
    then
        printf "  -- git\n\n"
    fi
    printf "  -- Python3 pip modules\n\n"
    printf "[?] Shall I continue? [y/n] "
    read ans
    if [[ "$ans" == "y" ]]
    then
        if [ $gitinstall -eq 1 ] || [ $pipinstall -eq 1 ]
        then
            apt update
            if [[ "$gitinstall" -eq 1 ]]
            then
                apt install git -y
            fi
            if [[ "$pipinstall" -eq 1 ]]
            then
                apt install python3-pip -y
            fi

        fi
        python3 -m pip install --upgrade pip
        python3 -m pip install -r requirements.txt

        mkdir -p /etc/demon/apps_repo
        cp files/apps_repo/demon_apps.json /etc/demon/apps_repo
        cp files/apps_repo/demon_apps.json /etc/demon/apps_repo/demon_apps_backup.json ## Make a backup

        printf "\n[i] All done! Now run 'python3 summon.py'\n"
    else
        printf "[i] Thanks for choosing Summon. Maybe another time? \n"
        exit 1
    fi
fi
# Test comment A
