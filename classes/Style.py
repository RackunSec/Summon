#!/usr/bin/env python3
## Summon - DEMON LINUX Build Tool
##  This is the future of Demon Linux.
## Python Class: Style - Style the app with color.
##
## This is just terminal colors using sty
from sty import fg ## colors
from sys import exit ## exit on issue
class Style:
    def __init__(self):
        self.BLK='\033[1m'+fg(233) # Black Text
        self.RED=fg(197)    ## pretty red
        self.YLL=fg(226)    ## pretty yellow
        self.GRN=fg(199)    ## nice green color
        self.GREEN=fg(82)
        self.RST='\033[0m'  ## reset the color to terminal default
        self.PPIN=fg(171)   ## purplish-pink
        self.PPUR=fg(135)   ## nice purple
        self.PINK=fg(201)   ## pink color
        self.BLUE=fg(39)
        self.BOLD="\033[1m"   ## Bold Text
        self.ORAN=fg(208)
        self.DRED=fg(124) ## Deep Red
        self.LRED=fg(160) ## Light Red
        self.CMNT=f"{fg(7)}\033[3m" ## Comments / grey text
        self.warn=f" {self.PPUR}[{self.YLL}*{self.PPUR}]{self.RST}"
        self.info=f" {self.RED}➙{self.RST}"
        self.ques=f" {self.PPUR}[{self.YLL}?{self.PPUR}]{self.RST}"
        self.fail=f" {self.PPUR}[{self.RED}!{self.PPUR}]{self.RST}"
        self.sing=f" 🔥"
        self.sub=f"{self.PPIN} └─{self.PPUR}[{self.RST}"
        self.subpipe=f"  {self.PPIN}   {self.PPUR}⎢{self.RST}"
        self.subpipebot=f"  {self.PPIN}   {self.PPUR}⎣{self.RST}"
        self.subapplist=f"{self.PPIN}└───{self.PPUR}⎡{self.RST}" #  
        self.subapp=f"\n{self.PPUR}[{self.RST}"
        self.install_success=f"  {self.PPUR} └─{self.PPUR}[{self.GREEN}Installation Successful{self.RST}"
        self.install_fail=f"  {self.PPUR} └─{self.PPUR}[{self.RED} !! Installation Failed !! {self.RST}"
        self.CYAN=fg(38)
    def prnt_install(self,app,category):
        print(f" {self.subapp}{self.ORAN}{self.BOLD}Installing{self.RST} {self.PPIN}─ {self.PPUR}{self.CYAN}{app} {self.PPUR}({category}){self.RST}{self.RST}{self.PPIN} ─ {self.PPUR}]{self.RST}")
        return
    ## Display a Text Banner at each run:
    def banner_text(self):
        print(f"""
      {self.PPIN}██████  █    ██  ███▄ ▄███{self.PINK}▓{self.PPIN} ███▄ ▄███▓ ▒█████   ███▄    █
    {self.PINK}▒{self.PPIN}██    {self.PINK}▒{self.PPIN}  ██  {self.PINK}▓{self.PPIN}██{self.PINK}▒▓{self.PPIN}██▒▀█▀ ██▒▓██▒▀█▀ ██{self.PINK}▒▒{self.PPIN}██{self.PINK}▒{self.PPIN}  ██▒ ██ ▀█   █
    {self.PINK}░ ▓{self.PPIN}██▄   ▓██  {self.PINK}▒{self.PPIN}██{self.PINK}░▓{self.PPIN}██    ▓██{self.PINK}░▓{self.PPIN}██    ▓██{self.PINK}░▒{self.PPIN}██{self.PINK}░{self.PPIN}  ██▒▓██  ▀█ ██{self.PINK}▒{self.PPIN}
      {self.PINK}▒{self.PPIN}   ██▒▓▓█  {self.PINK}░{self.PPIN}██{self.PINK}░▒{self.PPIN}██    ▒██{self.PINK} ▒{self.PPIN}██    ▒██{self.PINK} ▒{self.PPIN}██   ██░▓██{self.PINK}▒{self.PPIN}   ██{self.PINK}▒{self.PPIN}
    {self.PINK}▒{self.PPIN}██████▒▒▒▒█████{self.PINK}▓ ▒{self.PPIN}██{self.PINK}▒{self.PPIN}   ░██{self.PINK}▒▒{self.PPIN}██▒   ░██▒░ ████▓▒░▒██{self.PINK}░{self.PPIN}   ▓██{self.PINK}░{self.PPIN}
    {self.PINK}▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ░ ▒░   ░  ░░ ▒░   ░  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒
    ░ ░▒  ░ ░░░▒░ ░ ░ ░  ░      ░░  ░      ░  ░ ▒ ▒░ ░ ░░   ░ ▒░
    ░  ░  ░   ░░░ ░ ░ ░      ░   ░      ░   ░ ░ ░ ▒     ░   ░ ░
          ░     ░            ░          ░       ░ ░           ░

           {self.RED}{self.BOLD}Demon Linux{self.RST}{self.BOLD} Summoner - 2022 {self.PPUR}@RackunSec{self.RST} 😈
    """)

    ## Define the apps usage:
    def usage(self):
      print(f" 🔥 {self.ORAN}{self.BOLD}Usage:{self.RST}\n      python3 summon.py {self.PPIN}(Arguments){self.RST}\n")
      print(f" 🔥 {self.ORAN}{self.BOLD}Arguments:{self.RST}")
      print(f"      {self.PPIN}install{self.CMNT} - Install Demon and applications{self.RST}")
      print(f"      {self.PPIN}list-apps{self.CMNT} - List all Redteam apps in local repository{self.RST}")
      print(f"      {self.PPIN}app-info (App Name){self.CMNT} - Get application info from local repository{self.RST}")
      print(f"      {self.PPIN}version{self.CMNT} - Version your Demon repository{self.RST}")
      print(f"      {self.PPIN}upgrade{self.CMNT} - Upgrade your Demon app repository{self.RST}")
      print(f"      {self.PPIN}restore-repo{self.CMNT} - Restores a broken repository from backup{self.RST}\n")
      exit(1337) ## Exit with code

    ## Show some installation examples:
    def install_examples(self):
      print(f"{self.fail} Nothing to install!")
      print(f"\n 🔥 {self.ORAN}{self.BOLD}Install Examples:{self.RST}")
      print(f"      {self.PPIN}install {self.PINK}demon{self.CMNT} - Install Demon UI{self.RST}")
      print(f"      {self.PPIN}install {self.PINK}demon -u (Username){self.CMNT} - Install Demon UI for non-root user{self.RST}\n")
      print(f"      {self.PPIN}install {self.PINK}add{self.CMNT} - Install all applications with \"add\" set to \"True\"{self.RST}")
      print(f"      {self.PPIN}install {self.PINK}add --force{self.CMNT} - Same as above but using force{self.RST}\n")
      print(f"      {self.PPIN}install {self.PINK}all{self.CMNT} - Install all applications from repository{self.RST}")
      print(f"      {self.PPIN}install {self.PINK}all --force{self.CMNT} - Same as above but using force{self.RST}\n")
      print(f"      {self.PPIN}install {self.PINK}(Application){self.CMNT} - Install single application{self.RST}")
      print(f"      {self.PPIN}install {self.PINK}(Application) --force{self.CMNT} - Same as above but using force\n{self.RST}")
      return