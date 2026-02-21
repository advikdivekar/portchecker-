import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((target, port))
            if result == 0:
                return port
    except:
        pass
    return None

#checkpoint 1 
