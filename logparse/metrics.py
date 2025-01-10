from collections import Counter
from datetime import timezone
from urllib.parse import urlsplit
from .config import Config
from .models import LogRecord

class Metrics:
    def __init__(self, config: Config):
        self.config = config
        self.paths = Counter()
        self.other_paths = 0
        self.hours = Counter()
        self.statuses = Counter()
        self.methods = Counter()
        self.requests = 0
        self.errors = 0
        self.bytes_sent = 0

    def add(self, record: LogRecord) -> None:
        path = urlsplit(record.path).path or "/"
        if path in self.paths or len(self.paths) < self.config.max_paths:
            self.paths[path] += 1
        else:
            self.other_paths += 1
        self.hours[f"{record.timestamp.astimezone(timezone.utc).hour:02d}"] += 1
        self.statuses[str(record.status)] += 1
        self.methods[record.method.upper()] += 1
        self.requests += 1
        self.errors += int(record.status >= self.config.error_status)
        self.bytes_sent += record.bytes_sent

    def report(self) -> dict:
        return {"requests": self.requests, "errors": self.errors,
                "error_rate": self.errors / self.requests if self.requests else 0.0,
                "bytes_sent": self.bytes_sent,
                "statuses": dict(sorted(self.statuses.items())),
                "methods": dict(sorted(self.methods.items())),
                "hours_utc": dict(sorted(self.hours.items())),
                "top_paths": [{"path": p, "requests": n} for p, n in
                              sorted(self.paths.items(), key=lambda x: (-x[1], x[0]))[:self.config.top_paths]],
                "untracked_path_requests": self.other_paths}
