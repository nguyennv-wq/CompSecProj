import sqlite3
from sqlite3 import Error
import hashlib
import os

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

# Function to hash a password with a salt
def hash_password(password):
    """Hash the password with a salt using PBKDF2-HMAC-SHA256."""
    salt = os.urandom(16)  # Generate a 16-byte random salt
    hashed_pw = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt + hashed_pw  # Return salt + hashed password

# Function to create tables in the database
def create_tables(conn):
    """Create tables in the database."""
    try:
        # Create a cursor object
        cursor = conn.cursor()

        # Create a users table (id, username, email, hashed password, role)
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'  -- Add a role column with default 'user'
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

# Function to insert initial users into the database
def insert_initial_users(conn):
    """Insert initial users into the database."""
    cursor = conn.cursor()

    # Users with pre-defined passwords and roles
    users_data = [
        ("Jonathan", "jonathanspassword123", "jonathan@example.com", "user"),
        ("Bav", "bavspassword456", "bav@example.com", "user"),
        ("Nathan", "nathanspassword789", "nathan@example.com", "user"),
        ("admin", "adminpassword", "admin@example.com", "admin"),
        ("Sueve", "suevespassword", "sueve@example.com", "teller"),
        ("Sudo", "sudospassword", "sudo@example.com", "teller"),
        ("Ubuntu", "ubuntupassword", "ubuntu@example.com", "user"),
        ("Steve", "stevespassword", "steve@example.com", "user"),
        ("SpongBob", "spongebobpassword", "spongbob@example.com", "user")
    ]

    for username, password, email, role in users_data:
        # Hash the password before inserting
        hashed_pw = hash_password(password)
        cursor.execute('''
        INSERT OR IGNORE INTO users (username, email, password, role) 
        VALUES (?, ?, ?, ?)
        ''', (username, email, hashed_pw, role))

    # Commit the changes
    conn.commit()

# Function to initialize the database
def initialize_db():
    """Initialize the database by creating tables and inserting initial users."""
    conn = create_connection()

    if conn:
        create_tables(conn)
        insert_initial_users(conn)
        conn.close()

# Run the database setup
if __name__ == '__main__':
    initialize_db()
