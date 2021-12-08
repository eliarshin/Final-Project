'Discovering all devices on the network with their IP and MAC address'
'We will see any device that connected to the Router.'
'Every device send ARP Request to specific MAC address to communicate with him'
'All devices on same network will ignore the packet, the only device that will respond'
'is the device that got the IP that sent on ARP , on the response we will get the MAC of the device'
from rich.console import Console
from rich.table import Table
from art import *
import scapy.all as scapy

#TO DO#
'Create Constructor'
'Input from user'
'Display results'

def create_packet(ip):
    arp_req = scapy.ARP(pdst = ip) # create ARP packet object and the current IP 
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")  # create Ethernet packet
    arp_req_brod = broadcast/arp_req
    #print(arp_req_brod.summary())
    #scapy.ls(scapy.ARP()) # show us information of scapy ARP functions.
    #scapy.arping(ip)
    return arp_req_brod

def parse(packet):
    for data in packet:
        print(data[1].psrc)
        print(data[1].hwsrc)
        print("-" * 11)

def send_packet(packet):
    ans_packet,unans_packet = scapy.srp(packet, timeout = 1)
    #print(ans_packet.summary()) # clients that used
    #print(unans_packet.summary()) # no clients using them
    return ans_packet

ret = create_packet("172.29.96.1/24")
ans = send_packet(ret)
parse(ans)