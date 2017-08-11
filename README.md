# ARP-Sort
Convert "sh ip arp" to a sorted list of IP and MAC addresses.

**Authors:** 
* Carlos Ramirez
* Michael Hubbard

A Cisco switch running a routing protocol maintains a "Mac address-table" that maps a device's mac address to it's IP address.

This table is useful for trouble shooting but the switch doesn't sort the output and includes some fields like "Protocol" and "Type" that are always going to be the same on an Ethernet/TCP/IP network so are useless.

I use the mac address table when I'm replacing a core switch. I run a 'sh ip arp' before the cut and then one on the new switch and compare them to make sure all critical servers/devices are working. This script makes it easy (and fast) to compare the before and after since it only contains the IP/MAC and is sorted by IP address. 

I use Meld on Linux to compare files. On Windows, Notepad++ is my go to tool. Here is a link to a review of Linux Diff tools - [9 Best File Comparison and Difference (Diff) Tools for Linux](https://www.tecmint.com/best-linux-file-diff-tools-comparison/). Tecmint is a great site for Linux information.

You may need to ping the broadcast mask on the core before running the "sh ip arp" to make sure all devices are in the table. Most devices ignore a broadcast ping for security reasons but I've found that the fire alarms and Environmental Montioring Systems (EMS) that I am interested in do respond.

I also use the script to create the input to the [PingInfoView v1.65 - Ping monitor utility](http://www.nirsoft.net/utils/multiple_ping_tool.html) tool. I just run `sh ip arp vlan x` for the vlan of interest, run the script and pasted the output into PingInfoView. It uses the MAC as the hostname but that is fine for a lot of situations.


## Usage 

Download the files in this repository and unzip them. 

If you have Git installed you can just use:
```
git clone https://github.com/rikosintie/ARP-Sort.git
```
To clone the scripts

On the core switch run 
```
term len 0 #turn off paging
show ip arp or show ip arp vlan xx
term len 30 #set page length to 30
```

Save the output in a file named `arp.txt`

Start the copy on the first line with an IP address. 

Don't include the 
`show ip arp` command or the header 
`Protocol  Address          Age (min)  Hardware Addr   Type   Interface` 
in the file.

Start the copy on the line that looks like this:
```
Internet  10.56.246.196           0   e865.49c7.9f80  ARPA   Vlan246
```
Make sure there isn't a blank line at the end of the file. This will cause an error

`OSError: illegal IP address string passed to inet_aton`

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
## References ##
* [How to sort IP addresses stored in dictionary in Python?](https://stackoverflow.com/questions/6545023/how-to-sort-ip-addresses-stored-in-dictionary-in-python)
* [Python 3 sort a dict by its values](https://stackoverflow.com/questions/20944483/python-3-sort-a-dict-by-its-values)
* [5.5. Dictionaries](https://docs.python.org/3.3/tutorial/datastructures.html)
