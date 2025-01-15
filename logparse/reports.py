import json
from typing import TextIO

def write_json(report: dict, stream: TextIO) -> None:
    json.dump(report, stream, indent=2, sort_keys=True, ensure_ascii=False)
    stream.write("\n")

import csv

def write_csv(report: dict, stream: TextIO) -> None:
    writer = csv.writer(stream)
    writer.writerow(["section", "key", "value"])
    for key, value in report.items():
        if isinstance(value, dict):
            for label, count in value.items():
                writer.writerow([key, label, count])
        elif key == "top_paths":
            for item in value:
                writer.writerow([key, safe_cell(item["path"]), item["requests"]])
        else:
            writer.writerow(["summary", key, value])

def safe_cell(value: str) -> str:
    if value.lstrip().startswith(("=", "+", "-", "@")) or value.startswith(("\t", "\r", "\n")):
        return "'" + value
    return value
