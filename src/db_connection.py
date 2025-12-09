import sqlite3
import os
from contextlib import contextmanager



path='database/ecommerce.db'



#getting connection (Manual Close)
def connection():
    try:
        conn=sqlite3.connect(path)
        return conn
    except sqlite3.Error as e:
        print(f" Database connection Error- {e}")
        raise


#auto close connection (one function)
@contextmanager
def Auto_Close_connection():
    conn= None
    try:
        conn=sqlite3.connect(path)
        yield conn
    except sqlite3.Error as e:
        print(f"Database Connection Error-{e}")
        raise
    finally:
        if conn:
            conn.close()


#executing queries
def execute_query(query, parameter=None):
    with Auto_Close_connection() as conn:
        cursor=conn.cursor()
        if parameter:
            cursor.execute(query,parameter)
        else:
            cursor.execute(query)
        return cursor.fetchall()


#check if the database exists
def check_database_exists():
    return os.path.exists(path)



#give table names
def tables_in_database():
    with Auto_Close_connection() as conn:
        cursor=conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [row[0] for row in cursor.fetchall()]
