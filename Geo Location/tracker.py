import json
import requests
import argparse
from rich.console import Console
from rich.table import Table
from art import *
import pandas as pd
import re
'''
Geo Location tracker is responsible to give us information about URL or
IP address, we get the informaption from public API and represent it to the user
in easy way to understand.
This step of gathering information is important to build profile on the target that
you want to attack.
If theres information about the company on the API it add the risk complexity on the 
risk algorithm calculation
import pandas as pd
'''
## Everything is ok - Else - Data that not need to be published and it is published
## search email patterns of company
console=Console()

class tracker:
    def __init__(tracker):
        '''
        Init varibales that we will use in the code
        '''
        tracker.state = ""
        tracker.api = ""
        tracker.target = ""
        tracker.get_response = ""
        tracker.create_json =""

        #scoring tests
        tracker.all_params = "" 
        tracker.all_domains = ""
        
    @staticmethod
    def entry_message():
        '''
        Entry message with logo and menu
        The user will choose the current option that he want
        to perform his brute force
        In addition he can also import passwords list by himself
        or check for information by pressing H
        We MAKE PRETTY LOGO ASWELL
        '''
        art_font = text2art("Tracker",font='cybermedium',chr_ignore=True)
        console.print(f"[bold red]{art_font}[/bold red]")
        console.print("#" * 55, style="bold green")
        console.print("#"*12,"Tracker", "#"*12,style="dim cyan")
        console.print("#"*11,"Gather information about your target", "#"*11,style="dim cyan")
        console.print("#"*11,"Use social engineering to abuse it", "#"*11,style="dim cyan")
        console.print("")
        console.print("#" * 55, style="bold green")
        print()
        console.print("[+]For help press - H")
        console.print("[+]For gathering information - 1")

    def sublist3r_services(tracker): #### this one is good  
        tracker.get_response = requests.get("https://api.sublist3r.com/search.php?domain={tracker.target}")
        tracker.create_json = json.loads(tracker.get_response.content)
        print(tracker.create_json5)
    def certsh_services(target):
        tracker.get_response = requests.get("https://crt.sh/?q=%25.{tracker.target}")
    def threat_crowd_services(target):
        tracker.get_response = requests.get('https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={tracker.target}')
        #tracker.create_json = json.loads(tracker.get_response.content)
        #out_file = open("info.json" , 'w')
        #json.dump(tracker.create_json, out_file,indent = 6)
    def ip_api_services(target):
        tracker.target = tracker.api + tracker.target
    def netcraft_services(tracker):
        tracker.get_response = requests.get('https://searchdns.netcraft.com/?restriction=site+ends+with&host={tracker.target}')
    def virustotal_services(tracker):
        tracker.get_response = requests.get("https://www.virustotal.com/ui/domains/{tracker.target}/subdomains")
    def parse_json(target):
        tracker.get_response = requests.get(tracker.target)
        tracker.create_json = json.loads(tracker.get_response.content)
        out_file = open("info.json" , 'w')
        json.dump(tracker.create_json, out_file,indent = 6)
    
    def init_main(target):
        tracker.api = "http://ip-api.com/json/"
        tracker.entry_message()
        console.print("Please enter your option from menu : ")
        tracker.state = input()
        if tracker.state == '1':
            tracker.target = input("Enter target")
            tracker.ip_api_services(tracker)
            tracker.parse_json(tracker)
            print(tracker.create_json)
        if tracker.state == '2':
            tracker.target = input("Enter target")
            tracker.netcraft_services(tracker)
            print(tracker.get_response.text)
        if tracker.state == '3':
            tracker.target = input("Enter target")
            tracker.virustotal_services(tracker)
            print(tracker.get_response.text)
        if tracker.state == '4':
            tracker.target = input("Enter target")
            tracker.threat_crowd_services(tracker)
            print(tracker.get_response.text)
        if tracker.state =='5':
            tracker.target = input("enter target")
            tracker.sublist3r_services(tracker)
            print(tracker.get_response)





            #tracker.json_to_csv(tracker)

if __name__ == "__main__":
    track = tracker()
    track.init_main()