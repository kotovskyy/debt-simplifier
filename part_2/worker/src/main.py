import os
import time
import json
import boto3
from src.scripts.debt_simplifier import readData, saveData, settleDebts

bucket_name = os.environ.get("DEBTS_BUCKET_NAME")
queue_url = os.environ.get("WORKER_QUEUE_URL")

def main():
    s3 = boto3.client("s3")
    sqs = boto3.client("sqs")
    messages = sqs.receive_message(QueueUrl=queue_url)
    
    if 'Messages' in messages:
        for msg in messages['Messages']:
            msgBody = msg['Body']
            msgBody = json.loads(msgBody)
            debtsId = msgBody['debts_id']

            s3.download_file(bucket_name, debtsId, 'temp_data.csv')
            
            data_path = os.getcwd() + "/temp_data.csv"
            output_path = os.getcwd() + "/output.csv"
            data = readData(data_path)
            output = settleDebts(data)
            saveData(output_path, output)
            
            output_key = f"{debtsId}_results"
            s3.upload_file(output_path, bucket_name, output_key)
            
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=msg['ReceiptHandle']
            )
    else:
        print("No messages in the queue")
    

if __name__ == "__main__":
    while True:
        main()
        time.sleep(5)
