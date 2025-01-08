from collections import Counter
from .config import Config
from .models import LogRecord

class Metrics:
    def __init__(self, config: Config):
        self.config = config
        self.statuses = Counter()
        self.methods = Counter()
        self.requests = 0
        self.errors = 0
        self.bytes_sent = 0

    def add(self, record: LogRecord) -> None:
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
                "methods": dict(sorted(self.methods.items()))}
