'Discovering all devices on the network with their IP and MAC address'
'We will see any device that connected to the Router.'
'Every device send ARP Request to specific MAC address to communicate with him'
'All devices on same network will ignore the packet, the only device that will respond'
'is the device that got the IP that sent on ARP , on the response we will get the MAC of the device'
from rich.console import Console
from rich.table import Table
from art import *
import scapy.all as scapy
from nmap import PortScanner
import socket

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
    
    def get_target(net):
        net.target = "192.168.1.172/24"

    
    
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

    def init_main(net):
        net.entry_message()
        
        net.state = console.input("Enter your option")

        if(net.state == '1'):
            net.get_target()
            net.scan()
            net.results()

        elif(net.state == 'H' or net.state == 'h'):
            net.read_help()
        
        elif(net.state == '3'):
            net.target = input("Please enter your target with the following build : 00.00.00.00/subset")
            net.get_target()
            net.scan()
            net.results()
        else:
            print("Bad input - Please choose from the menu")
            net.init_main()

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