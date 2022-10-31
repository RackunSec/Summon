#!/usr/bin/env python3
## Summon - DEMON LINUX Build Tool
##  This is the future of Demon Linux.
## Python Class: Python - Do Python Stuff
##
## Python app stuff:
from classes.Style import Style
from classes.Shell import Shell
import subprocess ## Running Apps
import os

class Python:
    def __init__(self):
        self.style=Style()
        self.shell=Shell()
        self.current_dir=os.getcwd()

    ## Installing apps via PIP:
    def pip_install(self,app):
        from rich.status import Status
        with Status(f"{self.style.CMNT}Python-pip Install:{self.style.RST} {self.style.GRN}{app}{self.style.RST}") as status:
            subprocess.run(
                ["python3","-m","pip","install",app],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
                )
        return

    ## Uninstall a PIP app:
    def pip_uninstall(self,app):
        from rich.status import Status
        with Status(f"{self.style.CMNT}Python-pip Uninstall (Yes to all):{self.style.RST} {self.style.GRN}{app}{self.style.RST}") as status:
            subprocess.run(
                ["python3","-m","pip","uninstall",app,"-y"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        return

    ## Poetry Install:
    def poetry_install(self,path,app):
        #from rich.status import Status
        #with Status(f"{self.style.CMNT}Installing {app} with Poetry{self.style.RST}") as status:
        print(f"{self.style.sub}{self.style.CMNT}Installing {app} with Poetry{self.style.RST}")
        os.chdir(path)
        #print(f"{self.style.info} Current path: {os.getcwd()}")
        self.shell.run_cmd(["poetry","install"])
        #print(f"{self.style.info} Heading back to {self.current_dir}") ## DEBUG
        os.chdir(self.current_dir)
        return

    ## Pip install --upgrade
    def pip_install_upgrade(self,app):
        from rich.status import Status
        with Status(f"{self.style.CMNT}Python-pip Upgrade: {self.style.RST}{self.style.GRN}{app}{self.style.RST}") as status:
            subprocess.run(
                ["python3","-m","pip","install","--upgrade",app],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
                )
        return

    ## Python3 -m pip install -r requirements:
    def pip_reqs(self,app,path):
        from rich.status import Status
        with Status(f"{self.style.CMNT}Installing requirements for {self.style.RST}{self.style.GRN}{app}{self.style.RST}") as status:
            current_dir = os.getcwd()
            os.chdir(path) ## change directory
            try:
                subprocess.run(
                    ["python3","-m","pip","install","-r","requirements.txt"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                    )
            except Exception as e:
                print(f"{self.style.fail} Something went wrong while installing requirements for {app}: {self.style.RED}{e}{self.style.RST}")
            os.chdir(current_dir) ## go back
        return

    ## Pip install .
    def pip_install_dot(self,path):
        from rich.status import Status
        with Status(f"{self.style.CMNT}Pip install . {self.style.RST}") as status:
            current_dir = os.getcwd()
            os.chdir(path)
            subprocess.run(
                ["python3","-m","pip","install","."],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
                )
            os.chdir(current_dir)
        return ## Done
