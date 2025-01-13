import csv
import json
from io import StringIO
from pathlib import Path
from logparse.cli import main

EXAMPLES = Path(__file__).resolve().parents[1]/"examples"

def test_json_cli(capsys):
    assert main([str(EXAMPLES/"access.log")]) == 0
    result=json.loads(capsys.readouterr().out)
    assert result["requests"] == 3
    assert result["errors"] == 2

def test_csv_cli(capsys):
    assert main([str(EXAMPLES/"access.log"),"--format","csv"]) == 0
    rows=list(csv.reader(StringIO(capsys.readouterr().out)))
    assert rows[0]==["section","key","value"]
    assert ["summary","requests","3"] in rows

def test_config(capsys):
    assert main([str(EXAMPLES/"access.log"),"--config",str(EXAMPLES/"config.json")])==0
    assert json.loads(capsys.readouterr().out)["errors"]==1

def test_missing_file(tmp_path):
    assert main([str(tmp_path/"absent")])==2

def test_duplicate_stdin():
    assert main(["-","-"])==2
