#!/bin/bash

#pings
sudo ping -c4 8.8.8.8 > /dev/null
GGL=$? ### Google

sudo ping -c4 wikipedia.org > /dev/null
WKP=$? ### Wikipedia

sudo ping -c4 heise.de > /dev/null
HSD=$? ### Heise

sudo ping -c4 192.168.178.1 > /dev/null
FZB=$? ### Fritz!Box

PING=$((($GGL+$WKP+$HSD+$FZB)/4))
#PING=1 ### for testing


# Dates
DATE=$(date +"%Y-%m-%d")
DATETIME=$(date +"%Y-%m-%d_%H%M")

# Temp Connection Status
STATUS=$(<.connection_off.temp)

if [ $PING != 0 ]; then
  if [ $STATUS <= 60 ]; then
    echo $DATETIME "; No network connection, restarting wlan0; Ping = " $PING >> log/$DATE.log
	echo $DATETIME "; restarting wlan0; Ping = " $PING "; Attempt = " $STATUS >> log/ERROR.log
    sudo /sbin/ifdown 'wlan0'
    sleep 5
    echo 1 > .connection_off.temp
    sudo /sbin/ifup --force 'wlan0'
  else
    echo $DATETIME "; No network connection, rebooting RPi2; Ping = " $PING  >> log/$DATE.log
	echo $DATETIME "; rebooting RPi2; Ping = " $PING "; Attempt = " $STATUS >> log/ERROR.log
    echo 0 > .connection_off.temp
	sudo reboot
  fi
  echo $(($STATUS+1)) > .connection_off.temp
else
  if [ $STATUS != 0 ]; then
      echo $DATETIME "; Back online; PING = " $PING >> log/$DATE.log
      echo $DATETIME "; Back online; PING = " $PING "; Attempt = " $STATUS >> log/ERROR.log
    else
      echo $DATETIME "; Everything's fine here; Ping = " $PING  >> log/$DATE.log
  fi
    echo 0 > .connection_off.temp
fi
