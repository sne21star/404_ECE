#!/bin/sh

# restore.sh
#
# by Avi Kak (kak@purdue.edu)

##  The following three shell scripts:
##
##      start_monitoring.sh        
##
##      inject_arp.sh
##
##      restore.sh                    (this file)
##
##
##  are meant to be used only if your version of Ubuntu is
##  older than 13.10.  If your version of Ubuntu is more
##  recent than that, you need to use the shell script
##  
##      StartMonitorModeInterface.sh
##
##  Read the Lecture 9 notes on how to use this script.

# Execute this script after you have finished the attack to
# restore your wireless settings to what they need to be for
# normal operation.

# Note that yy:yy:yy:yy:yy:yy is the normal MAC address of your
# wlan0 wireless interface.

airmon-ng stop mon0
sleep 5
ifconfig wlan0 down
sleep 5
#macchanger --mac yy:yy:yy:yy:yy:yy wlan0
macchanger --mac 00:24:d6:4f:70:24 wlan0
sleep 5
service network-manager start
sleep 5
rmmod iwlwifi
sleep 5
modprobe iwlwifi


