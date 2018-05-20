'''
References:
https://stackoverflow.com/questions/6545023/how-to-sort-ip-addresses-stored-in-dictionary-in-python/6545090#6545090
https://stackoverflow.com/questions/20944483/python-3-sort-a-dict-by-its-values
https://docs.python.org/3.3/tutorial/datastructures.html

read a file containing the output of "sh ip arp" from a Nexus switch and create a sorted list of IP addresses and
IP/Mac Address conbinations.

In this example "sh ip arp vl 250". Save output as arp.txt

Address         Age       MAC Address     Interface
10.56.254.41    00:14:14  b863.4d8c.0859  Vlan254
10.56.254.62    00:00:39  34ab.37bd.177b  Vlan254
10.56.254.65    00:09:43  3cab.8e59.bdaa  Vlan254
10.56.254.66    00:00:46  ccc7.6010.5597  Vlan254
10.56.254.67    00:00:02  848e.0c8e.96e9  Vlan254
10.56.254.68    00:17:20  6067.2067.c9c6  Vlan254
10.56.254.70    00:00:20  INCOMPLETE      Vlan254

Run the script. Output is a list of correctly sorted list of IPs and MAC Addresses.

Output
10.53.250.1
10.53.250.2
10.53.250.4
10.53.250.10
10.53.250.11
10.53.250.12
10.53.250.15

10.53.250.1 0012.00f3.febf
10.53.250.2 1060.4b9d.db68
10.53.250.4 1060.4b9f.62f8
10.53.250.10 d8d4.3c2e.4b30
10.53.250.11 d8d4.3c2e.4b2f
10.53.250.12 d8d4.3c2e.4b32
10.53.250.15 d8d4.3c2e.4b31

'''
from socket import inet_aton
import struct
from socket import inet_aton,inet_ntoa
import struct
import manuf
import json
import sys
import re

def ip2long(ip):
    packed = inet_aton(ip)
    lng = struct.unpack("!L", packed)[0]
    return lng


def long2ip(lng):
    packed = struct.pack("!L", lng)
    ip=inet_ntoa(packed)
    return ip

vernum = '1.0'
def version():
    """
    This function prints the version of this program. It doesn't allow any argument.
    """
    print("+----------------------------------------------------------------------+")
    print("| "+ sys.argv[0] + " Version "+ vernum +"                                               |")
    print("| This program is free software; you can redistribute it and/or modify |")
    print("| it in any way you want. If you improve it please send me a copy at   |")
    print("| the email address below.                                             |")
    print("|                                                                      |")
    print("| Author: Michael Hubbard, michael.hubbard999@gmail.com                |")
    print("|         mwhubbard.blogspot.com                                       |")
    print("|         @rikosintie                                                  |")
    print("+----------------------------------------------------------------------+")

version()

#create a space between the command line and the output
print()
#create a blank list to accept each line in the file
data1 = []
#create a blank list to accept line split
temp = []
try:
    f = open('arp.txt', 'r')
except FileNotFoundError:
            print('arp.txt does not exist')
else:
#try to eliminate any lines that don't contain the IP and MAC address
#10.56.254.2     00:04:44  c08c.6036.19ef  Vlan254
    for line in f:
#        line = line.strip('\n')
#MAC addresses are expressed differently depending on the manufacture and even model of the device
# the formats that this script can parse are:
# 0a:0a:0a:0a:0a:0a, 0a-0a-0a-0a-0a-0a, 0a0a0a.0a0a0a0 and 0a0a0a-0a0a0a
# this should cover most Cisco and HP devices.
        match_PC = re.search(r'([0-9A-F]{2}[-:]){5}([0-9A-F]{2})', line, re.I)
        match_Cisco = re.search(r'([0-9A-F]{4}[.]){2}([0-9A-F]{4})', line, re.I)
        match_HP = re.search(r'([0-9A-F]{6}[-])([0-9A-F]{6})', line, re.I)
        # strip out lines without a mac address
        if match_PC or match_Cisco or match_HP:
            data1.append(line)
#Split line into parts, index(0) = IP, index(1) = age, index(2) = MAC, index(3)  = vlan
        temp = line.split()
        if len(temp) > 2:
            if len(temp[2]) == 14:
                data1.append(line)
    f.close

# string length
i = len(data1)-1
d = i + 1
counter = 0
sItems = []
IPs = []
data = {}
data2 = {}
temp = []
while counter <= i:
    IP = data1[counter]
#   Split line and save it in a list
#   index 0 = IP, Index 1 = age, index 2 = MAC, index 3 = vlan
    temp = IP.split()
    Mac = temp[2]
    Vlan = temp[3]
    MacAndVlan = Mac + " " + Vlan
    IP = temp[0]
    IPs.append(str(IP))
#   Convert IP to a long so it can be sorted.
#   See https://stackoverflow.com/questions/6545023/how-to-sort-ip-addresses-stored-in-dictionary-in-python/6545090#6545090
    IP = ip2long(IP)
# add IP address and MAC to dictionary
    data[IP] = Mac
    data2[IP] = MacAndVlan
    counter = counter + 1
#Sort IPs
IPs = sorted(IPs, key=lambda ip: struct.unpack("!L", inet_aton(ip))[0])
print ('Number of IP Addresses: %s ' %d)
for IP in IPs:
    print(IP)

print()
print ('Number of IP and MAC Addresses: %s ' %d)
#Create an empty dictionary to hold mac-ip pairs. Will be used with macaddr.py to output ip with interface
Mac_IP = {}
s = [(k, data[k]) for k in sorted(data)]
for k, v in s:
#   Convert IP back to dotted quad notation.
    k  = long2ip(k)
    print(k, v)
    Mac_IP[v] = k
    if "1cc1.de43.aeb7" in Mac_IP:
        print('The IP for MACA %s is  %s' %(v, k))
#    print(Mac_IP)

print()
print ('Number of IP, MAC and VLAN: %s ' %d)

s = [(k, data2[k]) for k in sorted(data2)]
for k, v in s:
    k  = long2ip(k)
    print(k, v)
#
#
#look up manufacture from MAC
print()
#
p = manuf.MacParser()

#Print IP, MAC, Manufacture
print ('Number of IP, MAC and Manufacture: %s ' %d)
print()
s = [(k, data[k]) for k in sorted(data)]
for k, v in s:
#   Convert IP back to dotted quad notation.
    k  = long2ip(k)
    manufacture = p.get_manuf(v)

    print(k, v, manufacture)
#Write the dictionary out as Mac2IP.json so that it can be used in macaddr.py
mydatafile = 'Mac2IP.json'
with open(mydatafile, 'w') as f:
    json.dump(Mac_IP, f)
