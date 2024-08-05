from confluent_kafka import Consumer
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


kafka_conf = {
    'bootstrap.servers': 'localhost:9092',  
    'group.id': 'log_consumer_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(kafka_conf)
consumer.subscribe(['postgresql'])  

def fetch_logs_from_kafka():
    logs = []
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                break
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            
            logs.append(msg.value().decode('utf-8'))
    finally:
        consumer.close()
    return logs

def save_logs_to_parquet(logs, file_path):
    
    df = pd.DataFrame(logs, columns=['log'])
    
    
    table = pa.Table.from_pandas(df)
    
    
    pq.write_table(table, file_path)

if __name__ == '__main__':
    logs = fetch_logs_from_kafka()
    if logs:
        save_logs_to_parquet(logs, 'postgres_logs.parquet')
        print("Logs have been saved to postgresql_logs.parquet")
    else:
        print("No logs found to save.")
