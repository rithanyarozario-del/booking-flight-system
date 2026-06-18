import os
import hashlib
import sqlite3

USERFILE = "users.txt"
DB_FILE = "bookings.db" #SQL

userfile = "users.txt"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def users_exist(username):
    if not os.path.exists(userfile):
        return False
    
    with open(userfile, "r") as f:
        return any(line.startswith(f"{username}:") for line in f)
    
def register(username, password):
    if users_exist(username):
        return "Username already exists"
        
    with open(userfile, "a") as f:
        f.write(f"{username}:{hash_password(password)}\n")

    return "Registration successful"

def login(username, password):
    if not os.path.exists(userfile):
        return "No Users Registered"

    hashed = hash_password(password)
    
    with open(userfile, "r") as f:
        for line in f:
            if line.strip() == f"{username}:{hashed}":
                return "Login Successful"

    return "Login Failed"

