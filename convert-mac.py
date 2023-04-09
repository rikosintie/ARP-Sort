import argparse
import re
import sys

'''
Converts any format mac address to:
    Colon separated: 64:e8:81:43:cc:4e
    HPE format: 64e881-43cc4e
    Cisco Format: 64e8.8143.cc4e
    MS Format: 64-e8-81-43-cc-4e
    No Space Format: 64e88143cc4e

    Usage
    convert-mac.py --mac 64e88143cc4e
    64:e8:81:43:cc:4e
    64e881-43cc4e
    64e8.8143.cc4e
    64-e8-81-43-cc-4e
    64e88143cc4e
'''

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
    colon = mac
    hpe = mac
    cisco = mac
    ms = mac
    # convert mac in canonical form (eg. 00:80:41:ae:fd:7e)
    colon = ":".join(["%s" % (mac[i:i+2]) for i in range(0, 12, 2)])
    # HPE format
    hpe = "-".join(["%s" % (mac[i:i+6]) for i in range(0, 12, 6)])
    # Cisco format
    cisco = ".".join(["%s" % (mac[i:i+4]) for i in range(0, 12, 4)])
    # MS format
    ms = "-".join(["%s" % (mac[i:i+2]) for i in range(0, 12, 2)])
    # Build list of macs
    list1 = [colon, hpe, cisco, ms, mac]
    MAC_Types = '\n'.join(list1)
    return MAC_Types


parser = argparse.ArgumentParser()
parser.add_argument("-a", "--mac", help="mac  address - ex. 64:e8:81:43:cc:4e")
args = parser.parse_args()
mac = args.mac

if mac is None:
    print('-a mac address is a required argument')
    sys.exit()

list_of_macs = format_mac(mac)
print(list_of_macs)
    