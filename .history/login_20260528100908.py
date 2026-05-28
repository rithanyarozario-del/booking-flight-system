import os
import hashlib

userfile = 'users.txt'

def hash_password(password):
    return hashlib
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