# db_setup.py
import sqlite3
import bcrypt

# Setup database and tables
def setup_database():
    conn = sqlite3.connect('alphabank.db')
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            funds REAL DEFAULT 0
        )
    ''')

    # Create transactions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            from_user TEXT,
            to_user TEXT,
            amount REAL,
            status TEXT
        )
    ''')

    # Insert default admin user
    admin_password = bcrypt.hashpw("Spookytus".encode(), bcrypt.gensalt())
    c.execute('''
        INSERT OR IGNORE INTO users (username, password, role) 
        VALUES (?, ?, ?)
    ''', ("admin", admin_password, "ADMIN"))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
