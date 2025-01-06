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

def lines(stream: TextIO) -> Iterator[tuple[int, str]]:
    for number, line in enumerate(stream, 1):
        yield number, line
