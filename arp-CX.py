import json
import re
import struct
from socket import inet_aton, inet_ntoa

from icecream import ic

import manuf

# ic.enable()
ic.disable()
'''
References:
https://github.com/wireshark/wireshark/blob/master/manuf
https://stackoverflow.com/questions/6545023/how-to-sort-ip-addresses-stored-in-dictionary-in-python/6545090#6545090
https://stackoverflow.com/questions/20944483/python-3-sort-a-dict-by-its-values
https://docs.python.org/3.3/tutorial/datastructures.html
reachable
read a file containing the output of "sh arp" on an Aruba CX switch and create a sorted list of IP addresses and 
IP/Mac Address conbinations.

sh arp vrf PD-VRF

IPv4 Address     MAC                Port    Physical Port State    VRF       
-------------------------------------------------------------------------------------------------------------------
10.50.39.36      34:75:c7:e4:7c:46  vlan20   lag254       reachable  PD-VRF
10.50.39.60      24:d9:21:3c:ab:9c  vlan20   lag254       reachable  PD-VRF
10.50.39.154     24:d9:21:4c:93:ef  vlan20   lag254       reachable  PD-VRF
10.50.40.194     00:05:1e:8f:26:6f  vlan40   lag254       reachable  PD-VRF
10.50.41.1       ac:cc:8e:51:95:52  vlan41   lag254       reachable  PD-VRF
10.50.40.114     00:40:84:23:2f:08  vlan40   lag254       reachable  PD-VRF
10.50.39.110     34:75:c7:e4:7c:15  vlan20   lag254       reachable  PD-VRF
10.50.42.199     6c:2b:59:fa:35:3e  vlan42   lag254       reachable  PD-VRF

Internet  10.50.43.19             1   509a.4c16.60f6  ARPA   Vlan42

Run the script. Output is a list of correctly sorted list of IPs and MAC Addresses.

Output

'''



#  https://stackoverflow.com/questions/11006702/elegant-format-for-a-mac-address-in-python-3-2
def format_mac(mac: str) -> str:
    """Converts most common MAC address formats
    into aa:bb:cc:dd:ee:ff format

    '008041aefd7e',  # valid
    '00:80:41:ae:fd:7e',  # valid
    '00:80:41:AE:FD:7E',  # valid
    '00:80:41:aE:Fd:7E',  # valid
    '00-80-41-ae-fd-7e',  # valid
    '0080.41ae.fd7e',  # valid
    '00 : 80 : 41 : ae : fd : 7e',  # valid
    '  00:80:41:ae:fd:7e  ',  # valid
    '00:80:41:ae:fd:7e\n\t',  # valid

    'aa:00:80:41:ae:fd:7e',  # invalid
    '0:80:41:ae:fd:7e',  # invalid
    'ae:fd:7e',  # invalid
    '$$:80:41:ae:fd:7e',  # invalid

    Args:
        mac (str): A valid mac address format

    Returns:
        str: MAC in aa:bb:cc:dd:ee:ff format
    """
    mac = re.sub('[.:-]', '', mac).lower()  # remove delimiters, convert to lc
    mac = ''.join(mac.split())  # remove whitespaces
    assert len(mac) == 12  # length should be now exactly 12 (eg. 008041aefd7e)
    assert mac.isalnum()  # should only contain letters and numbers
    # convert mac in canonical form (eg. 00:80:41:ae:fd:7e)
    mac = ":".join(["%s" % (mac[i:i+2]) for i in range(0, 12, 2)])
    return mac

def ip2long(ip):
    packed = inet_aton(ip)
    lng = struct.unpack("!L", packed)[0]
    return lng


def long2ip(lng):
    packed = struct.pack("!L", lng)
    ip = inet_ntoa(packed)
    return ip

# cisco style
# Internet  10.50.57.1              0   004e.01b7.d9f6  ARPA   Vlan10

print()
# create a blank list to accept each line in the file
data1 = []
try:
    f = open('arp.txt', 'r')
except FileNotFoundError:
    print('arp.txt does not exist')
else:
    # try to eliminate any lines that don't contain the IP and MAC address
    for line in f:
        if line.find('Address') != -1:
            continue
        elif line.find('Incomp') != -1:
            continue
        elif line.find('#') != -1:
            continue
        if line.strip() and line.find('reachable') != -1:
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
while counter <= i:
    IP = data1[counter]
    ic(IP)
    # Remove Enter
    #  IP = IP.strip('\n')
    Mac = IP
    #  split the line into elements ip, mac, port, physical port, state, vrf
    M1 = Mac.split()
    Mac = M1[1]
    #  Convert all mac formats to : separated
    Mac = format_mac(Mac)
    ic(M1)
    ic(Mac)

    #  Add mac, port, physical port, vrf
    MacAndVlan = M1[1] + " " + M1[2] + " " + M1[3] + " " + M1[5]
    ic(MacAndVlan)
    # Find the space after IP
    AfterIP = IP.find('   ')
    # Remove Characters After IP
    IP = IP[0:AfterIP].rstrip('')
    # Remove Internet before IP
    IP = IP.replace('Internet  ', '')
    IPs.append(str(IP))
    ic(IP)
    ic(IPs)
#   Convert IP to a long so it can be sorted.
#   See https://stackoverflow.com/questions/6545023/how-to-sort-ip-addresses-stored-in-dictionary-in-python/6545090#6545090     
    IP = ip2long(IP)
    ic(IP)
# add IP address and MAC to dictionary
    data[IP] = Mac
    data2[IP] = MacAndVlan
    ic(data)
    ic(data2[IP])
    counter = counter + 1
# Sort IPs
IPs = sorted(IPs, key=lambda ip: struct.unpack("!L", inet_aton(ip))[0])
print('-' * 29)
print(f'Number of IP Addresses: {d}')
print('-' * 29)
for IP in IPs:
    print(IP)

print()
print()
print(f'Number of IPs, MAC Addresses: {d}')
print()
# Create an empty dictionary to hold mac-ip pairs.
# Will be used with macaddr.py to output ip with interface
Mac_IP = {}
s = [(k, data[k]) for k in sorted(data)]
ic(s)
for k, v in s:
    #   Convert IP back to dotted quad notation.
    k = long2ip(k)
    print(k, v)
    Mac_IP[v] = k
    if "1cc1.de43.aeb7" in Mac_IP:
        print('The IP for MACA %s is  %s' % (v, k))
    ic(Mac_IP)
print()
print()
print('-' * 58)
print(f'Number of IPs, MACs, Ports, Physical ports, and VRFs: {d}')
print('-' * 58)
print()
ic(d)
s = [(k, data2[k]) for k in sorted(data2)]
for k, v in s:
    k = long2ip(k)
    print(k, v)
#
# look up manufacture from MAC
print()
#
p = manuf.MacParser()

# Print IP, MAC, Manufacture
print()
print('-' * 43)
print(f'Number of IPs, MACs and Manufactures: {d}')
print('-' * 43)
print()
s = [(k, data[k]) for k in sorted(data)]
ic(s)
for k, v in s:
    #   Convert IP back to dotted quad notation.
    k = long2ip(k)
    manufacture = p.get_manuf(v)

    print(k, v, manufacture)
# Write the dictionary out as Mac2IP.json so that it can be used in macaddr.py
mydatafile = 'Mac2IP.json'
with open(mydatafile, 'w') as f:
    json.dump(Mac_IP, f)
