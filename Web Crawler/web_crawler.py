
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
        crawl.found_subdomains = []
        crawl.subdomain_list = open("./Web Crawler/subdomains_list.txt")
        crawl.admin_list = open("./Web Crawler/admin_list.txt")
        crawl.directories_list = open("./Web Crawler/admin_list.txt")
        crawl.copy_directories_list =""
        crawl.directories_list_content =""
        crawl.copy_subdomain_list = ""
        crawl.subdomain_list_content = ""
        crawl.copy_admin_list = ""
        crawl.admin_list_content = ""
        crawl.urls = []
        crawl.state = ""

        #scoring tests
        crawl.crawling_subodmain_success = 0
        crawl.crawling_urls_scan_success = 0
        crawl.vulnerable_subdomains_found = 0
        crawl.vulnerable_urls_found = 0


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
        console.print("[+]For page directories scan - 2")
        console.print("[+]For recursive directories scan - 3")
        console.print("[+]Import your own subdomains list - 4")
    
    def export_information(crawl):
        df = pd.DataFrame(columns=['url'],data=crawl.urls)
        df.to_csv('results_urls.csv')

    def find_subdomains(crawl):
        crawl.parse_data()
        for subdomain in crawl.subdomain_list_content:
            url = (f"http://{subdomain}.{crawl.target}")
            #print("URL = "+ url)
            try:
                requests.get(url)
            except requests.exceptions.ConnectionError:
                pass
            else:
                #print(f"Discovered subdomain : :{url}" )
                crawl.found_subdomains.append(url)
        # for u in crawl.found_subdomains:
        #     print("[+]URL - " + u)

    def robots_page_check(crawl):
        try:
            req = requests.get(crawl.target + '/robots.txt')
            if '<html>' in req.text:
                print("Robots.txt not found")
            else:
                print("Robots.txt found. Check for findings")
                print(req.text)
        except:
            print("Robots.txt not found")

    def find_urls_current_page(crawl):
        response = requests.get(crawl.target)
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
                print("Discovered URL: "+url)

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
                print("Discovered URL: "+url)
            
            
            # else:
            #     print("request link = "+url)


            
    def display_subdomain_results(crawl):
        for domain in crawl.found_subdomains:
            console.print(domain)
            print("--------------------")   
    def display_urls_results(crawl):
        for link in crawl.urls:
            console.print(link)
            print("--------------------")

    def init_main(crawl):
        crawl.entry_message()
        crawl.state = input("Please enter you crawl option :")
        crawl.get_target()
        
        crawl.robots_page_check()
        #crawl.find_admin_login_page()
        #crawl.find_directories()

        if crawl.state == '1':
            crawl.find_subdomains()
            crawl.display_subdomain_results()
        elif crawl.state == '2':
            crawl.find_urls_current_page()
            crawl.display_urls_results()
            crawl.export_information()



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

    
    def get_started(crawl):
        crawl.get_target()
        crawl.robots_page_check()
        #crawl.find_subdomains()
        #crawl.find_urls_current_page()


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