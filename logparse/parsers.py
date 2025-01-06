import json
from .models import LogRecord
from .timestamps import iso_timestamp

def parse_json(line: str) -> LogRecord:
    data = json.loads(line)
    if not isinstance(data, dict):
        raise ValueError("JSON line must be an object")
    try:
        return LogRecord(iso_timestamp(data["timestamp"]), data["method"],
                         data["path"], data["status"], data.get("bytes", 0))
    except (KeyError, TypeError) as exc:
        raise ValueError("invalid JSON log schema") from exc

import re
from .timestamps import apache_timestamp

APACHE = re.compile(
    r'^\S+ \S+ \S+ \[([^\]]+)\] "([A-Za-z]+) ([^" ]+) HTTP/[^" ]+" '
    r'(\d{3}) (\d+|-)(?: "[^"\\]*(?:\\.[^"\\]*)*" "[^"\\]*(?:\\.[^"\\]*)*")?\s*$')

def parse_apache(line: str) -> LogRecord:
    match = APACHE.fullmatch(line.strip())
    if not match:
        raise ValueError("not an Apache common/combined access log")
    stamp, method, path, status, size = match.groups()
    return LogRecord(apache_timestamp(stamp), method, path, int(status),
                     0 if size == "-" else int(size))

def parse_line(line: str, format: str = "auto") -> LogRecord:
    if format not in {"auto", "json", "apache"}:
        raise ValueError("unknown input format")
    if format == "auto":
        format = "json" if line.lstrip().startswith("{") else "apache"
    return parse_json(line) if format == "json" else parse_apache(line)
