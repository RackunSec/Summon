#!/usr/bin/env python3
## Summon - DEMON LINUX Build Tool
##  This is the future of Demon Linux.
## Python Class: Files - Do File Stuff
##
## Files:
import os
import requests
from classes.Style import Style
from zipfile import ZipFile ## Unzipping files!
from rich.status import Status


#import shutil ## blow away an entire directory tree
import re

class Files:
    def __init__(self):
        self.demon_download_uri = "https://demonlinux.com/download/packages/4.X/"
        self.style = Style()

    ## Make a directory if it does not exist:
    def check_path_mkdir(self,path):
        if not os.path.exists(path):
            os.mkdir(path)
        return

    def download_base_files(self):
        download_files = [
            {"uri":self.demon_download_uri+"demon.zip","path":"/usr/share/demon.zip","zip":True},
            {"uri":self.demon_download_uri+"ubuntu-font.zip","path":"/usr/share/fonts/truetype/ubuntu-font.zip","zip":True},
            {"uri":self.demon_download_uri+"emojione-android.ttf","path":"/usr/share/fonts/truetype/emojione-android.ttf","zip":False}
        ]
        ## TODO Check if these were already completed or not:
        for file in download_files:
            file_name = re.sub(r'.*\/([^/]+)$',r'\1',file['uri'])
            #print(f"{self.style.sub}{self.style.CMNT}Downloading file: {self.style.RST}{self.style.PPUR}{file_name}{self.style.RST}")
            if not os.path.exists(file['path']):
                self.download_file(file['uri'],file['path'],False) ## Download Demon.zip
                if file['zip']: ## This is a zipped archive:
                    self.unzip_file(file_name,file['path']) ## Extract it
            else:
                print(f"{self.style.sub}{self.style.CMNT}File already exists: {file['path']}")


    def build_redteam(self):
        with Status(f"{self.style.sub}{self.style.CMNT}Building {self.style.RST}{self.style.RED}/redteam{self.style.CMNT} and {self.style.RST}{self.style.RED}~/Pentest{self.style.CMNT} directory trees{self.style.RST}") as status:
            directories = ["/redteam","/redteam/windows-domains","/redteam/web",
                "/redteam/osint","/redteam/passwords","/redteam/exploit","/redteam/wifi",
                "/redteam/rackunsec","/redteam/wordlists","/redteam/printers","/redteam/enumeration",
                "/redteam/web/GraphQL","/redteam/rackunsec/web/","/redteam/rackunsec/windows-domains/",
                "/redteam/rackunsec/wordlists/","/redteam/rackunsec/osint/",
                "/root/Pentest","/root/Pentest/web","/root/Pentest/scans",
                "/root/Pentest/files","/root/Pentest/users","/redteam/payloads/",
                "/redteam/apple","/redteam/cloud","/etc/demon","/redteam/evasion","/redteam/c2" ]
            ## Make a bunch of directories:
            for dir in directories:
                if not os.path.isdir(dir):
                    self.check_path_mkdir(dir)
        return

    ## Unzip a File:
    def unzip_file(self,file,path):
        if os.path.exists(path):
            with Status(f"Unzipping file: {self.style.GRN}{file}{self.style.RST}") as status:
                current_dir = os.getcwd() ## store to return
                path = re.sub(r'/[^/]+$','',path) ## overwrite the path
                os.chdir(path)
                with ZipFile(file, 'r') as zipObj:
                    zipObj.extractall()
                os.chdir(current_dir)
        return ## Done.

    ## Download a file to disk:
    def download_file(self,uri,path,clobber):
        #print(f"{self.style.info} Downloading: {uri}")
        if not clobber:
            if not os.path.exists(path):
                response = requests.get(uri)
                open(path, "wb").write(response.content)
            else:
                print(f"{self.style.sub}{self.style.CMNT}{path} already downloaded.{self.style.RST}")
                return
        else:
            with Status(f"Downloading files ... ") as status:
                response = requests.get(uri)
                open(path, "wb").write(response.content)
                #if os.path.exists(path):
                    #print(f"{self.style.sub}{self.style.CMNT}{path} Downloaded successfully.{self.style.RST}")
                #else:
                    #print(f"{self.fail} Something went wrong while trying to download file - {uri}")
            return
