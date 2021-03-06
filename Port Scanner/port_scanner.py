import collections
from pickle import TRUE
import socket
import string
import sys
import json
import random
#from turtle import pd
from typing import OrderedDict
from cv2 import threshold
from numpy import False_
from rich.console import Console
from rich.table import Table
from art import *
from threadpool import threadpool
import pandas as pd
import openpyxl

#Things to DO
'1. Add method to scan bulk from user directory'
'2. Edit the help functions'
'3. Find a database that giving information about open ports'
'4. Add port scan also for UDP services'


console = Console() ## for pretty write

##the class
class port_scanner:

    PORTS_TO_SCAN = "./Port Scanner/common_ports.json"
    #
    'Add advanced scan , and also choosing by user'
    #

    #Init of our struct
    def __init__(ps):
        ps.target = "" # The host we scan
        ps.target_url = ""
        ps.target_host = ""
        ps.open_ports = [] # collecting open ports
        ps.input_ports =[] #input from user
        ps.ports_vulnerability = {} # collecting vulnerability information
        ps.recived_data = {}
        ps.db = ""
        ps.state = "" # which state we are
        ps.service_name=[]
        ps.description=[]
        ps.export = [] # export it

        #scoring variables
        ps.scan_flag_start = 0
        ps.scan_flag_complete = 0

        ps.scan_started = 0
        ps.counter_open_ports = 0
        ps.scan_completed = 0
        ps.vulnerable_ports_found = 0
        #
        ps.final_score = 0
        ps.report_message = []
        ps.common_unsecure_ports = []

    def export_results(ps):
        ports =[]
        desc = []
        informative = pd.read_excel('./Port Scanner/Informative.xlsx')
        pd.set_option('display.max_colwidth', -1)
        #informative.dropna(inplace=True)
        #print(informative.head)

        for port in ps.open_ports:
            a = informative['Info'].where(informative['Port'] == (port))
            b = a.dropna()
            #print(" b ==",str(b))
            ports.append(str(port))
            desc.append(str(b))
        keys = ['port','description']
        zip_ports_desc = zip(ports,desc)
        # zipped_all=dict(zip(keys,zip_ports_desc))    
        #ps.export.append(ports,desc)
        df = pd.DataFrame(columns=['port', 'description'],data=zip_ports_desc)
        
        #print(df)
        df.to_csv('results.csv')
        

    #Extracting data from json file to our struct
    def read_from_json(ps):
        with open(port_scanner.PORTS_TO_SCAN, "r") as file: ## read and create dictionary
            data = json.load(file)
        ps.ports_vulnerability = {int(k): v for (k, v) in data.items()}


    #work it
    def read_from_db(ps):
        ps.db = pd.read_csv('./Port Scanner/db.csv')
        ps.db = ps.db.drop_duplicates(subset=['Port Number'])
        for port in ps.open_ports:
            a = ps.db['Service Name'].where(ps.db['Port Number'] == str(port))
            b = a.dropna()
            d = ps.db['Description'].where(ps.db['Port Number'] == str(port))
            c = d.dropna()
            ps.service_name.append(b)
            ps.description.append(c)


    #trying connection with the target through the port , if theres an respond we get the opened port
    def port_scan(ps, port):
        #find the best time out to catch all the open ports
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            conn_status = sock.connect_ex((ps.target, port))
            if conn_status == 0: # if connection established
                ps.open_ports.append(port)
                msg = sock.recv(4096) # recived answer to dictionary
                ps.recived_data[port] = msg #Recied data into dictionary
                ps.scan_flag_start = 1
            sock.close()
        except:
            pass

    #input from user - using us for input from user + for advanced scan
    def user_range_ports(ps,x,y):
        for i in range (int(x),int(y)):
            ps.input_ports.append(i)
        

    #display the results on table
    def display_results(ps):
        print()
    
        if ps.state=='1': # case one - advanced full scan
            console.print("Scan Completed. Open Ports:", style="bold blue")
            table = Table(show_header=True, header_style="bold green")
            table.add_column("PORT", justify="right", style="cyan", no_wrap=True)
            table.add_column("STATUS", justify="right", style="cyan", no_wrap=True)
            table.add_column("Vulnerability", justify="right", style="red", no_wrap=True)
            for port in ps.open_ports: ## need to add database with the vulnerability of the ports
                table.add_row(str(port), "OPEN", str(port))

        elif ps.state=='2': # compresed scan - built in ports and information about them
            console.print("Scan Completed. Open Ports:", style="bold blue")
            table = Table(show_header=True, header_style="bold green")
            table.add_column("PORT", justify="right", style="cyan", no_wrap=True)
            table.add_column("STATUS", justify="right", style="cyan", no_wrap=True)
            table.add_column("Vulnerability", justify="right", style="red", no_wrap=True)
            for port in ps.open_ports:
                table.add_row(str(port), "OPEN", ps.ports_vulnerability[port])
            
            

        elif ps.state=='3': # input ports from the user
            console.print("Scan Completed. Open Ports:", style="bold blue")
            table = Table(show_header=True, header_style="bold green")
            table.add_column("PORT", justify="right", style="cyan", no_wrap=True)
            table.add_column("STATUS", justify="right", style="cyan", no_wrap=True)
            table.add_column("Vulnerability", justify="right", style="red", no_wrap=True)
            for port,serv in zip(ps.open_ports,ps.service_name): ## need to add database with the vulnerability of the ports
                table.add_row(str(port), "OPEN",str(serv))
 
                
            
        console.print(table)

    #shuffle ports to not be detected as port scan
    def shuffle_ports(ps):
        if ps.state == '1':
            random.shuffle(ps.input_ports)
        if ps.state == '2':
            ("inside 3")
            shuffling = list(ps.ports_vulnerability.items())
            random.shuffle(shuffling)
            ps.ports_vulnerability = collections.OrderedDict(shuffling)
        if ps.state == '3':
            random.shuffle(ps.input_ports)

    #static method that pop up our main screen
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
        console.print("[+]To choose range of ports to scan press - 3")
        console.print("[+]To add your own JSON port file press - 4")

    #static method that gives us the IP address of the target
    @staticmethod
    def url_to_ip(target):
        try:
            ip_addr = socket.gethostbyname(target)
            check = socket.gethostbyaddr(ip_addr)
            #print("CHECK IS @@@@@@@@@@@@@@@@@@@@@@@@",check[0])
        except socket.gaierror as e:
            console.print(f"{e}. Exiting.", style="bold red")
            sys.exit()
        console.print(f"\nIP The IP address of the url is: [bold blue]{ip_addr}[/bold blue]")
        return ip_addr

    #main function - we choose here which option we choose
    def init_main(ps):
        ps.entry_message()
        #ps.read_from_db()
        ps.state = console.input(" Enter your scan option: ")
        

        if ps.state == '1':
            target = console.input("[dim cyan]Enter target URL or IP address: ")
            ps.target_url = target
            ps.target = ps.url_to_ip(target)
            ps.user_range_ports(2,65535)
            ps.shuffle_ports()
            ps.run()

        if ps.state == '2':
            ps.read_from_json()
            target = console.input("[dim cyan]Enter target URL or IP address: ")
            ps.target_url = target
            ps.target = ps.url_to_ip(target)
            ps.shuffle_ports()
            ps.run()
            #ps.display_results()
            ps.execute_tests()
            ps.final_results()
            ps.export_results()
            #print(f"Recived extra data :{ps.recived_data}")
            ps.is_ports_vulnerable()

        if ps.state == '3':
            target = console.input("[dim cyan]Enter target URL or IP address: ")
            ps.target = ps.url_to_ip(target)
            lower = console.input("[dim cyan]Enter starting port: ")
            higher = console.input("[dim cyan]Enter upper port: ")
            ps.user_range_ports(lower,higher)
            ps.shuffle_ports()
            ps.run()
            

        if(ps.state == 'h' or ps.state == 'H'):
            with open('./Port Scanner/help.txt') as f:
                contents = f.read()
                print(contents)
                ps.init_main()
        

    #this function run to us port_Scan function with threadpool
    def run(ps):
        if(ps.state == '1'):
            threadpool(ps.port_scan, ps.input_ports, len(ps.input_ports))
            ps.scan_flag_complete = 1
            ps.display_results()
        if(ps.state == '2'):
            threadpool(ps.port_scan, ps.ports_vulnerability.keys(), len(ps.ports_vulnerability.keys()))
            ps.scan_flag_complete = 1
        if(ps.state == '3'):
            threadpool(ps.port_scan, ps.input_ports, len(ps.input_ports))
            ps.scan_flag_complete = 1
            ps.read_from_db()
            ps.display_results()
        

    def is_scan_started(ps):
        if ps.scan_flag_start == 1:
            ps.scan_started = 1
            ps.report_message.append("Scan is started - target is public")
        else:
            ps.report_message.append("Scan failed - private target")

    def is_scan_detected(ps):
        if ps.scan_flag_complete == 1:
            ps.scan_completed = 1
            ps.report_message.append("Scan is undetected - scan is done")
        else:
            ps.report_message.append("Undetected scan failed - target detected the scan")

    def is_open_ports_found(ps):
        threshold = 4
        if len(ps.open_ports) > threshold:
            ps.counter_open_ports = len(ps.open_ports)
            ps.report_message.append("Open ports above threshold found")
        else:
            ps.report_message.append("Failed to find open ports above the threshold")
    
    def execute_tests(ps):
        ps.is_scan_started()
        ps.is_scan_detected()
        ps.is_open_ports_found()
        ps.is_ports_vulnerable()
        ps.security_score()

    def is_ports_vulnerable(ps):
        vulnerable_ports_bulk = ["20","21","22","139","137","445","53","443","80","8080","8443","23","25","69"]
        counter = 0
        for port in vulnerable_ports_bulk:
            #print(int(port))
            if (port) in str(ps.open_ports):
                ps.common_unsecure_ports.append(port)
                counter = counter+1
        if counter > 0 :
            ps.vulnerable_ports_found = 1
            ps.report_message.append("Vulnerable open ports found")
        else:
            ps.report_message.append("Failed to find vulnerable ports")
    
    def security_score(ps):
        threshold = 4
        if ps.scan_started == 1:
            ps.final_score = ps.final_score + 3
        if ps.scan_completed == 1:
            ps.final_score = ps.final_score + 4
        if ps.counter_open_ports >threshold:
            ps.final_score = ps.final_score + 5
        if ps.vulnerable_ports_found == 1:
            ps.final_score = ps.final_score + (len(ps.common_unsecure_ports) * 2)
    
    def final_results(ps):
        test_cases = ["SCANNABLE TARGET","UNDETECTED PORT SCAN","FOUND OPEN PORTS ABOVE TRESHOLD", "FOUND VULNERABLE PORTS"]
        color_type = ""
        risk_type = ""
        counter = 0

        if ps.final_score == 0:
            color_score = "green"
            risk_type = "Low"
        elif ps.final_score > 0 and ps.final_score < 6:
            color_score = "yellow"
            risk_type = "Medium"
        else:
            color_score = "red"
            risk_type = "High"
        art = text2art("Results",font='small',chr_ignore=True)
        print(art)
        console.print(f"[+] Your final secuirty score is:[{color_score}]{ps.final_score}[/{color_score}] Risk:[{color_score}]{risk_type}[/{color_score}]")
        print()
        console.print(f"Target is : {ps.target_url}")
        console.print(f"Target IP is : {ps.target}")
        console.print(f"Target host is: {socket.gethostbyaddr(ps.target)[0]}")
        console.print(f"Total ports scanned :{len(ps.ports_vulnerability.keys())}")
        console.print(f"Total open ports found :{ps.open_ports}")
        console.print(f"Total vulnerable ports found: {ps.common_unsecure_ports}")
        print()
        console.print("[magenta]Test cases:[/magenta]")

        console.print("Secuirty tests:", style="bold blue")
        table = Table(show_header=True, header_style="bold green")
        table.add_column("TEST CASE", justify="left", style="cyan", no_wrap=True)
        table.add_column("STATUS", justify="left", style="cyan", no_wrap=True)
        table.add_column("SUCCESS", justify="left", style="red", no_wrap=True)
        for report,case in zip(ps.report_message,test_cases): ## need to add database with the vulnerability of the ports
            if "failed" in report.lower():
                success_type = "V"
                table.add_row(str(case), str(report), f"[green]{success_type}[/green]")
            else:
                success_type = "X"
                table.add_row(str(case), str(report), f"[red]{success_type}[/red]")
        console.print(table)
        print()
        console.print(f"Scan Results :")
        ps.display_results()

        

if __name__ == "__main__":
    port_scan = port_scanner()
    port_scan.init_main()