#!/usr/bin/env python3
## Summon - DEMON LINUX Build Tool
##  This is the future of Demon Linux.
##  To Build:
##      1. Install the latest version of Debian using the Net ISO into a VMDK or on disk
##          a. Do not install x11, just a quick base installation
##      2. Install couple things: apt install git python3-pip
##          a. python3 -m pip install --upgrade pip
##      3. Clone this repository into /opt/redteam
##      4. Run this tool: python3 dlb-tool.py install
##      5. startx
##
## 2022 (c) GNU - @RackunSec
##
import subprocess
import sys ## For exit() and Arguments
import os
## Summon Classes:
from classes.Style import Style ## Stylish
from classes.Apps import Apps ## Application stuff
from classes.Shell import Shell ## run_cmd()
from classes.Files import Files ## File stuff
from classes.Repo import Repo ## Local and remote repo stuff
import importlib

## The main() function of the application:
def main(): ## This is mainly for handling input and sending tasks off to be done.
    style = Style() ## for colors
    shell = Shell() ## Check internet connectivity (required)
    ## Check if root (required, `sudo` is OK)
    if len(sys.argv)==1: ## I got no arguments!
        style.banner_text()
        style.usage()
    elif len(sys.argv)>1:
        style.banner_text()
        print(f"{style.info} {style.CMNT}Checking internet connectivity{style.RST}",end="")
        if shell.check_internet():
            print(f"{style.GREEN} ✔{style.RST}\n")
        else:
            print(f"{style.RED} ✖{style.RST}")
            sys.exit(1337)
        ## CHeck the repo for remote changes/sync:
        check_repo()
        ## Check if /redteam exists:
        files=Files()
        files.build_redteam() ## if not there, build it.
        
        ## Check existence of conf file:
        if os.path.isdir("/etc/demon"):
            repo=Repo()
            repo.check_config_file()

        ## Capture Force from arguments if there:
        if "--force" in sys.argv:
            force=True
            print(f"{style.info} Installing using force.")
        else:
            force=False
        ## What does the user mean to do?
        if sys.argv[1] == "install":
            get_uid("install")
            if len(sys.argv)>2:
                if sys.argv[2]=="demon":
                    print(f"{style.sing}{style.BOLD} {style.PINK}Heading to the {style.RED}Crossroads{style.PINK} ... {style.RST}")
                    if "-u" in sys.argv: ## Adding support for a user now:
                        user = sys.argv[4]
                        print(f"{style.info}{style.BOLD} Adding User support for {style.GRN}{user}{style.RST}")
                        ## Check if user exists before continuing:
                        if not os.path.isdir(f"/home/{user}/"):
                            print(f"{style.fail} Could not determine user {user}'s home directory. Does this user exist?")
                            sys.exit()
                    else:
                        user = None
                    app_module = importlib.import_module("files.install_modules.demon")
                    application = app_module.Application(user)
                    application.install() ## Build it!
                elif sys.argv[2]=="add":
                    redteam_apps(False,force) ## Go install what you need. all==False
                elif sys.argv[2]=="all":
                    redteam_apps(True,force) ## Go install what you need. 
                else: ## This could be an application:
                    if len(sys.argv)>=3:
                        install_app(sys.argv[2],force)
            else:
                style.install_examples() ## Show some examples - 

        elif sys.argv[1]=="list-apps":
            if len(sys.argv)>2: ## Was a category provided?
                list_apps(sys.argv[2])
            else:
                list_apps(None)
        elif sys.argv[1]=="app-info" and len(sys.argv)>2: ## Get information on a single application
            app_info(sys.argv[2])
        ## Secret functions:
        elif sys.argv[1]=="version": ## Show version
            demon_version()
        elif sys.argv[1]=="update-check": ## check for updates (Repo())
            repo=Repo()
            repo.update_check()
        elif sys.argv[1]=="upgrade":
            upgrade_summon()
        elif sys.argv[1]=="restore-repo":
            repo=Repo()
            repo.restore_repo() ## Restore the repository
        else:
            style.usage() ## I dunno

## Upgrade Summon:
def upgrade_summon():
    get_uid("upgrade")
    repo = Repo()
    repo.upgrade_summon()
    return


## Check if user is root or not:
def get_uid(function):
    style=Style()
    if os.getuid() != 0:
        print(f"{style.fail} {function} must be ran as root.")
        sys.exit(1337)

def check_repo():
    apps = Apps()
    apps.git_behind(os.getcwd(),"Summon")

## Show Demon repo Version
def demon_version():
    repo=Repo()
    repo.update_check()
    return

## Install Red Team apps listed in redteam.json using files within ./install_modules/
def redteam_apps(all,force):
    style=Style() ## for styling text
    apps=Apps() ## for application-specific stuff
    print(f"{style.sing} {style.BOLD}{style.PINK}Summoning the {style.CMNT}{style.RED}DEMON{style.PINK} for Apps ... {style.RST}")
    print(f"{style.sing} {style.BOLD}{style.PINK}Heading to the {style.RED}Crossroads{style.PINK} ... {style.RST}")
    apps.redteam_apps(all,force) ## Install everything set to "True"
    print(f"{style.RST}")

## List applications from redteam.json and their info:
def list_apps(filter_category):
    repo = Repo()
    repo.list_apps(filter_category) ## list them out.

## Get application info for single application:
def app_info(app):
    repo = Repo()
    repo.single_app_info(app)
    
## Install a single application:
def install_app(app,force):
    apps = Apps()
    apps.install_redteam_app(app,force,True)

if __name__ == "__main__":
    main()
    print("")
