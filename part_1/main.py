import os
import csv
from typing import List

def _fileExists(filepath: str) -> bool:
    return os.path.isfile(filepath)

def readData(filepath: str) -> List[List[str]]:
    if not _fileExists(filepath):
        raise FileNotFoundError(f"File '{filepath}' does not exist.")
    
    with open(filepath, newline='') as csvfile:
        data = csv.reader(csvfile)
        data = list(data)
    
    return data

def main():
    filepath = "test_data/debts.csv"
    readData(filepath)

if __name__ == "__main__":
    main()
