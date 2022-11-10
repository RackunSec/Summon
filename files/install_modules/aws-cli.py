#!/usr/bin/env python3
## 2022 - Demon Linux 4.X - Douglas Berdeaux
## Summon Installation module for: AWS_CLI_V2
## Module written by: @RackunSec
## -- Remember to add the application to demon_apps.json and enable it
##      by setting the value of "add" to "True"
## There are only 3 areas to update in this file.
## Edit everything between the ## vvv  ## ^^^ lines.

## Import all classes required for the module here:
from classes.Apps import Apps
from classes.Shell import Shell
from classes.Python import Python
from classes.Style import Style
from classes.Files import Files
import stat ## for chmod
import os ## for exit, and path
## The Application() Class:
class Application():
    def __init__(self,force):
        ## Instantiate Objects:
        self.apps = Apps() ## instanticate the object
        self.shell = Shell()
        self.python = Python()
        self.files = Files()
        self.style = Style()
        self.force = force ## We are forcing an installation 
        ## Common place to download stuff from:
        self.demon_repo = "https://demonlinux.com/download/packages/4.X/"
        ## Update this to point to the "installed" binary of this app
        ## This can often be in your $PATH (try `which (CMD` to locate it)
        ## Or sometimes, it's just the local GitHub repository:

        ##vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        self.install_path_check ="/usr/local/bin/aws" ## This file will exist when the application is properly installed.
        self.badpaths=["/usr/local/aws-cli","/usr/local/bin/aws","/usr/local/bin/aws_completer","/usr/local/aws-cli/"] ## Destroy local repo (/redteam/(CATEGORY)/repo) and binary in $PATH.
        ##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def install(self):
        ## Pre-install checks:
        ## Pre-install checks:
        if self.force: ## we are destroying all old artifacts:
            self.uninstall()
        ## Installation instructions go here:
        ##vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        self.files.download_file(self.demon_repo+"awscliv2.zip","/redteam/cloud/awscliv2.zip",True)
        os.chdir("/redteam/cloud/")
        self.files.unzip_file("awscliv2.zip","/redteam/cloud/")
        os.chdir("/redteam/cloud/aws")
        self.shell.run_cmd(["chmod","+x","install"])
        self.shell.run_cmd(["./install","--update"])
        os.unlink("/redteam/cloud/awscliv2.zip")
        self.shell.run_cmd(["chmod","a+x","/usr/local/aws-cli/v2/current/dist/aws"]) ## Make it executable? 

        ##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        ## Done. Do not edit below.
        return True

    def check_install(self):
    ## Check if application is actually installed:
        if os.path.exists(self.install_path_check): ## replace this, obviously.
            return True
        else:
            return False

    ## Uninstall:
    def uninstall(self):
        ## If the application is installed via pip, run self.python.pip_uninstall(app) to get rid of it.
        ## If not, you can be left with a broken installation.
        ##vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # self.python.pip_uninstall("app_name")
        ## If application installed with dpkg, use Apps().apt_remove(["app_name"]):
        # self.apps.apt_remove(["app_name"])
        ##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        if len(self.badpaths)>0:
            for path in self.badpaths:
                if os.path.exists(path):
                    print(f"{self.style.sub}{self.style.CMNT}Removing old installation: {path}{self.style.RST}")
                    self.shell.run_cmd(["rm","-rf",path]) ## remove what was there from apt or pip
        if os.path.exists(self.install_path_check):
            self.shell.run_cmd(["rm","-rf",self.install_path_check])
        return




