from dataclasses import dataclass, fields
import json
from pathlib import Path

@dataclass(frozen=True)
class Config:
    error_status: int = 400
    top_paths: int = 10
    max_paths: int = 10000

    def __post_init__(self) -> None:
        if type(self.error_status) is not int or not 400 <= self.error_status <= 599:
            raise ValueError("error_status must be 400..599")
        if type(self.top_paths) is not int or not 1 <= self.top_paths <= 1000:
            raise ValueError("top_paths must be 1..1000")
        if type(self.max_paths) is not int or not 1 <= self.max_paths <= 1000000:
            raise ValueError("max_paths must be 1..1000000")

    @classmethod
    def load(cls, path: Path) -> "Config":
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or set(data) - {f.name for f in fields(cls)}:
            raise ValueError("configuration must be an object with known keys")
        return cls(**data)
