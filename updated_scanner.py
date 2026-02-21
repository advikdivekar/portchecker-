import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((target, port))
            if result == 0:
                return port
    except:
        pass
    return None

#checkpoint 1 

def main():
    target = input("Enter target IP: ")

    print(f"\nScanning {target} ...")
    print("Scanning ports 1–1024 with 100 threads\n")

    start_time = time.time()
    open_ports = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_port, target, port) for port in range(1, 1025)]

        for future in as_completed(futures):
            result = future.result()
            if result:
                print(f"[+] Port {result} is OPEN")
                open_ports.append(result)

#checkpoint 2 

    end_time = time.time()

    print("\nScan Complete")
    print("Open Ports:", sorted(open_ports))
    print("Time taken:", round(end_time - start_time, 2), "seconds")


if __name__ == "__main__":
    main()

#checkpoint 3
