import subprocess
import time
from pathlib import Path

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

RUNS_PER_TEST = 3
TARGET = "scanme.nmap.org"

TESTS = [
    {
        "name": "v1_sequential",
        "cmd": ["python3", "sequential/scanner.py"],
        "interactive": True,
        "input": f"{TARGET}\n",
    },
    {
        "name": "v2_threaded_worker_pool",
        "cmd": ["python3", "threaded-worker-pool/updated_scanner.py"],
        "interactive": True,
        "input": f"{TARGET}\n",
    },
    {
        "name": "v3_cli_threaded",
        "cmd": ["python3", "cli-threaded/port-scannerv3.py", TARGET, "-s", "1", "-e", "1024", "-t", "100", "--timeout", "1"],
        "interactive": False,
        "input": "",
    },
]

def run_once(test):
    start = time.time()
    if test["interactive"]:
        p = subprocess.run(test["cmd"], input=test["input"], text=True, capture_output=True)
    else:
        p = subprocess.run(test["cmd"], text=True, capture_output=True)
    end = time.time()
    return {
        "returncode": p.returncode,
        "stdout": p.stdout.strip(),
        "stderr": p.stderr.strip(),
        "seconds": round(end - start, 2),
    }

def main():
    lines = []
    lines.append("# Port Scanner Benchmark Results\n")
    lines.append(f"Target: {TARGET}")
    lines.append(f"Runs per test: {RUNS_PER_TEST}\n")

    for t in TESTS:
        lines.append(f"## {t['name']}\n")
        for i in range(1, RUNS_PER_TEST + 1):
            r = run_once(t)
            lines.append(f"### Run {i}\n")
            lines.append(f"- Return code: {r['returncode']}")
            lines.append(f"- Time (s): {r['seconds']}")
            if r["stderr"]:
                lines.append(f"- STDERR:\n```\n{r['stderr']}\n```")
            lines.append(f"- STDOUT:\n```\n{r['stdout']}\n```\n")

    out = RESULTS_DIR / "bench_results.md"
    out.write_text("\n".join(lines))
    print(f"Saved: {out}")

if __name__ == "__main__":
    main()