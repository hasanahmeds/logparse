from datetime import datetime
import pytest
from logparse.filters import Filters
from logparse.models import LogRecord
from logparse.timestamps import iso_timestamp, apache_timestamp

def test_utc_conversion():
    assert iso_timestamp("2025-01-02T11:00:00+01:00") == iso_timestamp("2025-01-02T10:00:00Z")
    assert apache_timestamp("02/Jan/2025:11:00:00 +0100") == iso_timestamp("2025-01-02T10:00:00Z")

def test_naive_rejected():
    with pytest.raises(ValueError):
        iso_timestamp("2025-01-02T10:00:00")
    with pytest.raises(ValueError):
        Filters(since=datetime(2025,1,2))

def test_half_open_interval():
    stamp = iso_timestamp("2025-01-02T10:00:00Z")
    record = LogRecord(stamp, "GET", "/x?q=1", 200, 0)
    assert Filters(since=stamp, path_prefix="/x").accepts(record)
    assert not Filters(until=stamp).accepts(record)
    assert not Filters(path_prefix="/other").accepts(record)
