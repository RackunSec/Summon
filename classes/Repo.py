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
from configparser import ConfigParser ## for reading the config file in /etc/demon

class Repo():
    def __init__(self) -> None:
        self.repo_file = "/etc/demon/apps_repo/demon_apps.json"
        self.current_ver_uri="https://raw.githubusercontent.com/RackunSec/Summon/main/version.txt"
        self.style = Style()
        self.cwd=os.getcwd() ## Were are we running from
        self.config_path="/etc/demon/summon.conf"
        self.check_config_file() ## need this.
        self.summon_path=self.get_install_path()

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
                    if repo_json['apps_list'][category][app]['installed']=="True":
                        install_count=install_count+1
                    app_count=app_count+1
                    self.display_app_info(repo_json,category,app)
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
        print(f"  {self.style.PPUR}┌{self.style.PPUR}[{self.style.YLL}{repo_json['apps_list'][category][app]['name']}{self.style.PPUR}]{self.style.RST}: ",end="")
        apps=Apps()
        if repo_json['apps_list'][category][app]['installed']=="True":
            print(f"({self.style.CMNT}{self.style.GREEN}Installed{self.style.RST})")
        else:
            print(f"({self.style.CMNT}Not Installed{self.style.RST})")
        if repo_json['apps_list'][category][app]['comment'] == "":
            comment = "None"
        else:
            comment = repo_json['apps_list'][category][app]['comment']
        print(f"  {self.style.subapplist}{self.style.PPIN}About{self.style.PPUR}: {self.style.CMNT}{repo_json['apps_list'][category][app]['about']}{self.style.RST}")
        print(f" {self.style.subpipe}{self.style.PPIN}Summon Version{self.style.PPUR}: {self.style.CMNT}{repo_json['apps_list'][category][app]['demon_version']}{self.style.RST}")
        print(f" {self.style.subpipe}{self.style.PPIN}Project URI{self.style.PPUR}: {self.style.CMNT}{repo_json['apps_list'][category][app]['project_uri']}{self.style.RST}")
        print(f" {self.style.subpipe}{self.style.PPIN}Author{self.style.PPUR}: {self.style.CMNT}{repo_json['apps_list'][category][app]['author']}{self.style.RST}")
        print(f" {self.style.subpipe}{self.style.PPIN}Comment{self.style.PPUR}: {self.style.CMNT}{comment}{self.style.RST}")
        print(f" {self.style.subpipe}{self.style.PPIN}Install Path{self.style.PPUR}: {self.style.CMNT}{repo_json['apps_list'][category][app]['install_path']}{self.style.RST}")
        print(f" {self.style.subpipebot}{self.style.PPIN}How to Install{self.style.PPUR}: {self.style.CMNT}{self.style.PINK}sudo python3 summon.py install {app}{self.style.RST}\n")
        if repo_json['apps_list'][category][app]['remote_location']=="github" and repo_json['apps_list'][category][app]['local_repo_path']!="" and repo_json['apps_list'][category][app]['installed']=="True":
            apps.git_behind(repo_json['apps_list'][category][app]['local_repo_path'],repo_json['apps_list'][category][app]['name']) ## check for update
        return

    ## Update the Summon repository in /etc/demon/:
    def upgrade_summon(self):
        ## Update the repository
        if self.update_check():
            apps=Apps()
            shell=Shell()
            self.style.prnt_install("Upgrade","Base")
            if apps.git_pull(self.summon_path):
                installed_apps = []
                with open(self.repo_file, "r") as config: ## get a list of currently installed apps:
                    repo_json = json.load(config)
                    local_version = repo_json['repo_version']
                    for category in repo_json['apps_list']:
                        for repo_app in repo_json['apps_list'][category]:
                            if repo_json['apps_list'][category][repo_app]['installed']=="True":
                                installed_apps.append(repo_app)
                shell.run_cmd(["rm","-rf","/etc/demon/apps_repo/*"]) ## Remove the old repository
                shell.run_cmd(["cp",self.summon_path+"/files/apps_repo/demon_apps.json","/etc/demon/apps_repo/"])
                self.reset_new_repo(installed_apps) ## Write the new repo install status
                with open(self.repo_file, "r") as config: ## get a list of currently installed apps:
                    repo_json = json.load(config)
                    local_version = repo_json['repo_version']
                sudo_user=os.getlogin() ## User ran SUDO:
                home_dir = os.path.expanduser(f"/home/{sudo_user}/")
                xfce4_panel_icon_file = subprocess.run(["egrep","-iElr","summon",f"{home_dir}/.config/xfce4/panel/"], stdout=subprocess.PIPE)
                if xfce4_panel_icon_file!="":
                    xfce4_panel_icon_file=str(xfce4_panel_icon_file.stdout.decode()).strip()
                    shell.run_cmd(["sed","-i","s/summon-update.png/summon.png/",xfce4_panel_icon_file]) ## change the icon
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
        shell=Shell()
        apps=Apps()
        #self.check_config_file() ## Check the config file
        ## This gets called upon each login into EXCF4, so this makes the most sense for this code to be here:
        xfce4_panel_icon_file = self.get_summon_icon_file() ## Just get the file name
        if xfce4_panel_icon_file!="":
            shell=Shell()
            import re
            with open(xfce4_panel_icon_file,"r") as icon_file:
                lines = icon_file.readlines()
            for index,line in enumerate(lines):
                if re.search("^Exec",line):
                    lines[index]=line.replace("/opt/demon",self.summon_path) ## Overwrite it.
            with open(xfce4_panel_icon_file,"w") as icon_file: ## overwrite it:
                icon_file.writelines(lines)

        self.update_autostart_script(os.getlogin()) ## update this file too.

        import requests ## for HTTP request

        if os.path.exists(self.repo_file): ## We need a version first
            ## read the version fromthe repo file using json:
            with open(self.repo_file, "r") as config:
                repo_json = json.load(config)
                local_version = repo_json['repo_version']
            if local_version != "":
                response = requests.get(self.current_ver_uri)
                current_version = response.text.strip()
            print(f"{self.style.info} Local version: {local_version}")
            print(f"{self.style.info} Current version: {current_version}")
            if local_version == current_version:
                print(f"{self.style.info} Up to date.")
                xfce4_panel_icon_file = self.get_summon_icon_file() ## Just get the file name
                if xfce4_panel_icon_file!="":
                    xfce4_panel_icon_file=xfce4_panel_icon_file
                    shell.run_cmd(["sed","-i","s/summon-update.png/summon.png/",xfce4_panel_icon_file]) ## change the icon
                return False
            else:
                print(f"{self.style.info} An update is ready for you!")
                shell.run_cmd(["notify-send","Summon",f"Summon Updates Available ({current_version})","--icon=/usr/share/demon/images/icons/summon.png"])
                xfce4_panel_icon_file = self.get_summon_icon_file() ## Just get the file name
                if xfce4_panel_icon_file!="":
                    xfce4_panel_icon_file=xfce4_panel_icon_file
                    shell.run_cmd(["sed","-i","s/summon.png/summon-update.png/",xfce4_panel_icon_file]) ## change the icon
                return True
        else:
            print(f"{self.style.fail} Could not read version file: {self.local_ver_file}")
        return

    ## Get the install pathfr om the config file:
    def get_install_path(self):
        if os.path.exists(self.config_path):
            config=ConfigParser() ## Lets read the Summon install path
            config.read(self.config_path)
            summon_path=config['SUMMON']['summon_path']
            return str(summon_path)
        else:
            print(f"{self.style.fail} Could not read {self.config_path}")
            exit()

    ## Ensure the health/existence of the config file:
    def check_config_file(self):
        if not os.path.exists("/etc/demon/summon.conf"):
            ans=input(f"{self.style.ques} We are running from {self.style.RED}{self.cwd}{self.style.RST} Would you like to make this your Summon binary path [y/n]? ")
            if ans=="y":
                config=ConfigParser()
                config['SUMMON']= {"summon_path":self.cwd}
            with open("/etc/demon/summon.conf","w") as config_file:
                config.write(config_file)

    def update_autostart_script(self,user):
        home_dir=f"/home/{user}/.config/autostart/"
        script=str(subprocess.run(["egrep","-iElr","opt.demon",home_dir],stdout=subprocess.PIPE).stdout.decode().strip())
        import re
        if script != "":
            with open(script,"r") as script_file:
                script_lines=script_file.readlines()
            for index,line in enumerate(script_lines):
                if re.search(r'^Exec',line):
                    script_lines[index]=line.replace("/opt/demon",self.summon_path)
            #print(script_lines)
            with open(script,"w") as script_file: ## overwrite it
                script_file.writelines(script_lines)

    def get_summon_icon_file(self):
        home_dir = os.path.expanduser("~")
        return str(subprocess.run(["egrep","-iElr","summon",f"{home_dir}/.config/xfce4/panel/"], stdout=subprocess.PIPE).stdout.decode().strip())


    ## Restore from the backup in case something tragic happens:
    def restore_repo(self):
        shell=Shell()
        print(f"{self.style.info} Restoring repository from backup ... ")
        if os.path.exists("files/apps_repo/demon_apps.json"):
            shell.run_cmd(["cp","files/apps_repo/demon_apps.json","/etc/demon/apps_repo/demon_apps.json"])
            self.update_check()
        else:
            print(f"{self.style.fail} Could not open local repo file for reading: files/apps_repo/demon_apps.json !")
            exit()
