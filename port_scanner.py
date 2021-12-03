import threading
import socket


#Target
target = "google.com"

#port scanner
def port_scan(port):
    soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # TCP
    soc.settimeout(0.5)#timeout to establish that connection failed
    try:
        connection = soc.connect((target,port))
        print("Port Open",port)
        connection.close()
    except:
        pass

def main():
    r = 1
    for x in range(1,2000):
        t = threading.Thread(target = port_scan,kwargs={'port':r})
        r = r + 1
        t.start()
if __name__ == "__main__":
    main()

