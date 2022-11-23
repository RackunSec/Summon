# Summon - King of the Crossroads
<img src="https://github.com/RackunSec/Summon/raw/main/files/images/icons/summon.png" width="300" />

Summon is a tool that will turn a stock Debian installation into a [Demon Linux distribution](https://demonlinux.com). In the olde days, I was distributing ISO files that were ~3GB in size. To avoid bandwidth issues and make the process of updates a lot easier for me and other users of Demon Linux, I have created an installer script - Summon.

## Installation
To install Demon Linux ontop of a fresh installation of Debian follow these steps:
 1. Download and install a Debian amd64 using [the Netinstall ISO](https://www.demonlinux.com/download/iso/debian-11.5.0-amd64-netinst.iso).
    1. During installation, create a non-root user and only install the base system (Summon will handle the UI stuff)
    2. Remember to provide non root user with `sudo` access.
 2. Install git: `apt install git sudo -y` and clone this repository: `cd /opt && git clone https://github.com/RackunSec/Summon.git`
 3. Run the setup script with: `chmod +x setup.sh && ./setup.sh`
 4. Finally, Summon a Demon: `python3 summon.py install demon -u (NON_ROOT_USERNAME)`
 5. Reboot
 
[![Installation and Demo Video](https://img.youtube.com/vi/CspmyGp7LbA/default.jpg)](https://youtu.be/CspmyGp7LbA)

## Contributing
If your application requires an install module, just let me know or you can build it yourself by following the [Summon - Creating-Install-Modules Wiki](https://github.com/RackunSec/Summon/wiki/Creating-Install-Modules).

## Help
For more information, please check the [Summon Wiki](https://github.com/RackunSec/Summon/wiki)!

~Douglas

