# Summon - King of the Crossroads
<img src="https://github.com/RackunSec/Summon/raw/main/files/images/icons/summon.png" width="300" />

Summon is a tool that will turn a stock Debian installation into a [Demon Linux distribution](https://demonlinux.com). In the olde days, I was distributing ISO files that were ~3GB in size. To avoid bandwidth issues and make the process of updates a lot easier for me and other users of Demon Linux. I have created an installer script - Summon.

## Installation
To install Demon Linux ontop of a fresh installation of Debian follow these steps:
 1. Download and install a Debian amd64 using [the Netinstall ISO](https://www.demonlinux.com/download/iso/debian-11.5.0-amd64-netinst.iso).
    1. During installation, create a non-root user and only install the base system (Summon will handle the UI stuff)
 2. Install git: `apt install git -y` and clone this repository: `cd /opt && git clone https://github.com/RackunSec/Summon.git`
 3. Run the setup script with: `chmod +x setup.sh && ./setup.sh`
 4. Finally, Summon a Demon: `python3 summon.py install demon -u (NON_ROOT_USERNAME)`
 5. Reboot
 
 ## Adding Tools
 To list tools:
 ```bash
 sudo python3 summon.py list-apps
 ```
 To list app info:
 ```bash
 sudo python3 summon.py app-info (APP_NAME)
 ```
 To install an application (single):
 ```bash
 sudo python3 summon.py install (APP_SHORT_NAME) # e.g.: eaphammer
 ```
 To install all applications:
 ```bash
 sudo python3 summon.py install all
 ```
 To select and choose apps to install you will have to update the repository in `/etc/demon/demon_apps.json` and set `add="True"` for each one. Then simply run:
 ```bash
 sudo python3 summon.py install add
 ```
 To use force (if an installation fails for any reason) use `--force` with any of the install commands listed above.
 
 ## Updates and Upgrades
 All updates and upgrades will be handled by Summon. When you log into XFCE4, Summon will automatically check for updates and provide a notification if any are found. If updates are available, the Summon XCFE4 Panel icon will also change and show a green dot. To update, simply type:
 ```bash
 sudo python3 summon.py upgrade
 ```

