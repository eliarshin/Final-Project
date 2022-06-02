
from io import StringIO
from bs4 import BeautifulSoup
from pkg_resources import find_distributions
import urllib.request
import requests
import re
from urllib.parse import urlparse 
from urllib.parse import urljoin
from rich.console import Console
from art import *
from rich.table import Table
import pandas as pd

console = Console()
class web_crawler:

    def __init__(crawl):
        crawl.target = ""
        
        crawl.subdomain_list = open("./Web Crawler/subdomains_list.txt")
        crawl.admin_list = open("./Web Crawler/admin_list.txt")
        crawl.directories_list = open("./Web Crawler/admin_list.txt")
        crawl.copy_directories_list =""
        crawl.directories_list_content =""
        crawl.copy_subdomain_list = ""
        crawl.subdomain_list_content = ""
        crawl.copy_admin_list = ""
        crawl.admin_list_content = ""
        crawl.state = ""


        #Arrays to save the found values.
        crawl.found_subdomains = []
        crawl.found_robots = ""
        crawl.urls = []
        crawl.found_directories = []
        crawl.found_admin_login_pages = []
        crawl.report_message = []

        #scoring tests
        crawl.vulnerable_subdomains_found = 0
        crawl.vulnerable_urls_found = 0
        crawl.vulnerable_admin_pages_found = 0
        crawl.vulnerable_directories_found = 0
        crawl.vulnerable_robots_txt_found = 0 
        crawl.final_score = 0 

    def final_results(crawl):
        test_cases = ["ADMIN PAGE SCAN","DIRECTORIES SCAN","ROBOTS.TXT SCAN", "URLS SCAN","SUBDOMAINS SCAN"]
        color_type = ""
        risk_type = ""
        counter = 0

        if crawl.final_score == 0:
            color_score = "green"
            risk_type = "Low"
        elif crawl.final_score > 0 and crawl.final_score < 6:
            color_score = "yellow"
            risk_type = "Medium"
        else:
            color_score = "red"
            risk_type = "High"

        art = text2art("Results",font='small',chr_ignore=True)
        print(art)
        console.print(f"[+] Your final secuirty score is:[{color_score}]{crawl.final_score}[/{color_score}] Risk:[{color_score}]{risk_type}[/{color_score}]")
        print()
        console.print(f"[+] Your target is:[bold red]{crawl.target}[/bold red]")
        console.print("[magenta]Test cases:[/magenta]")
        console.print("Secuirty tests:", style="bold blue")
        table = Table(show_header=True, header_style="bold green")
        table.add_column("TEST CASE", justify="left", style="cyan", no_wrap=True)
        table.add_column("STATUS", justify="left", style="cyan", no_wrap=True)
        table.add_column("SUCCESS", justify="left", style="red", no_wrap=True)
        for report,case in zip(crawl.report_message,test_cases): ## need to add database with the vulnerability of the ports
            if "did not" in report.lower():
                success_type = "V"
                table.add_row(str(case), str(report), f"[green]{success_type}[/green]")
            else:
                success_type = "X"
                table.add_row(str(case), str(report), f"[red]{success_type}[/red]")
        console.print(table)


    def security_score(crawl):
        if crawl.vulnerable_admin_pages_found > 0:
            crawl.final_score = crawl.final_score + crawl.vulnerable_admin_pages_found
            crawl.report_message.append("ADMIN PAGES FOUND")
        else:
            crawl.report_message.append("ADMIN MESSAGE DID NOT FOUND")
        if crawl.vulnerable_directories_found > 0:
            crawl.final_score = crawl.final_score + crawl.vulnerable_directories_found
            crawl.report_message.append("SUSPICIOUS DIRECTORIES FOUND")
        else:
            crawl.report_message.append("SUSPICIOUS DIRECTORIES DID NOT FOUND")
        if crawl.vulnerable_robots_txt_found > 0:
            crawl.final_score = crawl.final_score + crawl.vulnerable_robots_txt_found
            crawl.report_message.append("ROBOTS.TXT PAGE FOUND")
        else:
            crawl.report_message.append("ROBOTS.TXT DID NOT FOUND")
        if crawl.vulnerable_urls_found > 0:
            crawl.final_score = crawl.final_score + crawl.vulnerable_urls_found
            crawl.report_message.append("VULNERABLE URLS FOUND")
        else:
            crawl.report_message.append("VULNERABLE URLS DID NOT FOUND")
        if crawl.vulnerable_subdomains_found > 0:
            crawl.final_score = crawl.final_score + crawl.vulnerable_subdomains_found
            crawl.report_message.append("VULNERABLE SUBDOMAINS FOUND")
        else:
            crawl.report_message.append("VULNERABLE SUBDOMAINS DID NOT FOUND")

    def test_robots(crawl):
        if "not found" not in crawl.found_robots:
            crawl.vulnerable_robots_txt_found = 1

    def test_directories(crawl):
        danger_directories = ['../','ssh','ftp','lib','.txt','.tar','.tgz','.zip'
        ,'asp','.azure-piplines.yml','babel','config']
        found_directories =[]
        for subdomain in danger_directories:
            for found_directory in crawl.found_directories:
                if subdomain in found_directory:
                    found_directories.append("[+]Domain is = "+found_directory+"\n [+]Subdomain is = "+subdomain)
        if len(found_directories) > 0:
            crawl.vulnerable_directories_found = len(found_directories)
        art = text2art("Directories",font='small',chr_ignore=True)
        print(art)
        for i in found_directories:
            print(i)

    def test_admin_page(crawl):
        danger_admin_endings = ['cpanel','admin','administrator','wp','wp-login','wp-admin',
        'suser','editor','server','sql']
        found_admin_urls = []
        for subdomain in danger_admin_endings:
            for found_url in crawl.found_admin_login_pages:
                if subdomain in found_url:
                    found_admin_urls.append("[+]Domain is = "+found_url+"\n [+]Subdomain is = "+subdomain)
        if len(found_admin_urls) > 0:
            crawl.vulnerable_admin_pages_found = len(found_admin_urls)
        art = text2art("Admin Pages",font='small',chr_ignore=True)
        print(art)
        for i in found_admin_urls:
            print(i)

    def test_urls(crawl):
        danger_urls = ['admin','payments','billing','.xml','../','news','direct','ssh','8080',
        'script','db','dir','bot']
        found_danger_urls = []
        for subdomain in danger_urls:
            for found_url in crawl.urls:
                if subdomain in found_url:
                    found_danger_urls.append("[+]Domain is = "+found_url+"\n [+]Subdomain is = "+subdomain)
        if len(found_danger_urls) > 0:
            crawl.vulnerable_urls_found = len(found_danger_urls)
        art = text2art("URL's",font='small',chr_ignore=True)
        print(art)
        for i in found_danger_urls:
            print(i)

    def test_subdomains(crawl):
        danger_subdomains =['admin','access','adm','administrator','asset','invoice','billing',
        'billings','bot','bug','ftp','db','css','dir','doc','www']
        found_danger_subdomains = []
        for subdomain in danger_subdomains:
            for found_domain in crawl.found_subdomains:
                if subdomain in found_domain:
                    found_danger_subdomains.append("[+]Domain is = "+found_domain+"\n [+]Subdomain is = "+subdomain)
        if len(found_danger_subdomains) > 0:
            crawl.vulnerable_subdomains_found = len(found_danger_subdomains)
        art = text2art("Subdomains",font='small',chr_ignore=True)
        print(art)
        for i in found_danger_subdomains:
            print(i)


    def parse_data(crawl):
        crawl.copy_subdomain_list = crawl.subdomain_list.read()
        crawl.copy_directories_list = crawl.directories_list.read()
        crawl.copy_admin_list = crawl.admin_list.read()
        crawl.directories_list_content = crawl.copy_directories_list.splitlines()
        crawl.admin_list_content = crawl.copy_admin_list.splitlines()
        crawl.subdomain_list_content = crawl.copy_subdomain_list.splitlines()

    def get_target(crawl):
        crawl.target = input("Enter your target :")

    @staticmethod
    def entry_message():
        art_font = text2art("Web Crawler",font='cybermedium',chr_ignore=True)
        console.print(f"[bold red]{art_font}[/bold red]")
        console.print("#" * 55, style="bold green")
        console.print("#"*12,"Web crawler", "#"*12,style="dim cyan")
        console.print("#"*11,"A Wide Range of Crawling Options", "#"*11,style="dim cyan")
        console.print("#" * 55, style="bold green")
        print()
        console.print("[+]For help press - H")
        console.print("[+]For Subdomains scan - 1")
        console.print("[+]For URL page scan - 2")
        console.print("[+]For Admin page scan - 3")
        console.print("[+]For directories page scan - 4")
        console.print("[+]For robots.txt page scan - 5")

    
    def export_information(crawl):
        df = pd.DataFrame(columns=['url'],data=crawl.urls)
        df.to_csv('results_urls.csv')

    def find_subdomains(crawl):
        crawl.parse_data()
        for subdomain in crawl.subdomain_list_content:
            url = (f"http://{subdomain}.{crawl.target}")
            #print(url)
            #print("URL = "+ url)
            try:
                requests.get(url)
            except requests.exceptions.ConnectionError:
                pass
            else:
                print(f"Discovered subdomain : :{url}" )
                crawl.found_subdomains.append(url)
        # for u in crawl.found_subdomains:
        #     print("[+]URL - " + u)

    def robots_page_check(crawl):
        try:
            req = requests.get(crawl.target + '/robots.txt')
            if '<html>' in req.text:
                print("Robots.txt not found")
                crawl.found_robots = "Robots.txt not found"
            else:
                crawl.found_robots = req.text
                print("Robots.txt found. Check for findings")
                print(req.text)
        except:
            print("Robots.txt not found")

    def find_urls_current_page(crawl):
        response = requests.get("http://"+crawl.target)
        soup = BeautifulSoup(response.text,"html.parser")
        for link in soup.find_all("a"):
            #print(f"{link.get('href')} -> {link.text}")
            #data = link.get("href")
            crawl.urls.append(f"{link.get('href')} -> {link.text}")
            #print(data)

    def find_directories(crawl):
        crawl.parse_data()
        for directory in crawl.directories_list_content:
            url = (f"http://{crawl.target}/{directory}")
            try:
                resp = requests.get(url)
            except requests.exceptions.ConnectionError:
                pass
            if resp:
                crawl.found_directories.append("Discovered URL: "+url)
                #print("Discovered URL: "+url)

    def find_admin_login_page(crawl):
        crawl.parse_data()
        for admin_link in crawl.admin_list_content:
            url = (f"http://{crawl.target}/{admin_link}")
            #req = requests.get(url)
            try:
                resp = requests.get(url)
            except requests.exceptions.ConnectionError:
                pass
            if resp:
                crawl.found_admin_login_pages.append("Discovered URL: "+url)
                #print("Discovered URL: "+url)
            
            
            # else:
            #     print("request link = "+url)


    def display_robots_results(crawl):
         print(crawl.found_robots)       
    def display_subdomain_results(crawl):
        for domain in crawl.found_subdomains:
            console.print(domain)
            print("--------------------")   
    def display_urls_results(crawl):
        for link in crawl.urls:
            console.print(link)
            print("--------------------")
    def display_admin_login_results(crawl):
        for link in crawl.found_admin_login_pages:
            console.print(link)
            print("--------------------")
    def display_directories_results(crawl):
        for link in crawl.found_directories:
            console.print(link)
            print("--------------------")

    def init_main(crawl):
        crawl.entry_message()
        crawl.state = input("Please enter you crawl option :")
        crawl.get_target()
        #crawl.robots_page_check()
        #crawl.find_admin_login_page()
        #crawl.find_directories()

        if crawl.state == '1':
            crawl.find_subdomains()
            crawl.display_subdomain_results()
            crawl.test_subdomains()
            crawl.security_score()
            crawl.final_results()
        elif crawl.state == '2': ## this is the right way to show
            crawl.find_urls_current_page()
            crawl.display_urls_results()
            crawl.test_urls()
            crawl.security_score()
            crawl.final_results()
            #crawl.export_information()
        elif crawl.state == '3':
            crawl.find_admin_login_page()
            crawl.display_admin_login_results()
            crawl.test_admin_page()
            crawl.security_score()
            crawl.final_results()
        elif crawl.state == '4':
            crawl.find_directories()
            crawl.display_directories_results()
            crawl.test_directories()
            crawl.security_score()
            crawl.final_results()
        elif crawl.state == '5':
            crawl.robots_page_check()
            crawl.display_robots_results()
            crawl.test_robots()
            crawl.security_score()
            crawl.final_results()



        # get_site = requests.get(crawl.target)
        # soup = BeautifulSoup(get_site.text,"lxml")

        # for i in soup.find_all("a"):
        #     href = i.attrs['href']
        #     if href.startswith("/"):
        #         crawl.target = crawl.target + href
        #         if crawl.target not in crawl.urls:
        #             crawl.urls.append(crawl.target) 
        #             print(crawl.target)
        #             crawl.find_directories_current_page()


if __name__ == "__main__":
    network_scan = web_crawler()
    network_scan.init_main()

# url = "ynet.co.il"

# def request(url):
#     try:
#         return requests.get("https://"+url)
#     except requests.exceptions.ConnectionError:
#         pass

# def find_subdomains(url):
#     with open("./subdomains_list.list", "r") as wordlist_file:
#         for line in wordlist_file:
#             word = line.strip()
#             test_url = word + "." + url
#             resp = request(test_url)
#             if resp:
#                 print("[+] subdomain discovered --> " + test_url)

# def find_directory(url):
#     with open("./subdomains_list.list", "r") as wordlist_file:
#         for line in wordlist_file:
#             word = line.strip()
#             test_url =  url + "/" + word
#             resp = request(test_url)
    
#             if resp:
#                 print("[+] url discovered --> " + test_url)

# def links(url):
#     resp = requests.get("https://"+url)
#     print(resp)
#     reg = b'(?:href=")(.*?)"'
#     href_links = re.findall( reg, resp.content)
#     #href_links.remove("b'")
#     for link in href_links:
#         #print(link)
#         link = urlparse.urljoin(url,link)
#         print(link)
# links(url)