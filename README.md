# logparse

A Python 3.10+ CLI for streaming HTTP access logs into JSON or CSV reports. Runtime dependencies: Python standard library only. This is a reconstructed educational development history assigned to January 2–19, 2025.

## Ubuntu quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e . -r requirements-dev.txt
python -m pytest -q
logparse examples/access.log
```

Without installing the package, run `python3 -m logparse examples/access.log` from this repository. JSON output for the three-line Apache fixture has 3 requests, 2 errors, 46 bytes and error_rate 2/3. All fixtures are synthetic.

## CLI examples

```bash
mkdir -p reports
python3 -m logparse examples/access.log --format csv --output reports/summary.csv
python3 -m logparse examples/access.log --config examples/config.json
python3 -m logparse examples/access.jsonl --input-format json --strict
python3 -m logparse examples/access.log --since 2025-01-02T10:00:00Z --until 2025-01-02T11:00:00Z
python3 -m logparse examples/access.log --path-prefix /checkout
cat examples/access.log | python3 -m logparse -
gzip -c examples/access.log > reports/access.log.gz
python3 -m logparse reports/access.log.gz examples/access.jsonl
python3 scripts/generate_logs.py --count 1000 --seed 42 > reports/synthetic.jsonl
python3 -m logparse reports/synthetic.jsonl
python3 scripts/benchmark.py --count 100000
```

`--input-format`: auto (per-line default), json or apache. `--format`: json or csv. `--output`: report path; otherwise stdout. `--config`: JSON config. `--strict`: abort on the first malformed nonblank record. `--verbose`: debug logging. `--version`: installed version. Multiple paths are accepted; stdin `-` may appear once. Logs ending in .gz are streamed through gzip.

Exit 0 means completed; exit 2 means argument, input, decoding, validation or output error. Tolerant mode skips malformed records, counts them and warns about only the first five. Blank lines are counted separately. A missing file, corrupt gzip, invalid UTF-8 or oversized line aborts regardless of strict mode. Diagnostics go to stderr; report data goes to stdout or the output file.

## Accepted data

JSON Lines: one object per physical line, with timestamp (ISO-8601, explicit timezone), method (letters), path (nonempty string), status (integer 100–599), and optional bytes (nonnegative integer, default zero). Additional fields are ignored. JSON arrays and multiline JSON documents are not supported. Boolean values are not valid numeric fields.

Example:
```json
{"timestamp":"2025-01-02T10:00:00Z","method":"GET","path":"/health","status":200,"bytes":12}
```

Apache common/combined access logs support the standard quoted METHOD TARGET HTTP/version request, English three-letter month and numeric timezone. `-` response sizes become zero. Nonstandard formats, application stack traces and multiline messages are not parsed. Configure servers to emit the documented structure.

Timestamps normalize to UTC. `--since` is inclusive and `--until` exclusive. Naive timestamps are rejected. Query strings are removed for path filtering and aggregation. Records excluded by filters are counted separately and excluded from the error-rate denominator.

## Reports and configuration

Default errors are statuses >=400. Example config changes this to >=500:
```json
{"error_status":500,"top_paths":5,"max_paths":10000}
```
Unknown config keys and invalid values fail. error_status: integer 400–599; top_paths: integer 1–1000; max_paths: integer 1–1000000.

JSON schema_version 1 reports lines, blank_lines, malformed_lines, filtered_records, requests, errors, error_rate (fraction 0–1), bytes_sent, statuses, methods, hours_utc, top_paths and untracked_path_requests. Empty selections yield zero requests and zero rate. CSV uses section,key,value rows for the same metrics. hours_utc means hour-of-day pooled across all dates.

Top-path tracking is capped and first-seen: a later frequent path can remain untracked once the cap fills. Raise max_paths when accurate rankings across more distinct paths matter. Details: docs/architecture.md. This tool does not infer unique users or sessions and does not redact all personal data.

## Docker

```bash
docker build -t logparse:local .
docker run --rm -v "$PWD/examples:/data:ro" logparse:local /data/access.log
cat examples/access.log | docker run --rm -i logparse:local -
```

The container runs as non-root UID 10001. Input mounts must be readable. To save results, redirect stdout on the host or mount a writable output directory with suitable permissions. CI tests Python 3.10–3.12 and builds the image. Local Docker execution depends on an installed Docker engine.

## Publish to GitHub

After generating this repository with the supplied version-2 backdate engine, create an empty GitHub repository named logparse (no README/license initialization). From the generated repository replace YOUR_USERNAME:

```bash
git remote add origin https://github.com/YOUR_USERNAME/logparse.git
git push -u origin main
```

Use your own Git identity when replaying the manifest. Do not force-push to an existing history. These commands do not create a GitHub repository automatically. Source/tests, packaging, CLI and reports are the final project; the manifest and backdate engine are external orchestration files.
