import socket
import threading

# User data and roles
users = {
    "Jonathan": {"password": "Purdue1", "role": "ADMIN", "funds": 10000000000},
    "Bav": {"password": "1upu1", "role": "ADMIN", "funds": 1000000000},
    "Nathan": {"password": "PJ3VF4TA4TUHM", "role": "ADMIN", "funds": 1000000000},
    "Santiago": {"password": "AlphaC00l!", "role": "USER", "funds": 500},
    "Sueve": {"password": "WillIAm", "role": "USER", "funds": 12392},
    "Sudo": {"password": "ZaZa", "role": "USER", "funds": 30023},
    "Ubuntu": {"password": "ABC", "role": "USER", "funds": 5002}
}

# Stores the logged-in clients
logged_in_users = {}

# Permission levels for each role
permissions = {
    "USER": ["BALANCE", "SEND", "REQUEST", "APPROVE"],
    "TELLER": ["BALANCE", "SEND", "REQUEST", "APPROVE", "DEPOSIT", "WITHDRAW", "ENROLL"],
    "ADMIN": ["BALANCE", "SEND", "REQUEST", "APPROVE", "DEPOSIT", "WITHDRAW", "ENROLL", "PROMOTE", "DEMOTE"]
}

# Command handlers
def handle_command(command, client_socket, username):
    if command.startswith("LOGIN"):
        return handle_login(command, client_socket, username)
    elif command == "BALANCE":
        return handle_balance(client_socket, username)
    elif command == "LOGOUT":
        return handle_logout(client_socket, username)
    elif command.startswith("SEND"):
        return handle_send(command, username)
    elif command.startswith("REQUEST"):
        return handle_request(command, username)
    elif command.startswith("APPROVE"):
        return handle_approve(command, username)
    elif command.startswith("DEPOSIT"):
        return handle_deposit(command, username)
    elif command.startswith("WITHDRAW"):
        return handle_withdraw(command, username)
    elif command.startswith("ENROLL"):
        return handle_enroll(command, username)
    elif command.startswith("PROMOTE"):
        return handle_promote(command, username)
    elif command.startswith("DEMOTE"):
        return handle_demote(command, username)
    else:
        return "Invalid command. Try again.\n"

def has_permission(username, command):
    user = users.get(logged_in_users.get(username))
    return user and command in permissions[user["role"]]

def handle_login(command, client_socket, username):
    parts = command.split()
    if len(parts) != 3:
        return "Usage: LOGIN <username> <password>\n"
    
    login_user, password = parts[1], parts[2]
    if login_user in users and users[login_user]["password"] == password:
        logged_in_users[username] = login_user
        return f"Login successful. Welcome {login_user}!\n"
    else:
        return "Invalid username or password.\n"

def handle_balance(client_socket, username):
    if not has_permission(username, "BALANCE"):
        return "FAIL: Unauthorized action.\n"
    user = users.get(logged_in_users[username])
    balance = user["funds"]
    return f"Your current balance is ${balance}.\n"

def handle_logout(client_socket, username):
    if username in logged_in_users:
        logged_in_users.pop(username)
        return "You have logged out.\n"
    else:
        return "You are not logged in.\n"

def handle_send(command, username):
    # Implementation for sending funds
    return "SEND command executed.\n"

def handle_request(command, username):
    # Implementation for requesting funds
    return "REQUEST command executed.\n"

def handle_approve(command, username):
    # Implementation for approving a transaction
    return "APPROVE command executed.\n"

def handle_deposit(command, username):
    if not has_permission(username, "DEPOSIT"):
        return "FAIL: Unauthorized action.\n"
    # Implement deposit functionality here
    return "DEPOSIT command executed.\n"

def handle_withdraw(command, username):
    if not has_permission(username, "WITHDRAW"):
        return "FAIL: Unauthorized action.\n"
    # Implement withdraw functionality here
    return "WITHDRAW command executed.\n"

def handle_enroll(command, username):
    if not has_permission(username, "ENROLL"):
        return "FAIL: Unauthorized action.\n"
    parts = command.split()
    if len(parts) != 3:
        return "Usage: ENROLL <new_username> <password>\n"
    
    new_username, password = parts[1], parts[2]
    if new_username in users:
        return "FAIL: User already exists.\n"
    
    users[new_username] = {"password": password, "role": "USER", "funds": 0}
    return f"User {new_username} enrolled successfully.\n"

def handle_promote(command, username):
    if not has_permission(username, "PROMOTE"):
        return "FAIL: Unauthorized action.\n"
    parts = command.split()
    if len(parts) != 2:
        return "Usage: PROMOTE <username>\n"
    
    target_user = parts[1]
    if target_user not in users:
        return "FAIL: User does not exist.\n"
    
    current_role = users[target_user]["role"]
    if current_role == "USER":
        users[target_user]["role"] = "TELLER"
    elif current_role == "TELLER":
        users[target_user]["role"] = "ADMIN"
    else:
        return "FAIL: User is already an ADMIN.\n"
    
    return f"{target_user} promoted to {users[target_user]['role']}.\n"

def handle_demote(command, username):
    if not has_permission(username, "DEMOTE"):
        return "FAIL: Unauthorized action.\n"
    parts = command.split()
    if len(parts) != 2:
        return "Usage: DEMOTE <username>\n"
    
    target_user = parts[1]
    if target_user not in users:
        return "FAIL: User does not exist.\n"
    
    current_role = users[target_user]["role"]
    if current_role == "ADMIN":
        users[target_user]["role"] = "TELLER"
    elif current_role == "TELLER":
        users[target_user]["role"] = "USER"
    else:
        return "FAIL: User is already a USER.\n"
    
    return f"{target_user} demoted to {users[target_user]['role']}.\n"

def handle_client(client_socket, addr):
    username = addr[0]
    client_socket.send("Welcome to AlphaBank. Please log in.\n".encode())
    
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        command = data.decode().strip()
        response = handle_command(command, client_socket, username)
        client_socket.send(response.encode())
    
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 6201))
    server.listen(5)
    print("Server started on port 6201")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
