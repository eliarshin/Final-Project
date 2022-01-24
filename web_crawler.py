from io import StringIO
import requests
import re
from urllib.parse import urlparse, urljoin



url = "ynet.co.il"

def request(url):
    try:
        return requests.get("https://"+url)
    except requests.exceptions.ConnectionError:
        pass

def find_subdomains(url):
    with open("./subdomains_list.list", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = word + "." + url
            resp = request(test_url)
            if resp:
                print("[+] subdomain discovered --> " + test_url)

def find_directory(url):
    with open("./subdomains_list.list", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url =  url + "/" + word
            resp = request(test_url)
    
            if resp:
                print("[+] url discovered --> " + test_url)

def links(url):
    resp = requests.get("https://"+url)
    print(resp)
    reg = b'(?:href=")(.*?)"'
    href_links = re.findall( reg, resp.content)
    #href_links.remove("b'")
    for link in href_links:
        #print(link)
        link = urlparse.urljoin(url,link)
        print(link)
links(url)