#!/usr/bin/env python3
import mysql.connector


class ExecuteQuery:
    """Context manager for executing parameterized queries on a MySQL database."""

    def __init__(self, config, query, params=()):
        self.config = config            # Dictionary with connection details
        self.query = query              # SQL query to execute
        self.params = params            # Parameters for the query
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Define your database connection configuration
    db_config = {
        'host': 'localhost',
        'user': 'your_username',
        'password': 'your_password',
        'database': 'your_database'
    }

    query = "SELECT * FROM users WHERE age > %s"
    params = (25,)

    with ExecuteQuery(db_config, query, params) as results:
        for row in results:
            print(row)

