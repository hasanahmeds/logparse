from contextlib import contextmanager
import os
from pathlib import Path
import tempfile
from typing import Iterator, TextIO

@contextmanager
def atomic_output(path: Path) -> Iterator[TextIO]:
    descriptor, name = tempfile.mkstemp(prefix=".logparse-", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
            yield stream
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
