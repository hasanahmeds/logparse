"""Run from the repository root: python scripts/benchmark.py --count 100000"""
import argparse
from io import StringIO
from pathlib import Path
import sys
import time
import tracemalloc
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from logparse.config import Config
from logparse.pipeline import analyze

class RepeatedStream:
    def __init__(self, count: int):
        self.remaining = count
    def readline(self, size: int = -1) -> str:
        if self.remaining <= 0:
            return ""
        self.remaining -= 1
        return 'host - - [02/Jan/2025:10:00:00 +0000] "GET /health HTTP/1.1" 200 12\n'

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count",type=int,default=100000)
    args=parser.parse_args()
    if args.count < 1:
        parser.error("count must be positive")
    tracemalloc.start()
    start=time.perf_counter()
    report=analyze([("synthetic",RepeatedStream(args.count))],Config())
    elapsed=time.perf_counter()-start
    peak=tracemalloc.get_traced_memory()[1]
    print(f"requests={report['requests']} seconds={elapsed:.3f} requests_per_second={args.count/elapsed:.1f} peak_bytes={peak}")

if __name__=="__main__":
    main()
