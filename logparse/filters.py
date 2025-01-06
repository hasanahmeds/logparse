from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlsplit
from .models import LogRecord

@dataclass(frozen=True)
class Filters:
    since: datetime | None = None
    until: datetime | None = None
    path_prefix: str = ""

    def __post_init__(self) -> None:
        for value in (self.since, self.until):
            if value is not None and (value.tzinfo is None or value.utcoffset() is None):
                raise ValueError("filter timestamps need timezones")
        if self.since and self.until and self.since > self.until:
            raise ValueError("since must not be after until")

    def accepts(self, record: LogRecord) -> bool:
        return ((self.since is None or record.timestamp >= self.since)
                and (self.until is None or record.timestamp < self.until)
                and urlsplit(record.path).path.startswith(self.path_prefix))
