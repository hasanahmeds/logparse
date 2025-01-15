import pytest
from logparse.output import atomic_output

def test_failure_preserves_old_report(tmp_path):
    path=tmp_path/"report.json"; path.write_text("old")
    with pytest.raises(RuntimeError):
        with atomic_output(path) as stream:
            stream.write("partial")
            raise RuntimeError("failure")
    assert path.read_text()=="old"
    assert list(tmp_path.iterdir())==[path]

def test_success_replaces_report(tmp_path):
    path=tmp_path/"report.json"
    with atomic_output(path) as stream:
        stream.write("new")
    assert path.read_text()=="new"
