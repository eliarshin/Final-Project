import socket
import json
import sys
from rich.console import Console
from rich.table import Table
from art import *

console = Console()

class port_scanner:

    PORTS_TO_SCAN = "./common_ports.json"

    #Init our ps struct, including target, which ports are open, and the vulnerabilities
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

    #Check every port that given with the host, if the connection succeeded, we append it on our struck of open ports
    def port_scan(ps, port):
        #find the best time out to catch all the open ports
        #AF_INET represent domain or IP ipv4 address , sock_stream is the default
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try: # we try to establish connection
            conn_status = sock.connect_ex((ps.target, port))
            if conn_status == 0:
                ps.open_ports.append(port)
            sock.close()
        except:
            pass

    #This is an static method that show us the entry message
    #Explain the features we have
    #I designed it with the libraries Art and Rich
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

    #this is an static method that give the IP address from URL
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
        ps.run() # we will create threadpool that we will send function and the ports to there

if __name__ == "__main__":
    port_scan = port_scanner()
    port_scan.init_main()