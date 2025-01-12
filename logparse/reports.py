import json
from typing import TextIO

def write_json(report: dict, stream: TextIO) -> None:
    json.dump(report, stream, indent=2, sort_keys=True, ensure_ascii=False)
    stream.write("\n")
