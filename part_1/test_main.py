import os
import csv
from unittest.mock import patch
import pytest
from main import saveData, readData, settleDebts

def test_saveDataCreatesFile(tmpdir):
    filepath = tmpdir.join("test_output.csv")
    data = [["a", "b", "1"], ["c", "d", "2"]]
    saveData(filepath, data)
    assert os.path.isfile(filepath)


def test_saveDataNoWriteAccess(tmpdir):
    filepath = tmpdir.join("test_output.csv")
    data = [["a", "b", "1"], ["c", "d", "2"]]
    with patch("os.access", return_value=False):
        with pytest.raises(PermissionError):
            saveData(filepath, data)


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


def test_readDataValidFile():
    filepath = "test_data/debts_3.csv"
    expected = [["Jacek", "Dominik", "10"],
                ["Dominik", "Jacek", "5"],
                ["Kasia", "Dominik", "5"],
                ["Michał", "Kamil", "13"]]
    data = readData(filepath)
    assert data == expected
    

def test_readDataNoReadAccess():
    filepath = "test_data/debts_3.csv"
    with patch("os.access", return_value=False):
        with pytest.raises(PermissionError):
            readData(filepath)


def test_readDataEmptyFile(tmpdir):
    filepath = tmpdir.join("empty.csv")
    with open(filepath, "w", newline='') as csvfile:
        pass
    data = readData(filepath)
    assert data == []


def test_readDataInvalidFile():
    filepath = "test_data/File_DoesNoT_Exist.csv"
    with pytest.raises(FileNotFoundError):
        data = readData(filepath)
    

def test_settleDebtsNoData():
    data = []
    output = settleDebts(data)
    assert output == []


def test_settleDebtsSignleDebt():
    data = [["Jacek", "Dominik", "10"]]
    expected = [["Dominik", "Jacek", "10"]]
    output = settleDebts(data)
    assert output == expected


def test_settleDebtsMultipleDebts():
    data = [["Jacek", "Dominik", "10"],
            ["Dominik", "Jacek", "5"],
            ["Kasia", "Dominik", "5"],
            ["Michał", "Kamil", "13"]]
    expected = [["Kamil", "Michał", "13"],
                ["Dominik", "Kasia", "5"],
                ["Dominik", "Jacek", "5"]]
    output = settleDebts(data)
    assert output == expected


def test_settleDebtsNoOneOwes():
    data = [["Jacek", "Dominik", "10"],
            ["Dominik", "Jacek", "10"]]
    output = settleDebts(data)
    assert output == []
