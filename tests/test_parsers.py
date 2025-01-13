import json
import pytest
from logparse.parsers import parse_line

BASE = {"timestamp": "2025-01-02T10:00:00Z", "method": "GET", "path": "/a", "status": 200}

def test_json_defaults():
    record = parse_line(json.dumps(BASE))
    assert record.bytes_sent == 0
    assert record.status == 200

@pytest.mark.parametrize("field,value", [("status", True), ("status", 600), ("bytes", -1),
                                         ("method", ""), ("path", None), ("timestamp", 3)])
def test_invalid_schema(field, value):
    with pytest.raises(ValueError):
        parse_line(json.dumps({**BASE, field: value}), "json")

def test_apache_common_and_combined():
    prefix = 'host - - [02/Jan/2025:10:00:00 +0000] "GET /x HTTP/1.1" 404 -'
    for suffix in ["", ' "-" "Browser"']:
        record = parse_line(prefix + suffix)
        assert (record.status, record.bytes_sent, record.path) == (404, 0, "/x")

@pytest.mark.parametrize("line", ["", "nonsense", "{}", "[]", '{"status":200}'])
def test_reject_bad_lines(line):
    with pytest.raises(ValueError):
        parse_line(line)
