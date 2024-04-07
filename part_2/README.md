# Debt Simplifer

# Part 1 - Debt Simplifier main script

My implementation of **Debt Simplifier** lies in the `part_1/` folder. There are files:

- `main.py` - main script of the **Debt Simplifier**
- `test_main.py` - unit tests for crucial functionalities of the `main.py` (`pytest`)
- `requirements.txt` - file with requirements needed to execute script and tests

## Usage
1. Save the script as `debt_simplifier.py` (or any preferred name)
2. Open a command prompt
3. Run the script using the following command:
```
python <path_to_script> <path_to_data> <path_to_save_output>
```
- `<path_to_data>` - path to the the CSV file containing the debts data
- `<path_to_save_output>` - path to the CSV file where output will be saved
4. The script will process the input data and create (or overwrite if the file 
already exists) the output file with the settled transactions.

## Input CSV format
The data in the input CSV file must have the following format:
```
<payer>,<debtor>,<amount> 
```
- **Example:** `Jacek,Dominik,10` - Dominik owes Jacek 10 units of currency

## Output CSV format
The data in the output CSV file will have slightly different format:
```
<debtor>,<payer>,<amount>
```
- **Example:** `Dominik,Jacek,5` - Dominik must pay Jacek 5 units of currency

## Time complexity of implemented functions
Assuming that **N** is a number of rows in input CSV file and **P** in a real number of people, we get:

- `getArguments()`: O(1) - Constant time, independent of input size.
- `_fileExists()`: O(1) - Constant time, system call complexity.
- `readData()`: O(N) - Linear time, iterates through N rows in the CSV file.
- `saveData()`: O(P) - Linear time in the worst case, iterates through P unique   people to write data.
- `_initPersonTotal()`: O(N) - Linear time, iterates through N rows in the data to build the dictionary.
- `_findSettlements()`:
    - **Worst case**: O(P) - In a complex debt chain scenario, the inner loop might iterate close to P times.
    - **Real complexity**: Smaller than O(P) - In most cases, the inner loop terminates early, leading to a lower complexity.
- `_settleDebts()`:
    - **Worst case**: O(P^2) - Loop iterates through P people, and each iteration calls `_findSettlements()` with worst-case O(P).
    - **Real complexity**: O(P) - In most cases, the inner loop in `_findSettlements()` terminates early, leading to a complexity dominated by the outer loop iterating through P people.
- `settleDebts()`:
    - **Worst case**: O(N + PlogP + P^2) - Combines complexities of `_initPersonTotal()`, sorting (`sorted()` with O(PlogP)), and worst-case `_settleDebts()`.
    - **Real complexity**: O(N + PlogP + P) - In most cases, the inner loop in `_findSettlements()` terminates early, reducing the complexity of `_settleDebts()` to O(P).
