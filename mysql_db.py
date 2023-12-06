import mysql.connector

def initialize_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Demo@cc2024",
        database="users"
    )

    cursor = conn.cursor()
    create_table(cursor)

    return conn, cursor

def create_table(cursor):
    cursor.execute("SHOW TABLES")
    temp = cursor.fetchall()
    tables = [item[0] for item in temp]

    if "users" not in tables:
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            password VARCHAR(30),
            email VARCHAR(100) UNIQUE
        )""")

def create_table_new(cursor):
    # Add your table creation logic here
    # Example:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS newreg (
            user_id INT PRIMARY KEY,
            username VARCHAR(255) NOT NULL
        )
    """)

def login(cursor, data):
    cursor.execute(f"""SELECT * FROM users WHERE email = '{data["email"]}' 
                       AND password = '{data["password"]}' """)

    return cursor.fetchone() is not None

conn, cursor = initialize_connection()

# Example login data
login_data = {"email": "rootuser@gmail.com", "password": "root123"}

# Test the login function
if login(cursor, login_data):
    print("Login successful!")
else:
    print("Login failed.")

# Close the database connection
cursor.close()
conn.close()
