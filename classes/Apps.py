#!/usr/bin/env python3
## Summon - DEMON LINUX Build Tool
##  This is the future of Demon Linux.
## Python Class: Apps - Do Application Stuff
##
## I built this to Do easy add-ons later:
from classes.Style import Style
from classes.Python import Python
from classes.Shell import Shell
from classes.Files import Files
import subprocess ## Running Apps
from git import Repo ## for git
import re ## for regexps
import os ## for OS stuff
import requests ## HTTP requests
from sys import exit
import json ## read the config.json file.
import importlib ## importing from string names (install_modules/{name}.py)
from rich.status import Status

class Apps:
    def __init__(self):
        self.initial_apps = [ ## Tshark taken out due to non compliant installation.
            "vim","ftp","open-vm*","curl","git","xfce4","tilix","python3-pip","python3",
            "gedit","dbus-x11","nmap","unzip","papirus-icon-theme","python3-venv","ssh",
            "proxychains4","freerdp2-x11","lightdm-settings","lightdm","slick-greeter","xfce4-goodies",
            "libpcap-dev","wget","libssl-dev","tcpdump","firefox-esr","unzip","sudo","smbclient",
            "imagemagick","ghostscript","gnome-themes-extra","gnome-themes-extra-data","simplescreenrecorder",
            "libcurl4-openssl-dev","libssl-dev","rubygems", "ruby", "ruby-dev", "jq", "mariadb-client", "dirb",
            "whois", "sslsplit", "dnsrecon", "sipsak", "braa", "onesixtyone", "sipvicious","make","gcc",
            "build-essential", "fontconfig", "fonts-powerline"
            ]
        self.rackgit = "https://github.com/RackunSec/"
        self.demonrepo = "https://demonlinux.com/download/packages/4.X/"
        self.install_modules_dir="files/install_modules/" 
        self.install_modules_classes="files.install_modules." 
        self.style=Style()
        self.python=Python()
        self.shell=Shell()
        self.files=Files()
        self.current_dir=os.getcwd()
        self.demon_app_repo="/etc/demon/apps_repo/demon_apps.json"

    ## Ruby Gem Install stuff:
    def ruby_gem_install(self,gems):
        from rich.status import Status
        for gem in gems:
            with Status(f"{self.style.sub}Installing Gem: {self.style.RST}{self.style.GRN}{gem}{self.style.RST} ... ") as status:
                subprocess.run( ## do some clean up!
                    ["gem","install",gem],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

    ## Installing apps via APT:
    def apt_install(self,apps_args):
        with Status(f"{self.style.CMNT}Apt Install ({len(apps_args)} Apps) {self.style.RST}") as status:
            apps_args.insert(0,"apt")
            apps_args.insert(1,"install")
            apps_args.insert(2,"-y")
            apps_args.insert(3,"--assume-yes")
            subprocess.run( ## Uncomment the DEVNULL lines to debug
                apps_args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL) ## Install stuff
        #print(f"{self.style.sub}{self.style.CMNT}Installation of apps completed.{self.style.RST}")
        return ## done

    ## Remove application with apt:
    def apt_remove(self,apps_args):
        with Status(f"{self.style.CMNT}Apt Remove ({len(apps_args)} Apps) {self.style.RST}") as status:
            apps_args.insert(0,"apt")
            apps_args.insert(1,"remove")
            apps_args.insert(2,"-y")
            apps_args.insert(3,"--assume-yes")
            subprocess.run( ## Uncomment the DEVNULL lines to debug
                apps_args,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL) ## Install stuff
        #print(f"{self.style.sub}{self.style.CMNT}Installation of apps completed.{self.style.RST}")
        return ## done

    ## Check if an app repo branch is behind:
    def git_behind(self,path,app):
        if os.path.isdir(path):
            os.chdir(path)
            ## Check if .git folder here:
            if os.path.isdir(".git"):
                self.shell.run_cmd(["git","remote","update"]) ## update refs with remote
                output = self.shell.run_cmd(["git","status","uno"])## Check if behind
                if re.search("Your branch is behind",output):
                    print(f"{self.style.info}{self.style.CMNT} Remote Git Repository updates available for {self.style.RED}{app}{self.style.RST}\n")
            else:
                print("[!] Apps.git_behind() requires a path to a local git Repository.")

    ## Installing apps via APT:
    def dpkg_install(self,deb_file):
        with Status(f"{self.style.CMNT}Dpkg Install: {self.style.RST}{self.style.PPUR}{deb_file}{self.style.RST}") as status:
            subprocess.run( ## install the package!
                ["dpkg","-i",deb_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL) ## Install stuff
            subprocess.run( ## do some clean up!
                ["apt","-f","install","-y"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    ## Apt Update:
    def apt_update(self):
        with Status(f"Updating local Debian package repository ... ") as status:
            subprocess.run(
                ["apt","update"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL) ## Install stuff
    ## Apt-Key Add:
    def apt_key_add(self,key_uri):
        ## Generate a file name for /tmp:
        ## https://debian.neo4j.com/neotechnology.gpg.key
        ## https://download.sublimetext.com/sublimehq-pub.gpg
        if re.match(r'.*\.key$',key_uri):
            key_file = "/tmp/"+re.sub(r'.*/([^/]+\.gpg\.key)$',r'\1',key_uri)
        else:
            key_file = "/tmp/"+re.sub(r'.*/([^/]+\.gpg)$',r'\1',key_uri)
        ##print(f"KEY FILE: {key_file}") ## DEBUG
        response = requests.get(key_uri)
        open(key_file, "wb").write(response.content)
        print(f"{self.style.sub}Adding APT key file: {self.style.PPUR}/tmp/neotechnology.gpg.key{self.style.RST}")
        subprocess.run(
            ["apt-key","add",key_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL) ## Install stuff

    ## APT Add Repo:
    def apt_add_repo(self,repo,path):
        if not os.path.exists(path):
            with open(path,"w") as file:
                file.write(repo)
        else: ## The file already exists:
            in_file = False ## Let's assume the repo is not yet there:
            with open(path,"r") as file:
                lines = file.readlines()
                for line in lines:
                    if re.search(repo,line):
                        in_file = True
            if not in_file: ## put it in there:
                with open(path,"w") as file:
                    file.write(repo)

    ## Git Pull:
    def git_pull(self,path):
        from rich.status import Status
        #os.chdir(path)
        try:
            repo = Repo(path)
            o = repo.remotes.origin
            o.pull
            print(f"{self.style.sub}{self.style.CMNT}Repo updated.{self.style.RST}")
            return True
        except Exception as e:
            return False


    ## Git clone: (regexps are currently broken)
    def git_clone(self,uri,path,repo_dir):
        from rich.status import Status
        repo = re.sub(r'.*\/(.+)\/(.+)\.git$',r'\1/\2',uri)
        app = re.sub(r'^[^/]+/',r'',repo)
        if repo_dir is not None:
            path = path+repo_dir ## We will be cloning here instead.
        else:
            path = path + app
        try:
            if os.path.isdir(path):
                ## Path exists. Check for the presence of a .git directory:
                if not os.path.isdir(path+"/.git"):
                    self.shell.run_cmd(["rm","-rf",path]) ## Destroy it.
                else:
                    try: ## Try to update the repo:
                        with Status(f"{self.style.CMNT}Path exists for {app}. Updating repository ... {self.style.RST}") as status:
                            repo = Repo(path)
                            o = repo.remotes.origin
                            o.pull()
                            print(f"{self.style.sub}{self.style.CMNT}Repo updated.{self.style.RST}")
                        return False
                    except Exception as e:
                        ## local changes will require removal of repo:
                        if e.stderr:
                            if "local changes to the following files" in e.stderr:
                                print(f"{self.style.fail} It looks like you have changes within the repo: {path}")
                                repo_ans = input(f"{self.style.ques}{self.style.YLL} Would you like my to remove this repo and start clean? (y/n) {self.style.RST}")
                                if repo_ans == "y":
                                    ## destroy directory
                                    print(f"{self.style.sub}Destroying directory {path}")
                                    self.shell.run_cmd(["rm","-rf",path])
                                    print(f"{self.style.sub}{self.style.CMNT}Cloning {self.style.RST}{self.style.GRN}{app.strip()}{self.style.CMNT} into {self.style.RST}{self.style.GRN}{path}{self.style.RST}")
                                    Repo.clone_from(uri, path)
                                    return True
                                else:
                                    return False
                        else:
                            print(f"{self.style.fail} Failed to update repository.")
                            return False
            with Status(f"{self.style.CMNT}Cloning {self.style.RST}{self.style.GRN}{repo}{self.style.CMNT} into {self.style.RST}{self.style.GRN}{path}{self.style.RST}") as status:
                Repo.clone_from(uri, path)
                return True
        except Exception as e:
            print(f"{self.style.fail} Failed to clone {repo}: {e}")
        return

    ## Install all Redteam Apps:
    def redteam_apps(self,all,force):
        ## Read the JSON file:
        app_count = 0
        app_fail_count = 0
        app_currently_installed_count = 0
        if os.path.isfile(self.demon_app_repo):
            with open(self.demon_app_repo, "r") as config:
                config_json = json.load(config)
                for category in config_json['apps_list']:
                    for app in config_json['apps_list'][category]:
                        ## Do they want to install all?:
                        if not all:
                            if config_json['apps_list'][category][app]['add']=="False":
                                continue
                        self.style.prnt_install(config_json['apps_list'][category][app]['name'],category)
                        if config_json['apps_list'][category][app]['installed']=="True":
                            if not force:
                                print(f"{self.style.sub}{self.style.CMNT}Application {self.style.RST}{self.style.GREEN}{config_json['apps_list'][category][app]['name']}{self.style.CMNT} already installed.{self.style.RST}")
                                print(f"{self.style.sub}{self.style.CMNT}Use {self.style.RED}--force{self.style.CMNT} to force installation.{self.style.RST}")
                                #config_json['apps_list'][category][app]['add']="False" # 
                                continue
                            else:
                                print(f"{self.style.sub}{self.style.RED}Forcing application installation.")
                        print(f"{self.style.sub}{self.style.CMNT}Additional Info: {config_json['apps_list'][category][app]['project_uri']}{self.style.RST}")
                        
                            ## install it
                        if self.install_redteam_app(app,force,False): # Will return True or False
                            ## Update demon_apps.json and set the value to "True" for "installed":
                            config_json['apps_list'][category][app]['installed']="True" # set to True
                            config_json['apps_list'][category][app]['add']="False" # set to True
                        else:
                            app_fail_count = app_fail_count + 1
                            continue
                        app_count = app_count + 1
            with open(self.demon_app_repo,"w") as update_json: ## The "indent=(n)" option here keeps the file linted/formatted/pretty nicely.
                update_json.write(json.dumps(config_json,indent=2)) ## write the new values.
            ## Now we re-read the file and print how many applications are now installed:
            with open(self.demon_app_repo,"r") as config:
                config_json = json.load(config)
                for category in config_json['apps_list']:
                    for app in config_json['apps_list'][category]:               
                        if config_json['apps_list'][category][app]['installed']=="True":
                            app_currently_installed_count = app_currently_installed_count + 1
            print(f"\n{self.style.info} {app_count} Applications installed/updated during this session.")
            print(f"{self.style.info} {app_fail_count} Applications failed to install.")
            print(f"{self.style.info} {app_currently_installed_count} Applications currently installed.")
        else:
            print(f"{self.style.fail} Could not read {self.demon_app_repo} file.")
            exit()

    ## Marke the application as "Installed":
    def update_repo_app_installed(self,app):
        with open(self.demon_app_repo, "r") as config:
            config_json = json.load(config)
            for category in config_json['apps_list']:
                for repo_app in config_json['apps_list'][category]:
                    if repo_app == app:
                        config_json['apps_list'][category][app]['installed']="True" # set to True
                        config_json['apps_list'][category][app]['add']="False" # set to True
        with open(self.demon_app_repo,"w") as update_json: ## The "indent=(n)" option here keeps the file linted/formatted/pretty nicely.
            update_json.write(json.dumps(config_json,indent=2)) ## write the new values.

    ## Install a single application using ./files/install_modules files:
    def install_redteam_app(self,app,force,single):
        module_name = self.install_modules_classes+app
        if single:
            ## Check application installation status in Repo:
            if os.path.isfile(self.demon_app_repo):
                with open(self.demon_app_repo, "r") as config:
                    config_json = json.load(config)
                    for category in config_json['apps_list']:
                        for repo_app in config_json['apps_list'][category]:
                            if repo_app == app:
                                app_module_name = importlib.import_module(module_name)
                                app_module = app_module_name.Application(force)
                                ## Print that you are actually gonna do something:        
                                self.style.prnt_install(config_json['apps_list'][category][repo_app]['name'],category)
                                if not force:
                                    if app_module.check_install(): ## Already installed.
                                        print(f"{self.style.sub}{self.style.CMNT}Application {self.style.RST}{self.style.GREEN}{app}{self.style.CMNT} already installed.{self.style.RST}")
                                        print(f"{self.style.sub}{self.style.CMNT}Use {self.style.RED}--force{self.style.CMNT} to force installation.{self.style.RST}")
                                        ## We need to check whether or this status is updated in the local repo:
                                        if config_json['apps_list'][category][repo_app]['installed'] != "True":
                                            self.update_repo_app_installed(app) ## update the repo file in /etc/demon
                                        return True
                                    if config_json['apps_list'][category][repo_app]['installed'] == "True" and not force:
                                        print(f"{self.style.sub}{self.style.CMNT}Application {self.style.RST}{self.style.GREEN}{app}{self.style.CMNT} already installed.{self.style.RST}")
                                        print(f"{self.style.sub}{self.style.CMNT}Use {self.style.RED}--force{self.style.CMNT} to force installation.{self.style.RST}")
                                        return True
                                    ## OK, so now it will flow through to below if not installed:
        if os.path.exists(self.install_modules_dir+app+".py"):
            ## install it
            app_module_name = importlib.import_module(module_name)
            app_module = app_module_name.Application(force)
            ## Check the installation status first:
            if not force:
                if app_module.check_install(): ## Already installed.
                    print(f"{self.style.sub}{self.style.CMNT}Application {self.style.RST}{self.style.GREEN}{app}{self.style.CMNT} already installed.{self.style.RST}")
                    print(f"{self.style.sub}{self.style.CMNT}Use {self.style.RED}--force{self.style.CMNT} to force installation.{self.style.RST}")
                    self.update_repo_app_installed(app) ## update the repo file in /etc/demon
                    return True
            app_module.install()
            if app_module.check_install():
                print(f"{self.style.install_success}")
                ## Installation was successful.
                ## If this was a single application from the CLI, we need to update the Repo:
                if single:
                    self.update_repo_app_installed(app) ## update the repo file in /etc/demon
                return True
            else:
                print(f"{self.style.install_fail}")
                return False
        else:
            print(f"{self.style.sub}{self.style.RED}No module named {app}.py found in {self.install_modules_dir}{self.style.RST}")
            return False

