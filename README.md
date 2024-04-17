# Debt Simplifer

**All code was written and tested using Python 3.12.0.**

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

# Part 2 - Worker implementation
My implementation of the worker lies in the `part_2/worker/src` folder. There are:

- `scripts/` - folder with `debt_simplifier.py` script from the **part_1**. I've decided to move it inside worker's `src/` folder, because the worker is running in the separate docker container and must have access to this script
- `main.py` - implementation of the worker
- `__init__.py`

Using this structure, main functions from `debt_simplifier.py` can be imported into worker's `main.py` like this:
```
from src.scripts.debt_simplifier import (<function_name>, ...)
```
Main library used in the worker is `boto3` - Python SDK for AWS. This library was not initially installed on the worker's container. To install it I've added it to the Dockerfile using poetry:
```
RUN poetry add boto3
```

## Worker's algorithm
Worker's algorithm looks like this:

1. Retrieve necessary configuration values from environment variables:
    - `DEBTS_BUCKET_NAME`: The name of the S3 bucket where debt data is stored.
    - `WORKER_QUEUE_URL`: The URL of the SQS queue where debt processing tasks are received.
    - Establish connections to AWS services:
        - `S3` (for data retrieval and upload)
        - `SQS` (for message reception and deletion)
    - Set up logging to track activity
2. Enter a continuous loop:
    - Check for messages in the SQS queue.
3. Message Processing:
    - If messages are found in the queue:
        ```
        For each message:
            1. Extract the <debtsId> from the message body (JSON format).
            2. Invoke the _processDebtData() function to handle the debt processing for that <debstID>.
            3. Delete the processed message from the queue.
        ```
    - If no messages are found, log a message indicating the queue is empty.

4.  Debt Processing (_processDebtData):
    - Log a message indicating debt processing has started for the specified `<debtsId>`.
    - Download the debt data file from S3 using the provided `<debtsId>`.
    - Read the debt data from the downloaded file.
    - Settle the debts using the `settleDebts()` function from the debt simplifier script.
    - Save the settled debts to an output file.
    - Upload the output file back to S3 with a key based on the `<debtsId>`.
    - Clean up temporary files (downloaded data and output file).
    - Log a message indicating that the processed data `<debtsId>` has been uploaded (If successfull. Otherwise log 'error while processing data for `<debtsId>`').

5. Wait and repeat:
    - Pause for a short interval (5 seconds, as it was set in the file initially) before checking for new messages again.
    - Repeat the process from step 2, continuously checking for and processing debt processing tasks.

Logging and exception handling is used in every crucial part of the code.
