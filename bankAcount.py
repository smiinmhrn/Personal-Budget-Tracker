from enum import Enum
import os
import json
import re

class FirstMenu(Enum):
    SIGN_UP = ("1. Sign Up", 1)
    SIGN_IN = ("2. Sign in", 2)
    EXIST = ("3. Exist", 3)

def main_menu():
    #print the menu
    print(FirstMenu.SIGN_UP.value[0], FirstMenu.SIGN_IN.value[0], FirstMenu.EXIST.value[0], 'choose your command...', sep='\n')

    #give the command
    choice = valid_command()

    #match the options with user choice
    while True:
        if choice == FirstMenu.SIGN_UP.value[1]:
            sign_Up()
            break
        elif choice == FirstMenu.SIGN_IN.value[1]:

            break
        elif choice == FirstMenu.EXIST.value[1]:
            break
        else:
            print('Invalid command. choose another one')
            choice = valid_command()


#give the valid command from user
def valid_command():
    valid_input = 0
    while True:
        user_input = input().strip()
        try:
            valid_input = int(user_input)
            break
        except ValueError:
            print("Invalid command. choose another one")
    return valid_input


def sign_Up():
    os.system('cls')
    name = input('Enter your full name \n').strip()
    username = input('Enter user name to creat an account \n').strip()

    while True:
        if not uniq_username(username):
            username = input().strip()
        else:
            break

    password = valid_password(input('Enter your password \n').strip())

    user_info = {
        "name": name,
        "username": username,
        "password": password,
        "cash": 0
    }
    append_to_file(user_info)

#check if the user name is uniq or not
def uniq_username(username):
    try:
        with open("account.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
        return True

    for user_data in data:
        if user_data["username"] == username:
            print('user name already taken choose another one')
            return False
        else:
            return True



def valid_password(password):
    while True:
        if not valid_password_lenth(password):
            password = input().strip()
            continue
        elif not valid_password_upercase(password):
            password = input().strip()
            continue
        elif not valid_password_lowercase(password):
            password = input().strip()
            continue
        elif not valid_password_digit(password):
            password = input().strip()
            continue
        elif not valid_password_character(password):
            password = input().strip()
            continue           
        else:
            return password

#check the password format
def valid_password_lenth(password):

    if len(password) < 8:
        print('your password should has at least 8 characters. try another')
        return False
    else:
        return True


def valid_password_upercase(password):
   
    if not re.search(r"[A-Z]", password):
        print('your password should has at least one uppercase letter. try another')
        return False
    else:
        return True
    
def valid_password_lowercase(password):
    
    if not re.search(r"[a-z]", password):
        print('your password should has at least one lowercase letter. try another')
        return False
    else:
        return True

def valid_password_digit(password):

    if not re.search(r"\d", password):
        print('your password should has at least one digit. try another')
        return False
    else:
        return True

def valid_password_character(password):
    
    if not re.search(r"[*$#@!]", password): 
        print('your password should has at least least one special character (*$#@!). try another')
        return False
    else:
        return True       


#write new user info into a file 
def append_to_file(new_data):
    try:
        # Read existing data from file, if any
        with open("account.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        # If file doesn't exist, initialize with an empty list
        data = []

    # Append new data to existing list
    data.append(new_data)

    # Write updated data back to file
    with open("account.json", "w") as file:
        json.dump(data, file, indent= 4)



main_menu()