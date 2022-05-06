
from io import StringIO
from bs4 import BeautifulSoup
from pkg_resources import find_distributions
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
        crawl.copy_subdomain_list = ""
        crawl.subdomain_list_content = ""
        crawl.urls = []
        crawl.state = ""

        #scoring tests
        crawl.crawling_subodmain_success = 0
        crawl.crawling_urls_scan_success = 0
        crawl.vulnerable_subdomains_found = 0
        crawl.vulnerable_urls_found = 0

    def parse_data(crawl):
        crawl.copy_subdomain_list = crawl.subdomain_list.read()
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
            try:
                requests.get(url)
            except requests.ConnectionError:
                pass
            else:
                #print(f"Discovered subdomain : :{url}" )
                crawl.found_subdomains.append(url)
        for u in crawl.found_subdomains:
            print("[+]URL - " + u)
    
    def find_directories_current_page(crawl):
        response = requests.get(crawl.target)
        soup = BeautifulSoup(response.text,"html.parser")
        for link in soup.find_all("a"):
            data = link.get("href")
            crawl.urls.append(data)
            print(data)

    def init_main(crawl):
        crawl.entry_message()
        crawl.state = input("Please enter you crawl option :")
        crawl.get_target()
        
        if crawl.state == '1':
            crawl.find_subdomains()
        elif crawl.state == '2':
            crawl.find_directories_current_page()
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
        #crawl.find_subdomains()
        crawl.find_directories_current_page()


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