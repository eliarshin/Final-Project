'Discovering all devices on the network with their IP and MAC address'
'We will see any device that connected to the Router.'
'Every device send ARP Request to specific MAC address to communicate with him'
'All devices on same network will ignore the packet, the only device that will respond'
'is the device that got the IP that sent on ARP , on the response we will get the MAC of the device'
from rich.console import Console
from rich.table import Table
from art import *
import scapy.all as scapy
import socket
import pandas as pd
import os
import netifaces
#TO DO#
'Create Constructor'
'Input from user'
'Display results'

console = Console()
class network_scanner:

    def __init__(net):

        net.target = ""
        net.state = ""
        net.clients_list = []
        net.clients_dict = []
        net.flag = 0

        #scoring tests
        net.scan_succeded = 0
        net.scan_import_all_mac = 0
        net.scan_high_counter_devices = 0

    def get_self_target(net):
        gateways = netifaces.gateways()
        default_gateway = gateways['default'][netifaces.AF_INET][0]
        default_gateway = default_gateway + "/24"
        net.target = default_gateway

    
    def export_results(net):
        ip =[]
        mac =[]
        for e in net.clients_list:
           ip.append(str(e["ip"]))
           mac.append(str(e["mac"])) 
        keys = ["IP","MAC"]
        zip_ip_mac = zip(ip,mac)
        df = pd.DataFrame(columns=['IP', 'MAC'],data=zip_ip_mac)
        df.to_csv('results_net.csv')

    def scan(net):
        arp_request = scapy.ARP(pdst=net.target)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        net.clients_list = []
        for element in answered_list:
            net.client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
            net.clients_list.append(net.client_dict)
        
    def results(net):
            table = Table(show_header=True, header_style="bold green")
            table.add_column("IP", justify="right", style="cyan", no_wrap=True)
            table.add_column("MAC Address", justify="right", style="cyan", no_wrap=True)
            for devices in net.clients_list:
                table.add_row(str(devices["ip"]),str(devices["mac"]))
            console.print(table)
            net.export_results()

    @staticmethod
    def entry_message():
        art_font = text2art("Network Scanner",font='cybermedium',chr_ignore=True)
        console.print(f"[bold red]{art_font}[/bold red]")
        console.print("#" * 55, style="bold green")
        console.print("#"*12,"Advanced Network Scanner", "#"*12,style="dim cyan")
        console.print("#"*11,"Show you all devices that connected to the network", "#"*11,style="dim cyan")
        console.print("#" * 55, style="bold green")
        print()
        console.print("[+]For help press - H")
        console.print("[+]For self network scan press - 1")
        console.print("[+]To choose the network to scan press - 2")
        console.print("[+]To choose the subset for scanning (default 24) - 3")

    def network_scan_success(net):
        if len(net.clients_list) > 0:
            net.scan_succeded = 1
    
    def is_mac_address_found(net):
        counter = 0
        for devices in net.clients_list:
            if len(devices["mac"]) > 0:
                counter = counter + 1
        
        if counter > 0:
            net.scan_import_all_mac = 1
    
    def devices_on_network_check(net):
        if len(net.clients_list) > 8:
            net.scan_high_counter_devices = 1


    def init_main(net):
        net.entry_message()
        
        net.state = console.input("Enter your option")

        if(net.state == '1'):
            #print(default_gateway)
            net.get_self_target()
            net.scan()
            net.results()
            net.network_scan_success()
            net.is_mac_address_found()
            net.devices_on_network_check()
            print(net.scan_succeded)
            print(net.scan_import_all_mac)
            print(net.scan_high_counter_devices)
        if(net.state == 'H' or net.state == 'h'):
            net.read_help()


    def read_help(net):
        with open('./Network Scanner/help.txt', encoding='utf8') as f:
            for line in f:
                print(line.strip())

if __name__ == "__main__":
    network_scan = network_scanner()
    network_scan.init_main()
    # network_scan.entry_message()
    # network_scan.get_target()
    # network_scan.scan()
    # network_scan.results()