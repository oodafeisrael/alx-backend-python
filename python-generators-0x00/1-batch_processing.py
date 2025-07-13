#!/usr/bin/python3

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def stream_users_in_batches(batch_size):
    """Generator that fetches rows from user_data table in batches"""
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Processes each batch and prints users with age > 25"""
    for batch in stream_users_in_batches(batch_size):   # 1st loop
        filtered = (user for user in batch if user["age"] > 25)  # generator expression (no extra loop)
        for user in filtered:  # 2nd loop
            print(user)

