#!/usr/bin/env python3
from TcpAttack import *

# Your TcpAttack class should be named as TcpAttack
spoofIP = "199.164.42.228"
targetIP = "128.46.144.123"  # Will contain actual IP addresses in real script
rangeStart = 551
rangeEnd = 555
port = 554
Tcp = TcpAttack(spoofIP, targetIP)
Tcp.scanTarget(rangeStart, rangeEnd)
if Tcp.attackTarget(port, 1):
    print("port was open to attack")
