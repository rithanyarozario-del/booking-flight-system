import os
import hashlib

userfile = 'users.txt'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def users_exist(username):
    if not os.path.exists(userfile):
        return False
    with open(userfile, 'r') as f:
        return any(line.startswith(f"{username}:") for line in f)
    
def register():
    username = input("Enter username:")
    if users_exist(username):
        print("Username already exists")
        return
    password = input("Enter password:")
    with open(userfile, 'a') as f:
        f.write(f"{username}:{hash_password(password)}\n")
    print("Registration successful")

def login():
    if not os.path.exists(user_file):
        print("No Users Regestred")")

        userame = input("Enter unsername")
        password = input("Enter password")
        hashed = has_password(password)
        with open(user_file, 'r') as f:
            for line in f:
                if line.strip() == f"{username}:{hashed}":
                    print("Login Successful")

        print("Login Failed")




def login ():
    options = {'1': Register, '2': Login, '3': Exit}
    while True:
        print ("\1. Register \n2.Login\n3.Exit")
        choice = input("choose an option:")
        action = options.get(choice) 
        if action:
            action()
        
        else:
            print("Invalid Login")