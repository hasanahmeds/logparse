from contextlib import contextmanager
from pathlib import Path
import sys
from typing import Iterator, TextIO

@contextmanager
def open_input(path: str) -> Iterator[TextIO]:
    if path == "-":
        yield sys.stdin
    else:
        with Path(path).open("rt", encoding="utf-8", errors="strict") as stream:
            yield stream

def lines(stream: TextIO) -> Iterator[tuple[int, str]]:
    for number, line in enumerate(stream, 1):
        yield number, line
