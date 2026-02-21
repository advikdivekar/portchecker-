import socket
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(target, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            if result == 0:
                return port
    except:
        pass
    return None


def main():
    parser = argparse.ArgumentParser(description="Simple TCP Port Scanner")

    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("--timeout", type=float, default=0.5, help="Timeout in seconds (default: 0.5)")

    args = parser.parse_args()

    print(f"\nScanning {args.target}")
    print(f"Ports: {args.start}-{args.end}")
    print(f"Threads: {args.threads}")
    print(f"Timeout: {args.timeout}s\n")

    start_time = time.time()
    open_ports = []

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [
            executor.submit(scan_port, args.target, port, args.timeout)
            for port in range(args.start, args.end + 1)
        ]

        for future in as_completed(futures):
            result = future.result()
            if result:
                print(f"[+] Port {result} is OPEN")
                open_ports.append(result)

    end_time = time.time()

    print("\nScan Complete")
    print("Open Ports:", sorted(open_ports))
    print("Time taken:", round(end_time - start_time, 2), "seconds")


if __name__ == "__main__":
    main()