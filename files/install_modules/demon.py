#!/usr/bin/env python3
## 2022 - Demon Linux 4.X - Douglas Berdeaux
## Summon Installation module for: (APP NAME)
## Module written by: @RackunSec
## -- Remember to add the application to demon_self.apps.json and enable it
##      by setting the value of "add" to "True"
##

## Import all classes required for the module here:
from classes.Apps import Apps
from classes.Shell import Shell
from classes.Python import Python
from classes.Style import Style
from classes.Files import Files
from classes.Repo import Repo
import os
import stat
from sys import exit

class Application():
    def __init__(self,user):
        ## Instantiate Objects:
        self.apps = Apps() ## instanticate the object
        self.shell = Shell()
        self.python = Python()
        self.files = Files()
        self.style = Style()
        self.repo=Repo()
        
        self.user = user ## We are forcing an installation 
        ## Common place to download stuff from:
        self.demon_repo = "https://demonlinux.com/download/packages/4.X/"
        ## Update this to point to the "installed" binary of this app
        ## This can often be in your $PATH (try `which (CMD` to locate it)
        ## Or sometimes, it's just the local GitHub repository:
        self.install_path_check ="/etc/demon" ## This file will exist when the application is properly installed.
        self.badpaths=[] ## if a previous installation is there, destroy it.
        
    def install(self):
        ## install the application:
        print(f"{self.style.sing}{self.style.BOLD} {self.style.PINK}Summoning the {self.style.CMNT}{self.style.RED}DEMON{self.style.PINK} ... {self.style.RST}")
        self.python.pip_install_upgrade("pip") ## upgrade this now.
        self.python.pip_install_upgrade("pycurl") ## upgrade this and compile correctly.
        self.python.pip_install("poetry") ## Poetry is used often for running within virtual envs.
        ## Install Demon Linux Theme, Firefox plugins, etc:
        self.files.download_file("https://demonlinux.com/download/packages/4.X/root.tgz","/root/root.tgz",False) ## download settings
        os.chdir("/root/") ## go home
        self.shell.run_cmd(["tar","vzxf","root.tgz"])
        
        ## Install dependencies:
        self.apps.apt_update() ## update this first
        self.apps.apt_install(self.apps.initial_apps) ## Install huge base system

        ## Install NanoDesu Window Manager (title bars) Theme:
        self.files.download_file("https://demonlinux.com/download/packages/4.X/nanodesu.zip","/usr/share/themes/nanodesu.zip",True)
        if not os.path.isdir("/usr/share/themes/nanodesu"):
            os.chdir("/usr/share/themes/") ## Go here.
            self.shell.run_cmd(["unzip","-o","nanodesu.zip"])

        ## Install all Powerline fonts for root self.user and specified self.user:
        self.files.check_path_mkdir("/usr/share/fonts/truetype/powerline-all") ## make the directory.
        self.apps.git_clone("https://github.com/powerline/fonts.git","/usr/share/fonts/truetype/","powerline-all") ## Clone here.
        self.files.download_file("https://demonlinux.com/download/packages/4.X/powerline.tgz","/tmp/powerline.tgz",True)
        os.chdir("/tmp")
        self.shell.run_cmd(["tar","vzxf","powerline.tgz"])
        self.shell.run_cmd(["cp","-R","fonts","/root/.local/share/"]) ## copy it into the root home.
        os.chdir(self.apps.current_dir) ## go back

        ## If a self.user was specified, let's give them access:
        if self.user is not None:
            self.files.check_path_mkdir(f"/home/{self.user}/.local")
            self.files.check_path_mkdir(f"/home/{self.user}/.local/share")
            self.shell.run_cmd(["cp","-R","/root/.local/share/fonts",f"/home/{self.user}/.local/share/"]) ## make a copy for the self.user too!
            os.rename("/root/root.tgz",f"/home/{self.user}/root.tgz") ## put her there!
            os.chdir(f"/home/{self.user}/") ## go there to extrapolate it
            self.shell.run_cmd(["tar","vzxf","root.tgz"]) ## Extrapolate it
            ## now install the right Bashrc file:
            self.files.download_file("https://demonlinux.com/download/packages/4.X/bashrc.txt",f"/home/{self.user}/.bashrc",True)
            self.shell.run_cmd(["sed","-i",f"s/demon/{self.user}/g",f"/home/{self.user}/.bashrc"]) ## Incase they don't choose "demon"      
            os.unlink(f"/home/{self.user}/root.tgz") ## zap it from disk
            os.chdir(self.apps.current_dir) ## go back to Summon home
            ## Install Dracula VIM theme:
            self.files.check_path_mkdir(f"/home/{self.user}/.vim")
            self.files.check_path_mkdir(f"/home/{self.user}/.vim/pack")
            self.files.check_path_mkdir(f"/home/{self.user}/.vim/pack/themes")
            self.files.check_path_mkdir(f"/home/{self.user}/.vim/pack/themes/start")
            self.apps.git_clone("https://github.com/dracula/vim.git",f"/home/{self.user}/.vim/pack/themes/start/","dracula")
            self.files.download_file("https://demonlinux.com/download/packages/4.X/vimrc.txt",f"/home/{self.user}/.vimrc",True)
            self.shell.run_cmd(["chown","-R",f"{self.user}:{self.user}",f"/home/{self.user}"]) ## TODO look up a Python way to do this!
            ## Install Dracula Gedit theme: -- This is set in the root.tgz file.
            self.files.check_path_mkdir(f"/home/{self.user}/.local/")
            self.files.check_path_mkdir(f"/home/{self.user}/.local/share")
            self.files.check_path_mkdir(f"/home/{self.user}/.local/share/gedit")
            self.files.check_path_mkdir(f"/home/{self.user}/.local/share/gedit/styles")
            self.files.download_file("https://raw.githubusercontent.com/dracula/gedit/master/dracula.xml",f"/home/{self.user}/.local/share/gedit/styles/dracula.xml",True)
            
            ## Install Dracula Grub Theme:
            self.files.check_path_mkdir("/boot/grub/themes") ## Make this directory
            ## download the grub.zip file into /boot/grub/themes/
            self.files.download_file(self.demon_repo+"grub.zip","/boot/grub/themes/grub.zip",True)
            os.chdir("/boot/grub/themes")
            self.shell.run_cmd(["unzip","-o","grub.zip"])
            ## download grub.txt and overwrite /etc/default/grub:
            self.files.download_file(self.demon_repo+"grub.txt","/etc/default/grub",True)
            ## update Grub:
            self.shell.run_cmd(["grub-mkconfig","-o","/boot/grub/grub.cfg"])
            self.shell.run_cmd(["update-grub"])
            self.repo.update_autostart_script(self.user)

        else:
            os.unlink("/root/root.tgz") ## delete it
        os.chdir(self.apps.current_dir) ## go back
        self.repo.update_autostart_script("root") ## Do this for root user too.

        self.files.build_redteam() ## Build the /redteam tree
        self.files.download_base_files() ## Download the base files

        ## Install Dracula VIM theme for root:
        self.files.check_path_mkdir(f"/root/.vim")
        self.files.check_path_mkdir(f"/root/.vim/pack")
        self.files.check_path_mkdir(f"/root/.vim/pack/themes")
        self.files.check_path_mkdir(f"/root/.vim/pack/themes/start")
        self.apps.git_clone("https://github.com/dracula/vim.git",f"/root/.vim/pack/themes/start/","dracula")
        self.files.download_file("https://demonlinux.com/download/packages/4.X/vimrc.txt",f"/root/.vimrc",True)

        ## Install the Dracula GTK theme: -- This is set in the root.tgz file.
        self.files.download_file("https://github.com/dracula/gtk/archive/master.zip","/usr/share/themes/master.zip",True)
        if os.path.exists("/usr/share/themes/master.zip"):
            os.chdir("/usr/share/themes/")
            self.shell.run_cmd(["unzip","-o","master.zip"])
            os.chdir(self.apps.current_dir) ## Go basck to Summon home.
        else:
            print(f"{self.style.fail} Something went wrong while downloading GTK theme.")
            exit(1337)

        ## Install Dracula Gedit theme: -- This is set in the root.tgz file.
        self.files.check_path_mkdir("/root/.local/")
        self.files.check_path_mkdir("/root/.local/share")
        self.files.check_path_mkdir("/root/.local/share/gedit")
        self.files.check_path_mkdir("/root/.local/share/gedit/styles")
        self.files.download_file("https://raw.githubusercontent.com/dracula/gedit/master/dracula.xml","/root/.local/share/gedit/styles/dracula.xml",True)

        ## Install Dracula Theme Icons:
        self.files.download_file("https://github.com/dracula/gtk/files/5214870/Dracula.zip","/usr/share/icons/Dracula.zip",True)
        if os.path.exists("/usr/share/icons/Dracula.zip"):
            os.chdir("/usr/share/icons")
            self.shell.run_cmd(["unzip","-o","Dracula.zip"])
        else:
            print(f"{self.style.fail} Something went wrong when trying to download icon theme.")
            exit(1337)

        ## Install Demon Linux theme for login window:
        self.files.download_file("https://demonlinux.com/download/packages/4.X/slick-greeter.conf","/etc/lightdm/slick-greeter.conf",True)
        self.python.pip_install("pipx") ## PIPX is nice. It puts the apps into ~/.local/bin and virtualizes/contains them
        self.python.pip_install("poetry") ## Poetry is for Python apps
        self.shell.run_cmd(["pipx","ensurepath"]) ## Ensure that PIPX-installed apps are accessible to the Demon

        ## Install Golang
        if not os.path.exists("/usr/local/go/bin/go"):
            self.style.prnt_install("Golang","development")
            self.files.download_file("https://demonlinux.com/download/packages/4.X/go1.19.2.linux-amd64.tar.gz","/tmp/go1.19.2.linux-amd64.tar.gz",False)
            os.chdir("/tmp/")
            self.shell.run_cmd(["tar","-C","/usr/local","-vzxf","go1.19.2.linux-amd64.tar.gz"])
            ## .bashrc from root.tgz already has this set up.
            os.chdir(self.apps.current_dir) ## go back home.
        ## Ubuntu Font:
        self.style.prnt_install("Fonts","misc")
        self.shell.run_cmd(["fc-cache","-f"])
 
        print(f"\n{self.style.info} All done! Simply reboot to take effect!\n\n")

        return

    def check_install(self):
    ## Check if application is actually installed:
        if os.path.exists(self.install_path_check): ## replace this, obviously.
            return True
        else:
            return False
