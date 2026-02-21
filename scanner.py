import socket 
import time 

def scan_port(target, port):
    try: 
        s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2) #wait max 1 seconds 
        result = s.connect_ex((target, port))
        s.close()
        return result == 0
    except: 
        return False

