"""Usage: python scripts/generate_logs.py --count 1000 > synthetic.jsonl"""
import argparse
from datetime import datetime, timedelta, timezone
import json
import random

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.count < 0:
        parser.error("count must be nonnegative")
    rng = random.Random(args.seed)
    start = datetime(2025, 1, 2, tzinfo=timezone.utc)
    for index in range(args.count):
        print(json.dumps({"timestamp": (start + timedelta(seconds=index)).isoformat(),
                          "method": rng.choice(["GET", "POST"]),
                          "path": rng.choice(["/health", "/products", "/checkout"]),
                          "status": rng.choices([200, 404, 500], weights=[90, 7, 3])[0],
                          "bytes": rng.randint(0, 4096)}))

if __name__ == "__main__":
    main()
