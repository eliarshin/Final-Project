
from io import StringIO
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urlparse
from urllib.parse import urljoin

class web_crawler:
    def __init__(crawl):
        crawl.target = ""
        crawl.found_subdomains = []
        crawl.subdomain_list = open("./Web Crawler/subdomains_list.txt")
        crawl.copy_subdomain_list = ""
        crawl.subdomain_list_content = ""
        crawl.urls = []

    def parse_data(crawl):
        crawl.copy_subdomain_list = crawl.subdomain_list.read()
        crawl.subdomain_list_content = crawl.copy_subdomain_list.splitlines()

    def get_target(crawl):
        crawl.target = input("Enter your target :")
    
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
    network_scan.get_started()

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