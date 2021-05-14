import time
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import os
import json
from google.cloud import bigquery

project_id = "blank-space-312006"
sub_id = "sub-1"
dataset_id = "week4"

timeout = 60
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

sub = pubsub_v1.SubscriberClient()

subscription_path = sub.subscription_path(project_id, sub_id)

messages = []

def callback(message):
    print(f"Received {message.data}.")
    message.ack()
    str_data = str(message.data).replace("\\n", "").replace("\\t", "").replace("\\r","").replace("\\","").replace("b\'b\'", "").replace("'", "") 
    # print(str_data)
    json_data = json.loads(str_data) 
    activities = [obj for obj in json_data['activities']]

    client = bigquery.Client()
    for act in activities:
        table_id = act['table']
        table_id1 = f'{project_id}.{dataset_id}.{table_id}'
        operation = act['operation']
        col_names = act['col_names']
        col_values = act['col_values']
        col_types = act['col_types']

        tables = [tables.table_id for tables in client.list_tables(dataset_id)]

        #something to do on insert operation here
        if operation == "insert":
            #check bq dataset, if table not exist, we need to create table and define schema
            if table_id not in tables:
                #create schema for new table
                schema = []
                for col_idx in range(len(col_names)):
                    field = bigquery.SchemaField(col_names[col_idx], col_types[col_idx])
                    schema.append(field)
                    
                table = bigquery.Table(table_id1, schema=schema)
                table = client.create_table(table) #make an API request.
            
            #we're done to create table. 
            add = ', '.join([f'ADD COLUMN IF NOT EXISTS {col[0]} {col[1] if col[1] != "integer" else "numeric"}' for col in zip(col_names, col_types)])
            sql = f'ALTER TABLE {table_id1} {add}'    
            client.query(sql)

        #TODO insert with new column operation need to be repair. There's some issue.
            #insert data to the table. 
            rows_to_insert = {}
            for idx in range(len(col_names)):
                rows_to_insert[col_names[idx]] = col_values[idx]
            
            insert_job = client.insert_rows_json(table_id1, [rows_to_insert]) 

        #TODO delete operation need to be repair. There's some issue.
        elif operation == "delete":
            if table_id not in tables:
                print(f"Transaction failed, {table_id} not found")
            else:
                row_to_delete = []
                #create query statement
                for idx in range(len(col_names)):
                    row_to_delete.append(f"""{col_names[idx]} = {col_values[idx] if col_types[idx] == 'integer' else f"'{col_values[idx]}'"}""")
                sql = f"DELETE FROM {table_id1} WHERE {' and '.join(row_to_delete)}" 
                print(sql)
                query_job = client.query(sql) 

streaming_pull_future = sub.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

with sub:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()