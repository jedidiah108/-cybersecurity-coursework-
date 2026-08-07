# connect.py

import hashlib
import time
import sys
import os
import re

PASSWORD_FILE = "Passwords.txt"

def generate_pin(username, password, timestamp):
    """
    Regenerate the PIN for verification, same as in device.py.
    """
    data = f"{username}{password}{timestamp}"
    h = hashlib.sha256(data.encode()).hexdigest()
    return str(int(h, 16) % 1_000_000).zfill(6)

def is_strong_password(pw):
    """
    Validate password strength: ≥8 chars, includes letters, digits, and symbols.
    """
    return (
        len(pw) >= 8 and
        re.search(r"[A-Za-z]", pw) and
        re.search(r"\d", pw) and
        re.search(r"[^\w\s]", pw)
    )

def register_user(username):
    """
    Register a new user and store credentials in Passwords.txt.
    """
    # Create file if it doesn't exist
    if not os.path.exists(PASSWORD_FILE):
        open(PASSWORD_FILE, "w").close()

    with open(PASSWORD_FILE, "r") as f:
        for line in f:
            if line.startswith(username + ":"):
                print("Username already exists.")
                return

    pw = input("Enter password: ")
    confirm = input("Confirm password: ")

    if pw != confirm:
        print("Passwords do not match.")
        return

    if not is_strong_password(pw):
        print("Password must be at least 8 characters and include letters, digits, and symbols.")
        return

    with open(PASSWORD_FILE, "a") as f:
        f.write(f"{username}:{pw}\n")

    print("User registered successfully.")

def authenticate(username, password, pin):
    """
    Authenticate a user by checking credentials and verifying the current PIN.
    """
    if not os.path.exists(PASSWORD_FILE):
        print("No users registered.")
        return

    found = False
    with open(PASSWORD_FILE, "r") as f:
        for line in f:
            stored_user, stored_pass = line.strip().split(":")
            if stored_user == username and stored_pass == password:
                found = True
                break

    if not found:
        print("Invalid username or password.")
        return

    current_time = int(time.time() // 15)
    # Check both current and previous PIN for network delay tolerance
    valid_pins = [
        generate_pin(username, password, current_time),
        generate_pin(username, password, current_time - 1)
    ]

    if pin in valid_pins:
        print("Authentication successful.")
    else:
        print("Invalid or expired PIN.")

# Entry point
if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[2] == "new":
        register_user(sys.argv[1])
    elif len(sys.argv) == 4:
        authenticate(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage:")
        print("  python connect.py <username> new")
        print("  python connect.py <username> <password> <pin>")
