# Port Scanner Benchmark Results

Target: scanme.nmap.org
Runs per test: 3

## v1_sequential

### Run 1

- Return code: 0
- Time (s): 287.93
- STDOUT:
```
Enter target IP: Resolved IP: 45.33.32.156

 scanning 45.33.32.156. Wait for the Scan completion
Scanning ports 1-1024

[+] Port 22 is OPEN
[+] Port 80 is OPEN

Scan Complete
Open Ports: [22, 80]
Time taken: 287.46 seconds
```

### Run 2

- Return code: 0
- Time (s): 287.32
- STDOUT:
```
Enter target IP: Resolved IP: 45.33.32.156

 scanning 45.33.32.156. Wait for the Scan completion
Scanning ports 1-1024

[+] Port 22 is OPEN
[+] Port 80 is OPEN

Scan Complete
Open Ports: [22, 80]
Time taken: 287.26 seconds
```

### Run 3

- Return code: 0
- Time (s): 289.64
- STDOUT:
```
Enter target IP: Resolved IP: 45.33.32.156

 scanning 45.33.32.156. Wait for the Scan completion
Scanning ports 1-1024

[+] Port 22 is OPEN
[+] Port 80 is OPEN

Scan Complete
Open Ports: [22, 80]
Time taken: 289.58 seconds
```

## v2_threaded_worker_pool

### Run 1

- Return code: 0
- Time (s): 3.16
- STDOUT:
```
Enter target IP: Resolved IP: 45.33.32.156

Scanning 45.33.32.156 ...
Scanning ports 1–1024 with 100 threads

[+] Port 22 is OPEN
[+] Port 80 is OPEN

Scan Complete
Open Ports: [22, 80]
Time taken: 3.08 seconds
```

### Run 2

- Return code: 0
- Time (s): 3.88
- STDOUT:
```
Enter target IP: Resolved IP: 45.33.32.156

Scanning 45.33.32.156 ...
Scanning ports 1–1024 with 100 threads

[+] Port 22 is OPEN
[+] Port 80 is OPEN

Scan Complete
Open Ports: [22, 80]
Time taken: 3.82 seconds
```

### Run 3

- Return code: 0
- Time (s): 3.66
- STDOUT:
```
Enter target IP: Resolved IP: 45.33.32.156

Scanning 45.33.32.156 ...
Scanning ports 1–1024 with 100 threads

[+] Port 22 is OPEN
[+] Port 80 is OPEN

Scan Complete
Open Ports: [22, 80]
Time taken: 3.6 seconds
```

## v3_cli_threaded

### Run 1

- Return code: 0
- Time (s): 2.93
- STDOUT:
```
Scanning scanme.nmap.org
Ports: 1-1024
Threads: 100
Timeout: 1.0s

[+] Port 22 is OPEN
[+] Port 80 is OPEN

Scan Complete
Open Ports: [22, 80]
Time taken: 2.86 seconds
```

### Run 2

- Return code: 0
- Time (s): 2.9
- STDOUT:
```
Scanning scanme.nmap.org
Ports: 1-1024
Threads: 100
Timeout: 1.0s

[+] Port 22 is OPEN
[+] Port 80 is OPEN

Scan Complete
Open Ports: [22, 80]
Time taken: 2.83 seconds
```

### Run 3

- Return code: 0
- Time (s): 3.16
- STDOUT:
```
Scanning scanme.nmap.org
Ports: 1-1024
Threads: 100
Timeout: 1.0s

[+] Port 22 is OPEN

Scan Complete
Open Ports: [22]
Time taken: 3.09 seconds
```
