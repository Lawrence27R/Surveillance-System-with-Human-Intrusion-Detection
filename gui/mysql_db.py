import mysql.connector
import os

class DatabaseHandler:
    def __init__(self):
        self.conn, self.cursor = self.initialize_connection()

    def initialize_connection(self):
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "users")
    )

        cursor = conn.cursor()
        self.create_table(cursor)
        
        return conn, cursor

    def create_table(self, cursor):
        cursor.execute("SHOW TABLES")
        temp = cursor.fetchall()
        tables = [item[0] for item in temp]

        if "users" not in tables:
            cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                password VARCHAR(30),
                email VARCHAR(100) UNIQUE
            )""")

    def create_add_details_table(self, cursor):
        cursor.execute("SHOW TABLES")
        temp = cursor.fetchall()
        tables = [item[0] for item in temp]

        if "add_details" not in tables:
            cursor.execute("""CREATE TABLE IF NOT EXISTS add_details (
                user_id INT PRIMARY KEY,
                user_name VARCHAR(255),
                email VARCHAR(100),
                phone_number VARCHAR(20)
            )""")

    def create_table_new(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS newreg (
                user_id INT PRIMARY KEY,
                username VARCHAR(255) NOT NULL
            )
        """)
    


    def login(self, data):
        self.cursor.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s",
            (data["email"], data["password"])
        )

        return self.cursor.fetchone() is not None

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
