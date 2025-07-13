#!/usr/bin/python3

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def stream_users():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT", 3306)
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()

#  This makes the module itself behave like a function
def __call__():
    return stream_users()

# Bind the module-level callable to `__call__`
import sys
sys.modules[__name__] = __call__
