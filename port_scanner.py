import socket
import json
import sys

class port_scanner:
    
    PORTS_TO_SCAN = "./common_ports.json"

    #Init our ps struct, including target, which ports are open, and the vulnerabilities
    def __init__(ps):
        ps.target = "" # The host we scan
        ps.open_ports = [] # collecting open ports
        ps.ports_vulnerability = {} # collecting vulnerability information
    
    #Extracting data from json file to our struct
    def read_from_json(ps):
        with open(port_scanner.PORTS_TO_SCAN, "r") as file:
            data = json.load(file)
        #print(data)
        ps.ports_vulnerability = {int(k): v for (k, v) in data.items()}

    #Check every port that given with the host, if the connection succeeded, we append it on our struck of open ports
    def port_scan(ps, port):
            #find the best time out to catch all the open ports
        #AF_INET represent domain or IP ipv4 address , sock_stream is the default
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try: # we try to establish connection
            conn_status = sock.connect_ex((ps.target, port))
            if conn_status == 0:
                ps.open_ports.append(port)
            sock.close()
        except:
            pass

