import socket
import sys

class port_scanner:

    #Init our ps struct, including target, which ports are open, and the vulnerabilities
    def __init__(ps):
        ps.target = "" # The host we scan
        ps.open_ports = [] # collecting open ports
        ps.ports_vulnerability = {} # collecting vulnerability information
    
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

