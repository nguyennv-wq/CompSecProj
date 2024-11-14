import socket
import threading

# User data and roles
users = {
    "Jonathan": {"password": "Purdue1", "role": "ADMIN", "funds": 10000000000},
    "Bav": {"password": "1upu1", "role": "ADMIN", "funds": 1000000000},
    "Nathan": {"password": "PJ3VF4TA4TUHM", "role": "ADMIN", "funds": 1000000000},
    "admin": {"password": "Spookytus", "role": "ADMIN", "funds": 500},
    "Sueve": {"password": "WillIAm", "role": "USER", "funds": 12392},
    "Sudo": {"password": "ZaZa", "role": "USER", "funds": 30023},
    "Ubuntu": {"password": "ABC", "role": "USER", "funds": 5002},
    "Steve": {"password": "1234", "role": "TELLER", "funds": 252525},
    "SpongBob": {"password": "Bubbles", "role": "TELLER", "funds": 500500200},
}

# Stores the logged-in clients
logged_in_users = {}

# Permission levels for each role
permissions = {
    "USER": ["BALANCE", "SEND", "REQUEST","APPROVE"],
    "TELLER": ["BALANCE", "DEPOSIT", "WITHDRAW","APPROVE","ENROLL"],
    "ADMIN": ["BALANCE", "SEND", "REQUEST", "DEPOSIT", "WITHDRAW", "ENROLL", "PROMOTE", "DEMOTE","APPROVE"]
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
    elif command.startswith("APPROVE"):
        return handle_approve(command, username)
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
        user_role = users[login_user]["role"]
        available_commands = "\n".join(permissions[user_role])
        return (f"Login successful. Welcome {login_user}! You have {user_role} privileges. "
                f"Available commands:\n{available_commands}\n")
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
    # Check if user has permission
    if not has_permission(username, "SEND"):
        return "FAIL: Unauthorized action.\n"

    # Parse command
    parts = command.split()
    if len(parts) != 3:
        return "Usage: SEND <recipient_username> <amount>\n"
    
    recipient_username = parts[1]
    try:
        amount = float(parts[2])
        if amount <= 0:
            return "FAIL: Amount must be positive.\n"
    except ValueError:
        return "FAIL: Invalid amount format.\n"

    # Get sender from `users` dictionary using the logged-in username
    sender_username = logged_in_users.get(username)
    sender = users.get(sender_username)

    if not sender:
        return "FAIL: Sender not logged in.\n"
    
    # Check if sender has enough funds
    if sender["funds"] < amount:
        return "FAIL: Insufficient funds.\n"

    # Check if recipient exists
    recipient = users.get(recipient_username)
    if not recipient:
        return f"FAIL: User {recipient_username} does not exist.\n"
    
    # Update balances for both sender and recipient
    users[sender_username]["funds"] -= amount  # Deduct from sender
    users[recipient_username]["funds"] += amount  # Add to recipient

    return (f"Success! ${amount} sent to {recipient_username}. "
            f"Your new balance is ${users[sender_username]['funds']}.\n")


# Dictionary to store pending requests in the format:
# { "recipient_username": [("requester_username", amount), ...] }
pending_requests = {}

def handle_request(command, username):
    # Parse command
    parts = command.split()
    if len(parts) != 3:
        return "Usage: REQUEST <recipient_username> <amount>\n"
    
    recipient_username = parts[1]
    try:
        amount = float(parts[2])
        if amount <= 0:
            return "FAIL: Amount must be positive.\n"
    except ValueError:
        return "FAIL: Invalid amount format.\n"

    # Check if recipient exists
    if recipient_username not in users:
        return f"FAIL: User {recipient_username} does not exist.\n"

    # Add request to pending_requests under the recipient's username
    if recipient_username not in pending_requests:
        pending_requests[recipient_username] = []
    
    # Add the request (requester, amount) to the recipient's list
    pending_requests[recipient_username].append((logged_in_users[username], amount))
    
    # Debugging: Print the pending requests
    print(f"Pending requests after {username}'s request: {pending_requests}")

    return (f"Request for ${amount} sent to {recipient_username}. "
            f"Waiting for approval.\n")


def handle_deposit(command, username):
    if not has_permission(username, "DEPOSIT"):
        return "FAIL: Unauthorized action.\n"
    parts = command.split()
    if len(parts) != 2:
        return "Usage: DEPOSIT <amount>\n"
    amount = float(parts[1])
    user = users[logged_in_users[username]]
    user["funds"] += amount
    return f"Deposited ${amount}. New balance: ${user['funds']}.\n"

def handle_withdraw(command, username):
    if not has_permission(username, "WITHDRAW"):
        return "FAIL: Unauthorized action.\n"
    parts = command.split()
    if len(parts) != 2:
        return "Usage: WITHDRAW <amount>\n"
    amount = float(parts[1])
    user = users[logged_in_users[username]]
    if amount > user["funds"]:
        return "Insufficient funds.\n"
    user["funds"] -= amount
    return f"Withdrew ${amount}. New balance: ${user['funds']}.\n"

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

def handle_approve(command, username):
    # Parse command
    parts = command.split()
    if len(parts) != 3:
        return "Usage: APPROVE <requester_username> <amount>\n"
    
    requester_username = parts[1]
    try:
        amount = float(parts[2])
    except ValueError:
        return "FAIL: Invalid amount format.\n"
    
    # Ensure the current user is the recipient of the request (who should approve it)
    recipient_username = logged_in_users.get(username)
    
    if recipient_username not in pending_requests:
        return "FAIL: No pending requests.\n"
    
    # Debugging: Show what the recipient has in pending requests
    print(f"Pending requests for {recipient_username}: {pending_requests[recipient_username]}")

    # Find the pending request matching the requester and amount
    requests = pending_requests[recipient_username]
    for i, (requester, requested_amount) in enumerate(requests):
        if requester == requester_username and requested_amount == amount:
            # Check if the recipient has enough funds to approve the request
            if users[recipient_username]["funds"] < amount:
                return "FAIL: Insufficient funds to approve this request.\n"
            
            # Process the transaction
            users[recipient_username]["funds"] -= amount
            users[requester]["funds"] += amount
            
            # Remove the approved request
            del requests[i]
            if not requests:  # If no more requests, remove the entry for this recipient
                del pending_requests[recipient_username]
            
            # Debugging: Show updated pending requests
            print(f"Updated pending requests: {pending_requests}")
            
            return (f"Request approved! ${amount} sent to {requester_username}. "
                    f"Your new balance is ${users[recipient_username]['funds']}.\n")
    
    return "FAIL: No matching request found.\n"


def handle_client(client_socket, addr):
    username = addr[0]
    client_socket.send("Welcome to AlphaBank. Please type LOGIN to log in! \n".encode())
    
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
