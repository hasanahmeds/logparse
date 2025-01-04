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
