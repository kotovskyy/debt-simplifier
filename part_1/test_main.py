import os
import csv
import pytest
from main import saveData

def test_saveDataCreatesFile(tmpdir):
    filepath = tmpdir.join("test_output.csv")
    data = [["a", "b", "1"], ["c", "d", "2"]]
    saveData(filepath, data)
    assert os.path.isfile(filepath) 

def test_saveDataNoParentDir(tmpdir):
    filepath = tmpdir.join("test/test_output.csv")
    data = [["a", "b", "1"], ["c", "d", "2"]]
    with pytest.raises(FileNotFoundError):
        saveData(filepath, data)
        
def test_saveDataSuccess(tmpdir):
    filepath = tmpdir.join("test_output.csv")
    expected = [["a", "b", "1"], ["c", "d", "2"]]
    saveData(filepath, expected)
    with open(filepath, newline='') as csvfile:
        data = csv.reader(csvfile)
        data = list(data)
    assert data == expected
