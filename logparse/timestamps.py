from datetime import datetime, timezone
import re

MONTHS = {name: i for i, name in enumerate(
    "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}

def iso_timestamp(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError("timestamp requires an explicit timezone")
    return result.astimezone(timezone.utc)

def apache_timestamp(value: str) -> datetime:
    match = re.fullmatch(r"(\d{2})/([A-Za-z]{3})/(\d{4}):(\d{2}:\d{2}:\d{2}) ([+-]\d{2})(\d{2})", value)
    if not match or match[2] not in MONTHS:
        raise ValueError("invalid Apache timestamp")
    day, month, year, clock, hour, minute = match.groups()
    return iso_timestamp(f"{year}-{MONTHS[month]:02d}-{day}T{clock}{hour}:{minute}")
