import collections
from pickle import TRUE
import socket
import string
import sys
import json
import random
#from turtle import pd
from typing import OrderedDict
from rich.console import Console
from rich.table import Table
from art import *
from threadpool import threadpool
import pandas as pd
import time
import sys
import socket
from tkinter import *
from datetime import datetime
import os


#Things to DO
'1. Add method to scan bulk from user directory'
'2. Edit the help functions'
'3. Find a database that giving information about open ports'


console = Console() ## for pretty write

##the class
class port_scanner:

    PORTS_TO_SCAN = "./Port Scanner/common_ports.json"
    #
    'Add advanced scan , and also choosing by user'
    #
    
    #Init of our struct
    def __init__(ps):
        ################## HERE TESTTTTTTTTTTTTTTTTTTTT ##########@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        ps.root = Tk()
        ps.btn1 = Button(ps.root, text="Built in portscan", command=ps.pinger)
        ps.txt1 =Text(ps.root, width=60)
        ps.lbl1=Label(ps.root, text="Insert IP or Domain >>")
        ps.ent =Entry(ps.root, width=20)
        ################## HERE TESTTTTTTTTTTTTTTTTTTTT ##########@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        ps.target = "" # The host we scan
        ps.open_ports = [] # collecting open ports
        ps.input_ports =[] #input from user
        ps.ports_vulnerability = {} # collecting vulnerability information
        ps.recived_data = {}
        ps.db = ""
        ps.state = "" # which state we are
        ps.service_name=[]
        ps.description=[]

    
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

        #print(ps.service_name)
        #print(ps.description)

                
            
    def create_screen(ps):
        ps.root.title('PT Framework')
        ps.root.geometry("500x500")
        ps.root.resizable(False, False)
        m1c = '#00ee00'
        bgc = '#222222'
        dbg = '#000000'
        fgc = '#111111'
        ps.root.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc, activeForeground=bgc, highlightColor=m1c,
                   highlightBackground=m1c)
        ps.btn1.place(x=420, y=15)
        ps.txt1.place(x=4, y=100)
        ps.lbl1.place(x=2, y=20)
        ps.ent.place(x=150, y=20)
        
        #test = port_scanner.get_data(port_scan)   
        
                


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
                #ps.txt1.insert(END,ps.ports_vulnerability[port]) ################## HERE TESTTTTTTTTTTTTTTTTTTTT ##########@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

            
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
            print(check[0])
        except socket.gaierror as e:
            console.print(f"{e}. Exiting.", style="bold red")
            sys.exit()
        console.print(f"\nIP The IP address of the url is: [bold blue]{ip_addr}[/bold blue]")
        return ip_addr

    #main function - we choose here which option we choose
    def init_main(ps):
        ps.entry_message()
        #ps.read_from_db()
        #ps.create_screen()################## HERE TESTTTTTTTTTTTTTTTTTTTT ##########@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        ps.state = console.input(" Enter your scan option: ")
        if ps.state == '1':
            target = console.input("[dim cyan]Enter target URL or IP address: ")
            ps.target = ps.url_to_ip(target)
            ps.user_range_ports(2,65535)
            ps.shuffle_ports()
            ps.run()

        if ps.state == '2':
            ps.read_from_json()
            target = console.input("[dim cyan]Enter target URL or IP address: ")
            ps.target = ps.url_to_ip(target)
            ps.shuffle_ports()
            ps.run()
            print((ps.recived_data))

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
    
    ################## HERE TESTTTTTTTTTTTTTTTTTTTT ##########@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def pinger(ps):
        ps.create_screen()
        ps.target = ps.url_to_ip(ps.ent.get())
        ps.shuffle_ports()
        ps.state==2
        ps.run()
    ################## HERE TESTTTTTTTTTTTTTTTTTTTT ##########@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # def get_data(ps):
    #     return ps.recived_data
            
        

    #this function run to us port_Scan function with threadpool
    def run(ps):
         if(ps.state == '1'):
             threadpool(ps.port_scan, ps.input_ports, len(ps.input_ports))
             ps.display_results()
         if(ps.state == '2'):
            threadpool(ps.port_scan, ps.ports_vulnerability.keys(), len(ps.ports_vulnerability.keys()))
            ps.display_results()
         if(ps.state == '3'):
             threadpool(ps.port_scan, ps.input_ports, len(ps.input_ports))
             ps.read_from_db()
             ps.display_results()

# class Gui:

#     PORTS_TO_SCAN = "./Port Scanner/common_ports.json"
    
    # def __init__(gui): 
    #     gui.root = Tk()
    #     gui.btn1 = Button(gui.root, text="Built in portscan", command=port_scanner.pinger(port_scan))
    #     gui.txt1 =Text(gui.root, width=60)
    #     gui.lbl1=Label(gui.root, text="Insert IP or Domain >>")
    #     port_scanner.target =Entry(gui.root, width=20)

    # def create_screen(gui):
    #     gui.root.title('PT Framework')
    #     gui.root.geometry("500x500")
    #     gui.root.resizable(False, False)
    #     m1c = '#00ee00'
    #     bgc = '#222222'
    #     dbg = '#000000'
    #     fgc = '#111111'
    #     gui.root.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc, activeForeground=bgc, highlightColor=m1c,
    #                highlightBackground=m1c)
    #     gui.btn1.place(x=420, y=15)
    #     gui.txt1.place(x=4, y=100)
    #     gui.lbl1.place(x=2, y=20)
    #     port_scanner.target.place(x=150, y=20)
    #     #test = port_scanner.get_data(port_scan)
#         #print("here data = ",test)
#         gui.txt1.insert(port_scanner.get_data(port_scan))

#         def url_to_ip(target):
#             try:
#                 ip_addr = socket.gethostbyname(target)
#                 check = socket.gethostbyaddr(ip_addr)
#                 print(check[0])
#             except socket.gaierror as e:
#                 console.print(f"{e}. Exiting.", style="bold red")
#                 sys.exit()
#             console.print(f"\nIP The IP address of the url is: [bold blue]{ip_addr}[/bold blue]")
#             return ip_addr
        
#         def run(gui):
#             threadpool(gui.port_scan, gui.ports_vulnerability.keys(), len(gui.ports_vulnerability.keys()))



if __name__ == "__main__":
    # gui = Gui()
    # gui.create_screen()
    port_scan = port_scanner()
    port_scan.init_main()
    port_scan.root.mainloop()