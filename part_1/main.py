import os
import csv
from typing import List, Tuple

def getArguments() -> str:
    import argparse
    parser = argparse.ArgumentParser(
        prog="DebtSimplifier",
        description="A tool to simplify debts between a group of people"
    )
    parser.add_argument("filepath", type=str, help="Path to the CSV file containing the data")
    args = parser.parse_args()
    return args.filepath
    

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
    filepath = getArguments()
    data = readData(filepath)

if __name__ == "__main__":
    main()
