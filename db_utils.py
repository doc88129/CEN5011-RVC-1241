import mysql.connector
from mysql.connector import Error

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            database="fooddb",
            user="root",
            password="password"
        )
        if conn.is_connected():
            print("Connected to MySQL database")
            return conn
    except Error as e:
        print(e)

# Define other database-related functions here
