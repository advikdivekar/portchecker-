# TCP Port Scanner – Comparative Study (Python)

## What we built
We implemented three versions of a TCP connect port scanner:
- v1: sequential (single-thread)
- v2: threaded worker pool (fixed configuration)
- v3: CLI tool (configurable threads/timeout/port-range)

## How a TCP connect scan works
A TCP connect scan attempts a full TCP handshake to determine if a service is listening on a port.
- Open: SYN → SYN-ACK → ACK (connect succeeds)
- Closed: RST returned quickly (connect fails fast)
- Filtered: no response (connect waits until timeout)

## Why sequential was slow
Sequential scans suffer from timeout stacking: each filtered port can consume the full timeout before moving on.
Total time ≈ number_of_ports × timeout (worst case).

## Why threading was faster
Threading overlaps I/O waiting. Multiple connection attempts wait concurrently, so timeouts do not stack linearly.
Total time ≈ (number_of_ports / workers) × timeout (rough estimate).

## Important pitfalls observed
- Trailing whitespace in hostnames breaks DNS resolution (e.g., "scanme.nmap.org ").
- Very low timeouts can cause false negatives on real networks.
- Very high concurrency can trigger rate limiting or packet drops.

## Results
See: results/bench_results.md

## Limitations
- TCP connect scan is noisier and more detectable than SYN scan.
- No UDP scanning.
- No service fingerprinting (yet).

## Ethics
Scanning should only be performed on systems you own or have explicit permission to test.