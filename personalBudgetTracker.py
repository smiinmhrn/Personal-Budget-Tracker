from enum import Enum
import os
import json
import re

class FirstMenu(Enum):
    SIGN_UP = ("1. Sign Up", 1)
    SIGN_IN = ("2. Sign in", 2)
    EXIST = ("3. Exist", 3)

class UserMenu(Enum):
    TRANSACTION_REGISTRATION = ("1. Transaction registration", 1)
    MANAGE_CATEGORIES = ("2. Manage categories", 2)
    BILL = ("3. Bill", 3)
    STATISTICS_AND_REPORTING = ("4. Statistics and reporting", 4)
    BACK = ("5. Back", 5)

def main_menu():
    #print the menu
    print(FirstMenu.SIGN_UP.value[0], FirstMenu.SIGN_IN.value[0], FirstMenu.EXIST.value[0], 'choose your command...', sep='\n')

    #give the command
    choice = valid_command()

    #match the options with user choice
    while True:
        if choice == FirstMenu.SIGN_UP.value[1]:
            sign_up()
            break
        elif choice == FirstMenu.SIGN_IN.value[1]:
            sign_in()
            break
        elif choice == FirstMenu.EXIST.value[1]:
            break
        else:
            print('Invalid command. choose another one')
            choice = valid_command()

def user_menu():
    #print the menu
    print(UserMenu.TRANSACTION_REGISTRATION.value[0], UserMenu.MANAGE_CATEGORIES.value[0],
           UserMenu.BILL.value[0], UserMenu.STATISTICS_AND_REPORTING.value[0], UserMenu.BACK.value[0], 'choose your command...', sep='\n')
    
    #give the command
    choice = valid_command()

    #match the options with user choice
    while True:
            if choice == UserMenu.TRANSACTION_REGISTRATION.value[1]:
                break
            elif choice == UserMenu.MANAGE_CATEGORIES.value[1]:
                break
            elif choice == UserMenu.BILL.value[1]:
                break
            elif choice == UserMenu.STATISTICS_AND_REPORTING.value[1]:
                break
            elif choice == UserMenu.BACK.value[1]:
                os.system('cls')
                main_menu()
                break
            else:
                print('Invalid command. try again')
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
            print("Please enter a number. try again")
    return valid_input


#creat an account for user
def sign_up():
    os.system('cls')
    name = input('Enter your full name \n').strip()
    username = input('Enter user name to creat an account \n').strip()

    while True:
        if not uniq_username(username)[0]:
            print('user name already taken choose another one')
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
    
    os.system('cls')
    user_menu()

#user sign in to the account
def sign_in():
    os.system('cls')
    username = input('Enter your username \n').strip()

    username_info = ()
    while True:
        username_info = uniq_username(username)
        if username_info[0]:
            username = input("username not found. try again \n").strip()
        else:
            break
    
    password = input('Enter your password \n').strip()
    while True:
        if username_info[1] == password:
            os.system('cls')
            user_menu()
            break
        else:
            password = input('your pass is wrong. try again \n').strip()


#check if the user name is uniq or not
def uniq_username(username):
    try:
        with open("account.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
        return (True, "")
    for user_data in data:
        if user_data["username"] == username:
            return (False, user_data["password"])
        else:
            return (True, "")


#insure that all the pass format is correct
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
        print('your password should has at least 8 characters. try again')
        return False
    else:
        return True

def valid_password_upercase(password):
   
    if not re.search(r"[A-Z]", password):
        print('your password should has at least one uppercase letter. try again')
        return False
    else:
        return True
    
def valid_password_lowercase(password):
    
    if not re.search(r"[a-z]", password):
        print('your password should has at least one lowercase letter. try again')
        return False
    else:
        return True

def valid_password_digit(password):

    if not re.search(r"\d", password):
        print('your password should has at least one digit. try again')
        return False
    else:
        return True

def valid_password_character(password):
    
    if not re.search(r"[*$#@!]", password): 
        print('your password should has at least least one special character (*$#@!). try again')
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