#!/usr/bin/python3

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def stream_users_in_batches(batch_size):
    """
    Generator function that yields users in batches from the database.
    """
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes users in batches and returns those with age > 25.
    """
    filtered_users = []

    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)  # Optional: for visible output
                filtered_users.append(user)

    return filtered_users

