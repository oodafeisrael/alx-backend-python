#!/usr/bin/env python3
import mysql.connector


class DatabaseConnection:
    """Context manager for managing MySQL database connections."""
    def __init__(self, host, user, password, database):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Replace these values with your actual MySQL credentials
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "your_password",
        "database": "your_database"
    }

    # Example usage to SELECT from users table
    with DatabaseConnection(**db_config) as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)

i
