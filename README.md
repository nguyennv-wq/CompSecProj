# AlphaBank Server Application

AlphaBank is a Python-based banking server that provides secure multi-user functionality with role-based permissions, hashed and salted password storage, and a simple command-based interface.

---

## Features

1. **User Authentication**
   - Secure login using hashed and salted passwords (PBKDF2 with SHA-256).
   - Supports multi-client connections.

2. **Roles and Permissions**
   - Three roles: **ADMIN**, **TELLER**, and **USER**.
   - Role-based permissions determine accessible commands.

3. **Supported Commands**
   - `LOGIN`: Authenticate to the server.
   - `BALANCE`: Check your account balance.
   - `SEND`: Transfer funds to another user.
   - `REQUEST`: Request funds from another user.
   - `APPROVE`: Approve fund requests.
   - `DEPOSIT`: Add funds to your account (TELLER or higher).
   - `WITHDRAW`: Withdraw funds (TELLER or higher).
   - `ENROLL`: Register a new user (TELLER or higher).
   - `PROMOTE/DEMOTE`: Modify user roles (ADMIN only).
   - `LOGOUT`: End your session.

4. **Database-Backed**
   - SQLite database (`alphabank.db`) for persistent storage of user data and transaction records.

5. **Preloaded Users**
   - The server includes some default users with predefined roles and balances.

---

## Setup Instructions

### Prerequisites

1. **Python**: Version 3.8 or higher.
2. Required Python modules:
   - `sqlite3` (included in Python standard library).

---

### Setting Up the Application

1. **Clone or Download the Repository**
   - Ensure all required files are in the same directory.

2. **Initialize the Database**
   - Run the `db_setup.py` script to set up the SQLite database:
     ```bash
     python db_setup.py
     ```

3. **Start the Server**
   - Run the `app.py` script to start the server:
     ```bash
     python app.py
     ```

4. **Connect to the Server**
   - Use `telnet` or `netcat` to connect to the server:
     ```bash
     nc localhost 5555
     ```
   - Replace `localhost` with the server's IP address if hosted remotely.

---

## Commands and Usage

### Logging In
```bash
LOGIN <username> <password>
