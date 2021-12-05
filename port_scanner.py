import socket
import sys
import json
from rich.console import Console
from rich.table import Table
from art import *
from threadpool import threadpool

#Things to DO
'1.Add Scanning Options for the Costumer'
'2.Add Description and Help Functions for the customer'
'3.Play with display fonts and make it good for the eye'

console = Console()
class port_scanner:

    PORTS_TO_SCAN = "./common_ports.json"
    #
    'Add advanced scan , and also choosing by user'
    #

    #Init of our struct
    def __init__(ps):
        ps.target = "" # The host we scan
        ps.open_ports = [] # collecting open ports
        ps.ports_vulnerability = {} # collecting vulnerability information
        
    #Extracting data from json file to our struct
    def read_from_json(ps):
        with open(port_scanner.PORTS_TO_SCAN, "r") as file:
            data = json.load(file)
        #print(data)
        ps.ports_vulnerability = {int(k): v for (k, v) in data.items()}

    #trying connection with the target through the port , if theres an respond we get the opened port
    def port_scan(ps, port):
        #find the best time out to catch all the open ports
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            conn_status = sock.connect_ex((ps.target, port))
            if conn_status == 0:
                ps.open_ports.append(port)
            sock.close()
        except:
            pass

    #display the results on table
    def display_results(ps):
        print()
        if ps.open_ports:
            console.print("Scan Completed. Open Ports:", style="bold blue")
            table = Table(show_header=True, header_style="bold green")
            table.add_column("Released", justify="right", style="cyan", no_wrap=True)
            table.add_column("Released", justify="right", style="cyan", no_wrap=True)
            table.add_column("Released", justify="right", style="red", no_wrap=True)
            for port in ps.open_ports:
                table.add_row(str(port), "OPEN", ps.ports_vulnerability[port])
            console.print(table)
        else:
            console.print(f"No Open Ports Found on Target", style="bold magenta")

    #
    @staticmethod
    def entry_message():
        art_font = text2art("port scanner",font='cybermedium',chr_ignore=True)
        console.print(f"[bold red]{art_font}[/bold red]")
        console.print("#" * 55, style="bold green")
        console.print("#"*12,"Advanced Port Scanner Including", "#"*12,style="dim cyan")
        console.print("#"*11,"A Wide Range of Scanning Options", "#"*11,style="dim cyan")
        console.print("#" * 55, style="bold green")
        print()
        console.print("[+]For help press - H")
        console.print("[+]For advanced scan (all ports) press - 1")
        console.print("[+]For built in scan press - 2")
        console.print("To choose range of ports to scan press - 3")
        console.print("To add your own JSON port file press - 4")

    @staticmethod
    def url_to_ip(target):
        try:
            ip_addr = socket.gethostbyname(target)
        except socket.gaierror as e:
            console.print(f"{e}. Exiting.", style="bold red")
            sys.exit()
        console.print(f"\nIP The IP address of the url is: [bold blue]{ip_addr}[/bold blue]")
        return ip_addr

    def init_main(ps):
        ps.entry_message()
        ps.read_from_json()
        target = console.input("[dim cyan]Enter target URL or IP address: ")
        num_of_workers = console.input("[dim cyan]Enter num of workers: ")
        ps.target = ps.url_to_ip(target)
  
        ps.run()

    def run(ps):
        threadpool(ps.port_scan, ps.ports_vulnerability.keys(), len(ps.ports_vulnerability.keys()))
        ps.display_results()
        #print(len(ps.ports_vulnerability.keys()))


if __name__ == "__main__":
    port_scan = port_scanner()
    port_scan.init_main()