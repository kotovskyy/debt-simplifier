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
    filepath = getArguments()
    data = readData(filepath)
    output = settleDebts(data)


if __name__ == "__main__":
    main()
