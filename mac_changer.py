import subprocess
#Information about subprocess library https://docs.python.org/3/library/subprocess.html
'The subprocess help us to run os comands, line by line not threadable'

#Getting the MAC on the computer
output = subprocess.call("getmac", shell=True)
print(output)

'Need to be done - Check which command change the MAC address !'
