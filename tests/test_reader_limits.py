from io import StringIO
import pytest
from logparse.reader import lines, MAX_LINE_CHARS

def test_line_limit():
    with pytest.raises(ValueError, match="exceeds"):
        list(lines(StringIO("x"*(MAX_LINE_CHARS+1))))

def test_unterminated_last_line():
    assert list(lines(StringIO("first\nlast"))) == [(1,"first\n"),(2,"last")]
