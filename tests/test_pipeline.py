import gzip
from io import StringIO
import pytest
from logparse.config import Config
from logparse.filters import Filters
from logparse.pipeline import analyze
from logparse.reader import open_input

LINE = '{"timestamp":"2025-01-02T10:00:00Z","method":"GET","path":"/x","status":500}\n'

def test_tolerant_counts():
    report = analyze([("test",StringIO(LINE+"bad\n\n"))], Config())
    assert report["requests"] == report["malformed_lines"] == report["blank_lines"] == 1
    assert report["lines"] == 3

def test_strict_location():
    with pytest.raises(ValueError, match="fixture:2"):
        analyze([("fixture",StringIO(LINE+"bad\n"))],Config(),strict=True)

def test_filtered_denominator():
    report=analyze([("test",StringIO(LINE))],Config(),Filters(path_prefix="/other"))
    assert report["requests"] == 0
    assert report["filtered_records"] == 1
    assert report["error_rate"] == 0.0

def test_gzip(tmp_path):
    path=tmp_path/"input.gz"
    with gzip.open(path,"wt",encoding="utf-8") as f:
        f.write(LINE)
    with open_input(str(path)) as stream:
        assert analyze([("gzip",stream)],Config())["errors"]==1
