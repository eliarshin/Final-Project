'Discovering all devices on the network with their IP and MAC address'
'We will see any device that connected to the Router.'
'Every device send ARP Request to specific MAC address to communicate with him'
'All devices on same network will ignore the packet, the only device that will respond'
'is the device that got the IP that sent on ARP , on the response we will get the MAC of the device'

import scapy.all as scapy

def scan(ip):
    scapy.arping(ip)

scan("172.29.96.1")