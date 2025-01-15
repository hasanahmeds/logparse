from logparse.cli import main

def test_same_file_is_protected(tmp_path):
    path=tmp_path/"input.log"; path.write_text("keep")
    assert main([str(path),"--output",str(path)])==2
    assert path.read_text()=="keep"

def test_config_is_protected(tmp_path):
    path=tmp_path/"config.json"; path.write_text('{}')
    source=tmp_path/"empty.log"; source.write_text('')
    assert main([str(source),'--config',str(path),'--output',str(path)])==2
    assert path.read_text()=='{}'
