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

#checkpoint 1 


def main(): 
    target = input("Enter target IP: ")

    print(f"\n scanning {target}. Wait for the Scan completion")
    print("Scanning ports 1-1024\n")

    start_time = time.time()
    open_ports = []

    for port in range(1, 1025):
        if scan_port(target, port):
            print(f"[+] Port {port} is OPEN")
            open_ports.append(port)

#checkpoint 2 

    end_time = time.time()

    print("\nScan Complete")
    print("Open Ports:", open_ports)
    print("Time taken:", round(end_time - start_time, 2), "seconds")


if __name__ == "__main__":
    main()

#checkpoint 3