from contextlib import contextmanager
from pathlib import Path
import gzip
import sys
from typing import Iterator, TextIO

@contextmanager
def open_input(path: str) -> Iterator[TextIO]:
    if path == "-":
        yield sys.stdin
    else:
        opener = gzip.open if path.endswith(".gz") else open
        with opener(path, "rt", encoding="utf-8", errors="strict") as stream:
            yield stream


MAX_LINE_CHARS = 1_048_576

def lines(stream: TextIO) -> Iterator[tuple[int, str]]:
    number = 0
    while True:
        line = stream.readline(MAX_LINE_CHARS + 1)
        if not line:
            return
        number += 1
        if len(line) > MAX_LINE_CHARS:
            raise ValueError(f"line {number} exceeds {MAX_LINE_CHARS} characters")
        yield number, line
