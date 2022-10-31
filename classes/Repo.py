#!/usr/bin/env python3
## Summon - DEMON LINUX Build Tool
##  This is the future of Demon Linux.
## Repository Class: Apps - Do Application Stuff
##
## I built this to Do easy add-ons later:
from classes.Style import Style ## Styling the terminal output
from classes.Shell import Shell ## Running commands.
from classes.Apps import Apps ## Application Stuff.
import os ## for OS stuff
from sys import exit
import json ## read the config.json file.
import subprocess ## Run command and save output to variable.

class Repo():
    def __init__(self) -> None:
        self.repo_file = "/etc/demon/apps_repo/demon_apps.json"
        self.current_ver_uri="https://raw.githubusercontent.com/RackunSec/Summon/main/version.txt"
        self.style = Style()

    ## Show all applications
    ##  calls display_app_info() for each application defined in the JSON file:
    def list_apps(self,filter_category):
        ## read the JSON file and list apps with info:
        if not os.path.exists(self.repo_file):
            print(f"{self.style.fail} Could not read repository file: {self.repo_file}. Exiting.")
            exit(1337)

        with open(self.repo_file, "r") as config:
            repo_json = json.load(config)
            app_count = 0
            install_count = 0
            for category in repo_json['apps_list']:
                if filter_category is not None:
                    if category != filter_category:
                        continue ## we don't need this one
                print(f"🔥 {self.style.ORAN}{self.style.BOLD}{category}{self.style.RST} 🔥")
                for app in repo_json['apps_list'][category]:
                    app_count=app_count+1
                    self.display_app_info(repo_json,category,app)
                    if repo_json['apps_list'][category][app]['installed']=="True":
                        install_count=install_count+1
            print(f"{app_count} applications total, {install_count} installed")
            
        return

    ## Filter the demon_apps.json file for a single application:
    def single_app_info(self,app):
        ## report info on a specific application:
        with open(self.repo_file, "r") as config:
            repo_json = json.load(config)
            for category in repo_json['apps_list']:
                for repo_app in repo_json['apps_list'][category]:
                    if repo_app == app:
                        self.display_app_info(repo_json,category,app)

        return

    ## Display application info to scree:
    def display_app_info(self,repo_json,category,app):
        print(f"  {self.style.PPUR}┌{self.style.PINK}{repo_json['apps_list'][category][app]['name']}:{self.style.RST} ",end="")
        if repo_json['apps_list'][category][app]['installed']=="True":
            print(f"({self.style.CMNT}{self.style.GREEN}Installed{self.style.RST})")
        else:
            print(f"({self.style.CMNT}Not Installed{self.style.RST})")
        if repo_json['apps_list'][category][app]['comment'] == "":
            comment = "None"
        else:
            comment = repo_json['apps_list'][category][app]['comment']
        print(f"  {self.style.subapplist}{self.style.PPUR}About: {self.style.CMNT}{repo_json['apps_list'][category][app]['about']}{self.style.RST}")
        print(f" {self.style.subpipe}{self.style.PPUR}Summon Version: {self.style.CMNT}{repo_json['apps_list'][category][app]['demon_version']}{self.style.RST}")
        print(f" {self.style.subpipe}{self.style.PPUR}Project URI: {self.style.CMNT}{repo_json['apps_list'][category][app]['project_uri']}{self.style.RST}")
        print(f" {self.style.subpipe}{self.style.PPUR}Author: {self.style.CMNT}{repo_json['apps_list'][category][app]['author']}{self.style.RST}")
        print(f" {self.style.subpipe}{self.style.PPUR}Comment: {self.style.CMNT}{comment}{self.style.RST}")
        print(f" {self.style.subpipe}{self.style.PPUR}Install Path: {self.style.CMNT}{repo_json['apps_list'][category][app]['install_path']}{self.style.RST}")
        print(f" {self.style.subpipebot}{self.style.PPUR}How to Install: {self.style.CMNT}{self.style.PINK}python3 summon.py install {app}{self.style.RST}\n")

        return

    ## Update the Summon repository in /etc/demon/:
    def upgrade_summon(self):
        ## Update the repository
        apps=Apps()
        shell=Shell()
        self.style.prnt_install("Upgrade","Base")
        if apps.git_pull("/opt/demon/"):
            installed_apps = []
            with open(self.repo_file, "r") as config: ## get a list of currently installed apps:
                repo_json = json.load(config)
                local_version = repo_json['repo_version']
                for category in repo_json['apps_list']:
                    for repo_app in repo_json['apps_list'][category]:
                        if repo_json['apps_list'][category][repo_app]['installed']=="True":
                            installed_apps.append(repo_app)
            shell.run_cmd(["rm","-rf","/etc/demon/apps_repo/*"]) ## Remove the old repository
            shell.run_cmd(["cp","/opt/demon/files/apps_repo/demon_apps.json","/etc/demon/apps_repo/"])
            self.reset_new_repo(installed_apps) ## Write the new repo install status
            print(f"{self.style.sing} {self.style.CMNT}Summon updated successfully to {self.style.GREEN}{local_version}{self.style.RST}.")
            return

        else:
            print(f"{self.style.fail} Could not update the Repository.")
        return

    ## Reset New Repo:
    def reset_new_repo(self,apps):
        with open(self.repo_file, "r") as config: ## get a list of currently installed apps:
            repo_json = json.load(config)
            local_version = repo_json['repo_version']
            for category in repo_json['apps_list']:
                for repo_app in repo_json['apps_list'][category]:
                    if repo_app in apps: ## It was previously installed, set it to "True":
                        repo_json['apps_list'][category][repo_app]['installed']="True"
        with open(self.repo_file,"w") as update_json: ## The "indent=(n)" option here keeps the file linted/formatted/pretty nicely.
            update_json.write(json.dumps(repo_json,indent=2)) ## write the new values.

    ## Check for updates:
    def update_check(self):
        style=Style()
        shell=Shell()
        import requests ## for HTTP request
        if os.path.exists(self.repo_file): ## We need a version first
            ## read the version fromthe repo file using json:
            with open(self.repo_file, "r") as config:
                repo_json = json.load(config)
                local_version = repo_json['repo_version']
            if local_version != "":
                response = requests.get(self.current_ver_uri)
                current_version = response.text.strip()
            print(f"{style.info} Local version: {local_version}")
            print(f"{style.info} Current version: {current_version}")
            if local_version == current_version:
                print(f"{style.info} Up to date.")
                return
            else:
                print(f"{style.info} An update is ready for you!")
                #shell.run_cmd(["notify-send","Summon","'Summon Updates Available'","--icon=software-update-urgent"])
                shell.run_cmd(["notify-send","Summon",f"Summon Updates Available ({current_version})","--icon=/usr/share/demon/images/icons/summon.png"])
                ## Check if using XCFE4 Panel Icon:
                home_dir = os.path.expanduser("~")
                #print(f"{style.info} Home directory: {home_dir}")
                xfce4_panel_icon_file = subprocess.run(["egrep","-iElr","summon",f"{home_dir}/.config/xfce4/panel/"], stdout=subprocess.PIPE)
                if xfce4_panel_icon_file!="":
                    xfce4_panel_icon_file=str(xfce4_panel_icon_file.stdout.decode()).strip()
                    #print(f"{style.info} Found XFCE4 Panel icon location: {xfce4_panel_icon_file}")
                    shell.run_cmd(["sed","-i","s/summon.png/summon-update.png/",xfce4_panel_icon_file]) ## change the icon
        else:
            print(f"{style.fail} Could not read version file: {self.local_ver_file}")
        return
