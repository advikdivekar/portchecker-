import subprocess
import time
from datetime import datetime
from pathlib import Path
import csv

TARGETS = ["google.com", "openai.com"]

TEST_CASES = [
    {"workers": 50, "timeout": 2},
    {"workers": 100, "timeout": 2},
    {"workers": 200, "timeout": 2},
    {"workers": 100, "timeout": 4},
    {"workers": 300, "timeout": 4},
    {"workers": 500, "timeout": 4},
]

PORT_START = 1
PORT_END = 1024

SCANNER_CMD = ["python3", "cli-threaded/port-scannerv3.py"]  # adjust if needed

RESULTS_FILE = Path("results/benchmarks.csv")
RESULTS_FILE.parent.mkdir(exist_ok=True)

if not RESULTS_FILE.exists():
    with open(RESULTS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp","lang","impl","workers","timeout_s",
            "start_port","end_port","target",
            "total_time_s"
        ])

for target in TARGETS:
    for case in TEST_CASES:
        print(f"\nRunning: {target} | Workers={case['workers']} | Timeout={case['timeout']}")

        cmd = SCANNER_CMD + [
            target,
            "-s", str(PORT_START),
            "-e", str(PORT_END),
            "-w", str(case["workers"]),
            "-t", str(case["timeout"])
        ]

        start = time.time()
        subprocess.run(cmd)
        end = time.time()

        duration = round(end - start, 4)

        with open(RESULTS_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                "python",
                "threaded",
                case["workers"],
                case["timeout"],
                PORT_START,
                PORT_END,
                target,
                duration
            ])

print("\nAll Python benchmarks completed.")