# Architecture and resource behavior

Input files/stdin → bounded line reader → auto/explicit parser → validated UTC record → filters → metrics → JSON/CSV writer.
Only one input file is open at a time. No request records are retained. Paths are tracked up to max_paths; new paths beyond the cap contribute to untracked_path_requests. Top paths are exact only among the retained first-seen paths; this is not a heavy-hitter approximation. Method and status counters are small for conventional HTTP traffic. Hour buckets aggregate hour-of-day across dates, not chronological hourly time series.

The line reader caps individual decoded lines at 1,048,576 characters. Oversized lines and decoding errors abort even in tolerant mode. Path-query strings are removed before aggregation, but paths themselves may contain identifiers; review reports before sharing.

JSON output preserves raw path strings; CSV prefixes formula-like path values with an apostrophe. File output uses a temporary file and atomic replacement. Existing reports can be replaced; input and config files are protected. The parent output directory must exist. Strict parse failures occur before writing a report.

Run python scripts/benchmark.py --count 100000 to measure your environment. The benchmark synthesizes lines on demand and reports throughput and tracemalloc peak allocations; it makes no hardware-independent performance guarantee.
