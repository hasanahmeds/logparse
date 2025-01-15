import csv
from io import StringIO
from logparse.reports import write_csv

def test_formula_cells():
    stream=StringIO()
    write_csv({"top_paths":[{"path":"=2+2","requests":1}]},stream)
    rows=list(csv.reader(StringIO(stream.getvalue())))
    assert rows[1][1]=="'=2+2"
