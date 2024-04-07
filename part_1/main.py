import os
import csv
from typing import List, Tuple


def getArguments() -> Tuple[str]:
    """
    Get command line arguments.

    Returns:
        - `Tuple[str]`: A tuple containing the data path and output path provided as command line arguments.
    """
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
    """
    Check if a file exists at the given filepath.

    Args:
        - `filepath: str` - The path to the file.

    Returns:
        - `bool` - True if the file exists, False otherwise.
    """
    return os.path.isfile(filepath)


def readData(filepath: str) -> List[List[str]]:
    """
    Reads data from a CSV file and returns it as a list of lists (rows).

    Args:
        - `filepath: str` - The path to the CSV file.

    Returns:
        - `List[List[str]]` - The data read from the CSV file as a list of lists.
    """
    if not _fileExists(filepath):
        raise FileNotFoundError(f"File '{filepath}' does not exist.")
    
    with open(filepath, newline='') as csvfile:
        data = csv.reader(csvfile)
        data = list(data)
    
    return data

def saveData(filepath: str, data: List[List[str]]) -> None:
    """
    Save data to a CSV file.

    Args:
        - `filepath: str` - The path to the CSV file.
        - `data: List[List[str]]` - The data to be saved.

    Raises:
        - `FileNotFoundError` - If the directory of the filepath does not exist.
        - `PermissionError` - If there is no write access to the directory of the filepath.
    """
    dirpath = os.path.dirname(filepath)
    if not os.path.isdir(dirpath):
        raise FileNotFoundError(f"Directory '{dirpath}' does not exist.")
    if not os.access(dirpath, os.W_OK):
        raise PermissionError(f"No write access to directory '{dirpath}'.")
    
    with open(filepath, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
        

def _initPersonTotal(data: List[List[str]]) -> dict:
    """
    Initializes and returns a dictionary containing the total amount owed
    ("+" amount sign) or paid ("-" amount sign) by each person.

    Args:
        - `data: List[List[str]]` - A list of lists containing receiver, payer, and amount.

    Returns:
        - `dict` - A dictionary where the keys are the names of the persons 
        involved and the values are the total amounts owed or paid by each person.
    """
    person_total = {}
    for receiver, payer, amount in data:
        person_total[receiver] = person_total.get(receiver, 0) + int(amount)
        person_total[payer] = person_total.get(payer, 0) - int(amount)
    return person_total


def settleDebts(data: List[List[str]]) -> List[List[str]]:
    """
    Settles debts among a group of people based on the given data.

    Args:
        - `data: List[List[str]]` - A list of lists representing the debt data.

    Returns:
        - `List[List[str]]` - A list of lists representing the settled debts. 
    """
    person_total = _initPersonTotal(data)
    people = sorted(person_total, key=lambda x: person_total[x])
    totals = [person_total[p] for p in people]
    return _settleDebts(people, totals)


def _findSettlements(people: List[str], totals: List[int], i: int) -> List[List[str]]:
    """
    Finds settlements between people based on their totals.

    Args:
        - `people: List[str]` - A list of people's names.
        - `totals: List[int]` - A list of total amounts for each person.
        - `i: int` - The index of the current person.

    Returns:
        - `List[List[str]]` - A list of settlements.
    """
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


def _settleDebts(people: List[str], totals: List[int]) -> List[List[str]]:
    """
    `settleDebts()` helper. Finds the settlements for debts among a group of people.

    Args:
        - `people: List[str]` - A list of people's names.
        - `totals: List[int]` - A list of debt totals for each person.

    Returns:
        - `List[List[str]]` - A list of settlements.
    """
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
