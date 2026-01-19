# HomeLab: wake-up-computer

Script dedicated as a way to power on a computer thru Wake-On-LAN, which would allow me to then remotely interact with those devices using Tailscale from anywhere outside my home internet.

The script currently makes use of the python library [wakeonlan](https://pypi.org/project/wakeonlan/) to wake up these devices, and performs checks to ensure whether the device powered on successfully.
