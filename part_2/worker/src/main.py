import os
import time
import json
import logging
import boto3
from src.scripts.debt_simplifier import readData, saveData, settleDebts


logging.basicConfig(level=logging.INFO)

bucket_name = os.environ.get("DEBTS_BUCKET_NAME")
queue_url = os.environ.get("WORKER_QUEUE_URL")

def _removeTempFiles(data_path: str, output_path: str) -> None:
    """
    Remove temporary files.

    Args:
        - `data_path: str` - The path to the data file.
        - `output_path: str` - The path to the output file.
    """
    try:
        if os.path.exists(data_path):
            os.remove(data_path)
        if os.path.exists(output_path):
            os.remove(output_path)
    except Exception as e:
        logging.error(f"Error while removing temp files: {e}")
    else:
        logging.info("Temp files removed successfully")

def _processDebtData(debtsId: str) -> None:
    """
    Download debt data, process it, upload results and clean up.
    
    Args:
        - `debtsId: str` - The ID of the debt data.
    """
    s3 = boto3.client("s3")
    data_path = os.getcwd() + "/temp_data.csv"
    output_path = os.getcwd() + "/output.csv"
    try:
        logging.info(f"Processing debt data for ID: {debtsId}")
        
        s3.download_file(bucket_name, debtsId, 'temp_data.csv')
        
        data = readData(data_path)
        output = settleDebts(data)
        saveData(output_path, output)
        
        output_key = f"{debtsId}_results"
        s3.upload_file(output_path, bucket_name, output_key)
    except Exception as e:
        logging.error(f"Error while processing debt data for <debtsId> = {debtsId}: {e}")
    else:
        logging.info(f"Uploaded processed data for ID: {debtsId}")
    finally:
        _removeTempFiles(data_path, output_path)
    
    

def main():
    sqs = boto3.client("sqs")
    
    while True:
        try:
            messages = sqs.receive_message(QueueUrl=queue_url)
            if 'Messages' in messages:
                for msg in messages['Messages']:
                    msgBody = msg['Body']
                    msgBody = json.loads(msgBody)
                    debtsId = msgBody['debts_id']

                    _processDebtData(debtsId)
                    
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=msg['ReceiptHandle']
                    )
            else:
                logging.info("No messages in the queue")
                
        except Exception as e:
            logging.error(f"Error while interacting with SQS: {e}")
            
        time.sleep(5)
    

if __name__ == "__main__":
    main()
