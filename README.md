# HomeLab: wake-up-computer

Script dedicated as a way to power on a computer thru Wake-On-LAN, which would allow me to then remotely interact with those devices using Tailscale from anywhere outside my home internet.

The script currently makes use of the python library [wakeonlan](https://pypi.org/project/wakeonlan/) to wake up these devices, and performs checks to ensure whether the device powered on successfully.

![](https://i.imgur.com/7mEckJM.gif)

## Required Environment Variables:

```
# IP_TYPE: 'tailscale'/'local' based on type of device connection desired
# LOCAL_IP: Dedicated local home network IP address
# TS_IP: Dedicated Tailscale IP address
# MAC: Physical MAC address of a device

IP_TYPE=

MSI_LOCAL_IP= 
MSI_TS_IP=
MSI_MAC=

PI_LOCAL_IP=
PI_TS_IP=
PI_MAC=
  
TANK_LOCAL_IP=
TANK_TS_IP=
TANK_MAC=

TP_LOCAL_IP=
TP_TS_IP=
TP_MAC=

# logger.py
# LOG_STATE: 'debug' or 'info'
LOG_STATE=
```

## Future Implementations

* Implement automatic tailscale/local IP decisions based on whether the current device is connected to the home network or not.