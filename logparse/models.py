from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class LogRecord:
    timestamp: datetime
    method: str
    path: str
    status: int
    bytes_sent: int

    def __post_init__(self) -> None:
        if self.timestamp.tzinfo is None or self.timestamp.utcoffset() is None:
            raise ValueError("timestamp must have a timezone")
        if type(self.status) is not int or not 100 <= self.status <= 599:
            raise ValueError("status must be an integer between 100 and 599")
        if type(self.bytes_sent) is not int or self.bytes_sent < 0:
            raise ValueError("bytes must be a nonnegative integer")
        if not isinstance(self.method, str) or not self.method.isalpha():
            raise ValueError("method must contain letters")
        if not isinstance(self.path, str) or not self.path:
            raise ValueError("path must be a nonempty string")
