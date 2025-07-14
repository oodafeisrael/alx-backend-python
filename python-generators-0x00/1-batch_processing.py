#!/usr/bin/python3

#!/usr/bin/python3
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()  # Load DB credentials from .env

def stream_users_in_batches(batch_size):
    """Generator that yields users in batches from the user_data table"""
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """Process each batch and print users over age 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)

