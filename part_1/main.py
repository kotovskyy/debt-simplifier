import os
import csv
from typing import List, Tuple

def getArguments() -> Tuple[str]:
    import argparse
    parser = argparse.ArgumentParser(
        prog="DebtSimplifier",
        description="A tool to simplify debts between a group of people"
    )
    parser.add_argument("data_path", type=str, help="Path to the CSV file containing the data")
    parser.add_argument("output_path", type=str, help="Path to the CSV file where the output will be saved")
    args = parser.parse_args()
    return (args.data_path, args.output_path)
    

def _fileExists(filepath: str) -> bool:
    return os.path.isfile(filepath)


def readData(filepath: str) -> List[List[str]]:
    if not _fileExists(filepath):
        raise FileNotFoundError(f"File '{filepath}' does not exist.")
    
    with open(filepath, newline='') as csvfile:
        data = csv.reader(csvfile)
        data = list(data)
    
    return data

def saveData(filepath: str, data: List[List[str]]):
    dirpath = os.path.dirname(filepath)
    if not os.path.isdir(dirpath):
        raise FileNotFoundError(f"Directory '{dirpath}' does not exist.")
    if not os.access(dirpath, os.W_OK):
        raise PermissionError(f"No write access to directory '{dirpath}'.")
    
    with open(filepath, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
        

def _initPersonTotal(data: List[List[str]]) -> dict:
    person_total = {}
    for receiver, payer, amount in data:
        person_total[receiver] = person_total.get(receiver, 0) + int(amount)
        person_total[payer] = person_total.get(payer, 0) - int(amount)
    return person_total


def settleDebts(data: List[List[str]]):
    person_total = _initPersonTotal(data)
    people = sorted(person_total, key=lambda x: person_total[x])
    totals = [person_total[p] for p in people]
    return _settleDebts(people, totals)


def _findSettlements(people: List[str], totals: List[int], i: int):
    settlements = []
    for j in range(len(people)-1, i, -1):
        if totals[j] > 0:
            transactionAmount = min(-totals[i], totals[j])
            totals[i] += transactionAmount
            totals[j] -= transactionAmount
            settlements.append([people[i], people[j], str(transactionAmount)])
            if totals[i] == 0:
                break
    return settlements


def _settleDebts(people: List[str], totals: List[int]):
    settlements = []
    for i in range(len(people)):
        if totals[i] < 0:
            settlements.extend(_findSettlements(people, totals, i))
    return settlements


def main():
    data_path, output_path = getArguments()
    data = readData(data_path)
    output = settleDebts(data)
    saveData(output_path, output)


if __name__ == "__main__":
    main()
