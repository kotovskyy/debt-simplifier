import csv
from typing import List

def readData(filepath: str) -> List[List[str]]:
    with open(filepath, newline='') as csvfile:
        data = csv.reader(csvfile)
        data = list(data)
    return data

def main():
    filepath = "test_data/debts_1.csv"
    readData(filepath)

if __name__ == "__main__":
    main()
