'''
References:
https://stackoverflow.com/questions/6545023/how-to-sort-ip-addresses-stored-in-dictionary-in-python/6545090#6545090
https://stackoverflow.com/questions/20944483/python-3-sort-a-dict-by-its-values
https://docs.python.org/3.3/tutorial/datastructures.html

read a file containing the output of "sh ip arp" and create a sorted list of IP addresses and 
IP/Mac Address conbinations.

In this example "sh ip arp vl 250". Save output as arp.txt

Internet  10.53.250.4             3   1060.4b9f.62f8  ARPA   Vlan250
Internet  10.53.250.1             -   0012.00f3.febf  ARPA   Vlan250
Internet  10.53.250.2             0   1060.4b9d.db68  ARPA   Vlan250
Internet  10.53.250.12            0   d8d4.3c2e.4b32  ARPA   Vlan250
Internet  10.53.250.15            0   d8d4.3c2e.4b31  ARPA   Vlan250
Internet  10.53.250.11            0   d8d4.3c2e.4b2f  ARPA   Vlan250
Internet  10.53.250.10            0   d8d4.3c2e.4b30  ARPA   Vlan250

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

def ip2long(ip):
    packed = inet_aton(ip)
    lng = struct.unpack("!L", packed)[0]
    return lng


def long2ip(lng):
    packed = struct.pack("!L", lng)
    ip=inet_ntoa(packed)
    return ip

#create a space between the command line and the output
print()
#create a blank list to accept each line in the file
listname = []
f = open('arp.txt', 'r')
for line in f:
    listname.append(line)
f.close
# string length
i = len(listname)-1
d = i + 1
counter = 0
sItems = []
IPs = []
data = {}
while counter <= i:
    IP = listname[counter]
    #Remove Enter
    IP = IP.strip('\n')
    Mac = IP
    Vlan = Mac.find('Vlan')
    Mac = Mac[38:Vlan-9].rstrip('')
    #print (Mac)
    #Find the space after IP
    AfterIP = IP.find('   ')
    #Remove Characters After IP
    IP = IP[0:AfterIP].rstrip('')
    #Remove Internet before IP
    IP = IP.replace('Internet  ','')
    IPs.append(str(IP))
#   Convert IP to a long so it can be sorted. 
#   See https://stackoverflow.com/questions/6545023/how-to-sort-ip-addresses-stored-in-dictionary-in-python/6545090#6545090     
    IP = ip2long(IP)
# add IP address and MAC to dictionary
    data[IP] = Mac    
    counter = counter + 1
IPs = sorted(IPs, key=lambda ip: struct.unpack("!L", inet_aton(ip))[0])
print (' # IP Addresses: %s ' %d)
for IP in IPs:
    print(IP)
print()
print (' # IP and MAC Addresses: %s ' %d)
s = [(k, data[k]) for k in sorted(data)]
for k, v in s:
#   Convert IP back to dotted quad notation. 
    k  = long2ip(k)
    print(k, v)

	
