from io import StringIO
import json
import pytest
from logparse.config import Config
from logparse.pipeline import analyze
from logparse.cli import main
from test_pipeline import LINE

@pytest.mark.parametrize("value", [True, 0, -1, 1001, "5"])
def test_invalid_top_paths(value):
    with pytest.raises(ValueError):
        Config(top_paths=value)

def test_unknown_config(tmp_path):
    path=tmp_path/"config.json";path.write_text('{"unknown":1}')
    with pytest.raises(ValueError):
        Config.load(path)

def test_empty():
    report=analyze([("empty",StringIO())],Config())
    assert report["requests"]==report["lines"]==0
    assert report["error_rate"]==0.0
    assert report["top_paths"]==[]

def test_multiple_files():
    report=analyze([("a",StringIO(LINE)),("b",StringIO(LINE))],Config())
    assert report["requests"]==2

def test_stdin(monkeypatch,capsys):
    monkeypatch.setattr("sys.stdin",StringIO(LINE))
    assert main(["-"])==0
    assert json.loads(capsys.readouterr().out)["requests"]==1
