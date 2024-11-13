# app.py
import socket
import sqlite3
import bcrypt
import threading

# TCP port and max connections
PORT = 6201
MAX_CONNECTIONS = 16

# Database connection
conn = sqlite3.connect('alphabank.db', check_same_thread=False)
cursor = conn.cursor()

# Dictionary for session tracking
sessions = {}

# Command handler functions
def login(username, password):
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    if user and bcrypt.checkpw(password.encode(), user[2]):
        return f"Logged in as {username}", user[0]  # user_id
    else:
        return "Login failed", None

def deposit(user_id, amount):
    cursor.execute("UPDATE users SET funds = funds + ? WHERE id=?", (amount, user_id))
    conn.commit()
    return f"Deposited {amount}"

# Handling commands based on roles
def handle_command(user_id, role, command):
    parts = command.strip().split()
    if len(parts) == 0:
        return "Invalid command"
    
    cmd = parts[0]
    if cmd == "deposit" and role in ["TELLER", "ADMIN"]:
        amount = float(parts[2])
        return deposit(user_id, amount)
    elif cmd == "login":
        return login(parts[1], parts[2])
    else:
        return "Unknown command or insufficient permissions"

# Handle client connection
def client_handler(client_socket, address):
    client_socket.send(b"Welcome to AlphaBank!\n")
    user_id = None
    role = None

    while True:
        command = client_socket.recv(1024).decode().strip()
        if command.lower() == "quit":
            client_socket.send(b"Goodbye!\n")
            client_socket.close()
            break

        if not user_id:
            if command.startswith("login"):
                msg, user_id = login(*command.split()[1:])
                client_socket.send(f"{msg}\n".encode())
                if user_id:
                    role = cursor.execute("SELECT role FROM users WHERE id=?", (user_id,)).fetchone()[0]
            else:
                client_socket.send(b"Please login first.\n")
        else:
            response = handle_command(user_id, role, command)
            client_socket.send(f"{response}\n".encode())

# Start server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', PORT))
    server.listen(MAX_CONNECTIONS)
    print(f"Server listening on port {PORT}")

    while True:
        client_socket, address = server.accept()
        print(f"Connection from {address}")
        client_thread = threading.Thread(target=client_handler, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
