import pytest
from logparse.config import Config
from logparse.metrics import Metrics
from logparse.models import LogRecord
from logparse.timestamps import iso_timestamp

def test_metrics_and_path_cap():
    metrics = Metrics(Config(max_paths=1))
    for path, status in [("/a?secret=1", 200), ("/b", 500), ("/a?secret=2", 404)]:
        metrics.add(LogRecord(iso_timestamp("2025-01-02T12:00:00Z"), "GET", path, status, 10))
    report = metrics.report()
    assert report["requests"] == 3
    assert report["error_rate"] == pytest.approx(2/3)
    assert report["bytes_sent"] == 30
    assert report["top_paths"] == [{"path":"/a", "requests":2}]
    assert report["untracked_path_requests"] == 1
    assert report["hours_utc"] == {"12":3}
    assert report["statuses"] == {"200":1,"404":1,"500":1}

def test_server_errors_only():
    m = Metrics(Config(error_status=500))
    m.add(LogRecord(iso_timestamp("2025-01-02T00:00:00Z"), "GET", "/", 404, 0))
    assert m.report()["errors"] == 0
