import sqlite3
from sqlite3 import Error

# Path to your SQLite database file
DATABASE = 'alphabank.db'

# Function to create a database connection
def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        print("Connection to the database was successful.")
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

# Function to create tables in the database
def create_tables(conn):
    """Create tables in the database."""
    try:
        # Create a cursor object
        cursor = conn.cursor()

        # Create a users table (id, username, email, hashed password)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
        ''')

        # Create a transactions table (transaction_id, from_user, to_user, amount)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user INTEGER NOT NULL,
            to_user INTEGER NOT NULL,
            amount REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (from_user) REFERENCES users(id),
            FOREIGN KEY (to_user) REFERENCES users(id)
        );
        ''')

        # Commit the changes
        conn.commit()
        print("Tables created successfully.")
    except Error as e:
        print(f"Error creating tables: {e}")

# Function to initialize the database
def initialize_db():
    """Initialize the database by creating tables."""
    conn = create_connection()

    if conn:
        create_tables(conn)
        conn.close()

# Run the database setup
if __name__ == '__main__':
    initialize_db()
