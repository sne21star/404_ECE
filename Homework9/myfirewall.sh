'''
Homework Number: 9
Name: Sneha Mahapatra
ECN Login: mahapat0
Due Date: April 2, 2020
'''
#!/bin/sh
# A minimalist sort of a firewall for your laptop:

# Create a new user-defined chain for the filter table: Make sure you first
# flush the previous rules by iptables -t filter F and delete the
# previous chains by iptables -t filter -X
iptables -t filter -N myfirewall.rules

# Accept all packets generated locally:
iptables -A myfirewall.rules -p all -i lo -j ACCEPT

# Accept all ICMP packets regardless of source:
iptables -A myfirewall.rules -p icmp --icmp-type any -j ACCEPT

# You must not block packets that correspond to TCP/IP protocol numbers 50
# (ESP) and 51 (AH) for VPN to work. (See Lecture 20 for ESP and AH.). VPN
# also needs the UDP ports 500 (for IKE), UDP port 10000 (for IPSec
# encapsulated in UDP) and TCP port 443 (for IPSec encapsulated in
# TCP). [Note that if you are behind a NAT device, make sure it does not
# change the source port on the IKE (Internet Key Exchange) packets.  If
# the NAT device is a Linksys router, just enable "IPSec Passthrough":
iptables -A myfirewall.rules -p 50 -j ACCEPT
iptables -A myfirewall.rules -p 51 -j ACCEPT
iptables -A myfirewall.rules -p udp --dport 500 -j ACCEPT
iptables -A myfirewall.rules -p udp --dport 10000 -j ACCEPT

# The destination port 443 is needed both by VPN and by HTTPS:
iptables -A myfirewall.rules -p tcp --dport 443 -j ACCEPT

# For multicast DNS (mDNS) --- allows a network device to choose a domain
# name in the .local namespace and announce it using multicast.  Used by
# many Apple products.  mDNS works differently from the unicast DNS we
# discussed in Lecture 17.  In mDNS, each host stores its own information
# (for example its own IP address).  If your machine wants to get the IP
# address of such a host, it sends out a multicast query to the multicast
# address 224.0.0.251.
iptables -A myfirewall.rules -p udp --dport 5353 -d 224.0.0.251 -j ACCEPT

# for the Internet Printing Protocol (IPP):
iptables -A myfirewall.rules -p udp -m udp --dport 631 -j ACCEPT

# Accept all packets that are in the states ESTABLISHED and RELATED (See
# Section 18.11 for packet states):
iptables -A myfirewall.rules -p all -m state --state ESTABLISHED,RELATED -j ACCEPT

# I run SSH server on my laptop.  Accept incoming connection requets:
iptables -A myfirewall.rules -p tcp --destination-port 22 -j ACCEPT

# sendmail running on my laptop requires port 25
#iptables -A myfirewall.rules -p tcp --destination-port 25 -j ACCEPT

# Does fetchmail need port 143 to talk to IMAP server on RVL4:
#iptables -A myfirewall.rules -p tcp --destination-port 143 -j ACCEPT

# I run Apache httpd web server on my laptop:
iptables -A myfirewall.rules -p tcp --destination-port 80 -j ACCEPT

# Drop all other incoming packets.  Do not send back any ICMP messages for
# the dropped packets:
iptables -A myfirewall.rules -p all -j REJECT --reject-with icmp-host-prohibited

iptables -I INPUT -j myfirewall.rules
iptables -I FORWARD -j myfirewall.rules

#Line 1 Remove any previous rules or chains
sudo iptables -t filter -F
sudo iptables -t filter -X
sudo iptables -t mangle -F
sudo iptables -t mangle -X
sudo iptables -t nat -F
sudo iptables -t nat -X
sudo iptables -t raw -F
sudo iptables -t raw -X

#Line 2 For all outgoing packets, change their source IP address to your own machine’s IP address
var=$(hostname -I)
sudo iptables -t nat -A POSTROUTING -o $var -j MASQUERADE

#Line 3 Block a list of specific IP addresses (of your choosing) for all incoming connections.
sudo iptables -A INPUT -s 209.175.44.100 -j DROP

#Line 4 Block your computer from being pinged by all other hosts (Hint: ping uses ICMP Echo
#requests).
sudo iptables -A myfirewall.rules -p icmp --icmp-type echo-request -j DROP
#sudo iptables -A INPUT -p icmp --icmp-type echo-request -j REJECT

#Line 5 Set up port-forwarding from an unused port of your choice to port 22 on your computer.
# Test if you can SSH into your machine using both ports
# (Hint: You need to enable connections on the unused port as well).


#Line 6 Allow for SSH access (port 22) to your machine from only the engineering.purdue.edu domain.
sudo iptables -A INPUT -p tcp -s 128.46.104.5 --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT

# Line 7 Assuming you are running an HTTPD server on your machine that can make available your entire
# home directory to the outside world, write a rule that allows only a single IP address in the internet
# to access your machine for the HTTP service.
sudo iptables

#Line 8 Permit Auth/Ident (port 113) that is used by some services like SMTP and IRC.
tcp_services = "113"
sudo iptables -A INPUT -m state --state=ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -i $ext_if -p tcp --dport $tcp_services --syn -j ACCEPT