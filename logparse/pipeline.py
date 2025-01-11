import logging
from typing import Iterable, TextIO
from .config import Config
from .filters import Filters
from .metrics import Metrics
from .parsers import parse_line
from .reader import lines

LOGGER = logging.getLogger(__name__)

def analyze(streams: Iterable[tuple[str, TextIO]], config: Config,
            filters: Filters = Filters(), format: str = "auto", strict: bool = False) -> dict:
    metrics = Metrics(config)
    total = blank = malformed = filtered = 0
    for source, stream in streams:
        for number, line in lines(stream):
            total += 1
            if not line.strip():
                blank += 1
                continue
            try:
                record = parse_line(line, format)
                accepted = filters.accepts(record)
            except (ValueError, OverflowError) as exc:
                malformed += 1
                if strict:
                    raise ValueError(f"{source}:{number}: malformed log record") from exc
                if malformed <= 5:
                    LOGGER.warning("%s:%d: skipped malformed record", source, number)
                continue
            if accepted:
                metrics.add(record)
            else:
                filtered += 1
    return {"schema_version": 1, "lines": total, "blank_lines": blank,
            "malformed_lines": malformed, "filtered_records": filtered, **metrics.report()}
