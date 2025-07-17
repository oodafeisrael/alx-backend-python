#!/usr/bin/python3
import time
import sqlite3 
import functools

# Dictionary to cache query results
query_cache = {}

# --- Decorator to handle DB connection ---
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# --- Decorator to cache SQL query results ---
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query")
        if query in query_cache:
            print("Using cached result for query:", query)
            return query_cache[query]
        print("Caching result for query:", query)
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# --- Function using connection and query cache decorators ---
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will execute and cache
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
