# ARP-Sort
**What Does it Do?**

Converts "show ip arp" to a sorted list of IP and MAC addresses.

**Authors:** 
* Carlos Ramirez
* Michael Hubbard

A Cisco switch running a routing protocol maintains an ARP table that maps mac addresses to IP addresses.

This table is useful for troubleshooting but the switch doesn't sort the output and includes some fields like "Protocol" and "Type" that are always going to be the same on an Ethernet/TCP/IP network.

I use the ARP table when I'm replacing a core switch. I run a 'sh ip arp' before the cut and then 'sh ip arp' on the new switch and compare them to make sure all critical servers/devices are working. This script makes it easy (and fast) to compare the before and after since it only contains the IP/MAC and is sorted by IP address. You can include the vlan in the "show ip arp" if you are only working on one vlan. For example - show ip arp vlan 250.

I use Meld on Linux\Windows to compare files. On Windows, Notepad++ is also a good tool. Here is a link to a review of Linux Diff tools - [9 Best File Comparison and Difference (Diff) Tools for Linux](https://www.tecmint.com/best-linux-file-diff-tools-comparison/). Tecmint is a great site for Linux information.

One drawback is that devices will time out of the ARP cache if they aren't active. You may need to ping each device to refresh the ARP cache. There are a few ways to do this:
1. Ping the broadcast mask on the core before running the "sh ip arp". Most devices ignore a broadcast ping for security reasons but I've found that the fire alarms and Environmental Montioring Systems (EMS) that I am interested in do respond to ping x.x.x.255 (for a /24). 
2. Use a tool like nmap or angry IP to ping all addresses in the subnet.
3. If you are a Linux user I wrote a python script that takes the output of 
```
sh run | i ^interface|^_ip address 
```
converts the subnets to hosts and pings each of them. You can grab it here - [pingSVI](https://github.com/rikosintie/pingSVI)

In the sh run command the | i means include, ^ means beginning of line, _ means one space and | is the logical OR. For use with pingSVI you can use just
```
sh run | i ^_ip address
```
since the script doesn't need the interface.


I also use the script to create the input to the [PingInfoView v1.65 - Ping monitor utility](http://www.nirsoft.net/utils/multiple_ping_tool.html). I just run `sh ip arp vlan x` for the vlan of interest, run the script and paste the output into PingInfoView. It uses the MAC as the hostname but that is fine for a lot of situations.

![alt text](https://github.com/rikosintie/ARP-Sort/blob/master/dashboard1.PNG "Logo PingInfo Dashboard")

I do that before the cutover and sort by Servers, Building Management, switches, etc. I put each into a separate PingInfoViewer instance and then I have a dashboard of all critical devices. One look and I can see if something isn't working after the cutover.


## Usage 

Download the files in this repository and unzip them. 

If you have Git installed you can just use:
```
git clone https://github.com/rikosintie/ARP-Sort.git
```
to clone the scripts onto your hard drive.

On the core switch run 
```
term len 0 !turn off paging
show ip arp or show ip arp vlan xx
term len 30 !set page length to 30
```

Save the output in a file named `arp.txt`


## Run the script ##
To execute on windows if the python launcher is installed
```
python -3 arp.py 
```
**On Linux**

```
python3 arp.py
```

## Results
The script will strip off everyting except the IP address and MAC address.

**arp.txt**
```
Internet  10.53.250.4             3   1060.4b9f.62f8  ARPA   Vlan250
Internet  10.53.250.1             -   0012.00f3.febf  ARPA   Vlan250
Internet  10.53.250.2             0   1060.4b9d.db68  ARPA   Vlan250
Internet  10.53.250.12            0   d8d4.3c2e.4b32  ARPA   Vlan250
Internet  10.53.250.15            0   d8d4.3c2e.4b31  ARPA   Vlan250
Internet  10.53.250.11            0   d8d4.3c2e.4b2f  ARPA   Vlan250
Internet  10.53.250.10            0   d8d4.3c2e.4b30  ARPA   Vlan250
```
**Output**
```
10.53.250.1
10.53.250.2
10.53.250.4
10.53.250.10
10.53.250.11
10.53.250.12
10.53.250.15
```
```
10.53.250.1 0012.00f3.febf
10.53.250.2 1060.4b9d.db68
10.53.250.4 1060.4b9f.62f8
10.53.250.10 d8d4.3c2e.4b30
10.53.250.11 d8d4.3c2e.4b2f
10.53.250.12 d8d4.3c2e.4b32
10.53.250.15 d8d4.3c2e.4b31
```
**UPDATE January 11, 2018**
I found a Python tool on github that queries the Wireshark OUI database and returns the manufacture. It can run stand alone at the command line or as a library. I added the library to the script, it's called manuf.py. You will need to have Wireshark installed.

**Manufacturer output** 
 IP, MAC and Manufacture: 21 
```
1192.168.10.1 6c41.6a19.dadf Cisco
192.168.10.2 0090.f80a.9aca Mediatri
192.168.10.3 0090.f80a.9aa0 Mediatri
192.168.10.4 0090.f80b.dffa Mediatri
192.168.10.6 0004.f276.dfe6 Polycom
192.168.10.8 0004.f276.e130 Polycom
192.168.10.11 0004.f276.dfc9 Polycom
192.168.10.14 0004.f276.e02a Polycom
192.168.10.17 0004.f276.dfc0 Polycom
192.168.10.19 0004.f276.dfd0 Polycom
192.168.10.21 0004.f276.e027 Polycom
192.168.10.23 0004.f276.dfb7 Polycom
192.168.10.25 0004.f276.e373 Polycom
192.168.10.27 0004.f276.dfd1 Polycom
192.168.10.29 0004.f276.e2a7 Polycom
192.168.10.32 0004.f276.e018 Polycom
192.168.10.34 0004.f276.dffe Polycom
192.168.10.36 0004.f276.e00a Polycom
192.168.10.38 0004.f276.de85 Polycom
192.168.10.254 0019.92d2.209b Adtran
```
**UPDATE March 7, 2018**
Added code to create a json file. The file contains the mac address as the key and the ip address as the value. If you run the macaddr.py script (available here - [mac2manuf](https://github.com/rikosintie/MAC2Manuf)) in the same folder it will import the json file and then output the ip address with the output. This is useful for edge switches since they don't maintain an ARP table. You will be able to see the manufacturer and IP address for each device on the edge switch.
```
Number Entries: 49 

Vlan     MAC Address      Interface      IP           Vendor
  20    f8b1.56d2.3c13     Gi1/0/3   10.129.20.70    Vendor(manuf='Dell', comment=None)
****************************************************************************
  20    0011.431b.b291     Gi1/0/16   10.129.20.174    Vendor(manuf='Dell', comment=None)
****************************************************************************
  20    9890.96b4.2f6f     Gi1/0/18   10.129.20.16    Vendor(manuf='Dell', comment=None)
****************************************************************************
  20    0080.77cd.b2c4     Gi1/0/21   10.129.20.16    Vendor(manuf='BrotherI', comment=None)
****************************************************************************
  20    ace2.d3d7.44f6     Gi1/0/25   10.129.20.69    Vendor(manuf='HewlettP', comment=None)
****************************************************************************
```

## References ##
* [How to sort IP addresses stored in dictionary in Python?](https://stackoverflow.com/questions/6545023/how-to-sort-ip-addresses-stored-in-dictionary-in-python)
* [Python 3 sort a dict by its values](https://stackoverflow.com/questions/20944483/python-3-sort-a-dict-by-its-values)
* [Python Docs 5.5. Dictionaries](https://docs.python.org/3.3/tutorial/datastructures.html)
* [Parser library for Wireshark's OUI database.](https://github.com/coolbho3k/manuf)
