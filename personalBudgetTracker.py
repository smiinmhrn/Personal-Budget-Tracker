from enum import Enum
import os
import json
import re
from datetime import datetime


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

class BillMenu(Enum):
    SHOW = ("1. Show", 1)
    FILTER = ("2. Filter", 2)
    SORT = ("3. Sort", 3)
    BACK = ("4. Back", 4)
global_user_info = {}

def main_menu():
    #print the menu
    print(FirstMenu.SIGN_UP.value[0], FirstMenu.SIGN_IN.value[0], FirstMenu.EXIST.value[0], sep='\n')

    #give the command
    choice = valid_number_input(input("choose your command... \n"))

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
            choice = valid_number_input(input("Invalid command. choose another one \n"))

def user_menu():
    #print the menu
    print(UserMenu.TRANSACTION_REGISTRATION.value[0], UserMenu.MANAGE_CATEGORIES.value[0],
           UserMenu.BILL.value[0], UserMenu.STATISTICS_AND_REPORTING.value[0], UserMenu.BACK.value[0], sep='\n')
    
    #give the command
    choice = valid_number_input(input("choose your command...\n"))

    #match the options with user choice
    while True:
            if choice == UserMenu.TRANSACTION_REGISTRATION.value[1]:
                Transaction_registration()
                break
            elif choice == UserMenu.MANAGE_CATEGORIES.value[1]:
                break
            elif choice == UserMenu.BILL.value[1]:
                bill()
                break
            elif choice == UserMenu.STATISTICS_AND_REPORTING.value[1]:
                break
            elif choice == UserMenu.BACK.value[1]:
                os.system('cls')
                main_menu()
                break
            else:
                choice = valid_number_input(input('Invalid command. try again \n'))


#do and write the transactions into file
def Transaction_registration():
    global global_user_info

    os.system('cls')
    print("[ TRANSACTION REGISTRATION ]")
    transaction_type = valid_number_input(input("What kind of transaction is it ؟\n1. Income          2. Cost \n"))
    
    while True:
        if transaction_type != 1 and transaction_type != 2:
            transaction_type = valid_number_input(input("choose from options above \n"))
        else: 
            break

    #give the info of transaction from user 
    receiver = valid_string_input(input("enter the name of receiver: "))
    depositor = valid_string_input(input("enter the name of depositor: "))
    amount = valid_money_input()
    date = str(get_user_date())
    category = valid_string_input(input("enter the category of transport: "))

    #create an id for every transaction to undrestand which transaction did earlier
    transaction_id = 1
    if len(global_user_info["transactions"]) != 0:
        transaction_id = transaction_id + global_user_info["transactions"][-1]["id"]


    #make a dictionary of it to save
    transactions = {
        "id": transaction_id,
        "reciver": receiver,
        "depositor": depositor,
        "amount": amount,
        "date": date,
        "category": category,
    }


    #check if the transaction is income increase the user cash else decrease it and update the user cash
    if transaction_type == 1 :
        global_user_info["cash"] = global_user_info["cash"] + amount
    else:
        global_user_info["cash"] = global_user_info["cash"] - amount
    

    #update and add the new transaction into user account
    global_user_info["transactions"].append(transactions)

    #delete the old user info from json file
    delete_from_json()

    #update an add the user info into file
    append_to_file(global_user_info)
    
    #access the user to add another transaction or back to previous menue
    command = valid_number_input(input("Transaction saved sucsesfully.\n1. Add another          2. Back\n"))

    while True:
        if command != 1 and command != 2:
            command = valid_number_input(input("choose from options above \n"))
        else: 
            break
    
    if command == 1:
        os.system('cls')
        Transaction_registration()
    else:
        os.system('cls')
        user_menu()

#creat bill menu
def bill():
    os.system('cls')
    print("[ BILL ]")
    print(BillMenu.SHOW.value[0], BillMenu.FILTER.value[0], BillMenu.SORT.value[0], BillMenu.BACK.value[0], sep='\n')

    choice = valid_number_input(input("choose your command... \n"))

    #match the options with user choice
    while True:
        if choice == BillMenu.SHOW.value[1]:
            show_bill()
            break
        elif choice == BillMenu.FILTER.value[1]:
            break
        elif choice == BillMenu.SORT.value[1]:
            break
        elif choice == BillMenu.BACK.value[1]:
            user_menu()
            break
        else:
            choice = valid_number_input(input("Invalid command. choose another one \n"))

def show_bill():
    os.system('cls')
    print("[ SHOW BILL ]")
    choice = valid_number_input(input("how many bill you want to see.\n1. 10          2. 50          3. all\n"))

    while True:
        if choice != 1 and choice != 2 and choice != 3:
            choice = valid_number_input(input("choose from options above \n"))
        else: 
            break
    
    if choice == 1:
        print_bill(10)
    elif choice == 2:
        print_bill(50)
    else:
        pass
        print_bill(len(global_user_info["transactions"]))

    command = valid_number_input(input("Result showed sucsesfully.\n1. Show Again          2. Back\n"))

    while True:
        if command != 1 and command != 2:
            command = valid_number_input(input("choose from options above \n"))
        else: 
            break
    
    if command == 1:
        os.system('cls')
        show_bill()
    else:
        os.system('cls')
        bill()


def print_bill(number_of_bill):
    if number_of_bill >= len(global_user_info["transactions"]):
        for transaction in global_user_info["transactions"]:
            print("".join(f"{key}: {value} " for key, value in transaction.items()))
    else:
        for transaction in global_user_info["transactions"][-number_of_bill:]:
            print("".join(f"{key}: {value} " for key, value in transaction.items()))


#get a valid input for money
def valid_money_input(prompt="Enter the amount of money: "):
    while True:
        user_input = input(prompt)
        try:
            # Try converting the input to a int 
            amount = int(user_input)
            # Check if the amount is positive
            if amount < 0:
                print("Please enter a positive amount.")
            else:
                return amount
        except ValueError:
            # If conversion fails, print an error message
            print("Invalid input. Please enter a valid number.")


#check the date format for transactions
def get_user_date(prompt="Enter a date of transport (YYYY-MM-DD): "):
    while True:
        user_input = input(prompt)
        try:
            # Try to parse the input into a datetime object
            user_date = datetime.strptime(user_input, "%Y-%m-%d")
            # Format the datetime object to return only the date as string (YYYY-MM-DD)
            formatted_date = user_date.strftime("%Y-%m-%d")
            return formatted_date
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")


#give the valid string command from user
def valid_string_input(user_input):
    while True:
        try:
            int(user_input)
            print("Please enter a name. try again")
            user_input = input().strip()
            break
        except ValueError:
            break
    return user_input


#give the valid number command from user
def valid_number_input(user_input):
    valid_input = 0
    while True:
        try:
            valid_input = int(user_input)
            break
        except ValueError:
            print("Please enter a number. try again")
            user_input = input().strip()
    return valid_input


#creat an account for user
def sign_up():
    global global_user_info

    os.system('cls')
    print("[ SIGN UP ]")
    name = input('Enter your full name \n').strip()
    username = input('Enter user name to creat an account \n').strip()

    while True:
        if not uniq_username(username):
            print('user name already taken choose another one')
            username = input().strip()
        else:
            break

    password = valid_password(input('Enter your password \n').strip())

    global_user_info = {
        "name": name,
        "username": username,
        "password": password,
        "cash": 0,
        "transactions" : []
    }
    append_to_file(global_user_info)
    
    os.system('cls')
    user_menu()

#user sign in to the account
def sign_in():
    global global_user_info

    os.system('cls')
    print("[ SIGN IN ]")
    username = input('Enter your username \n').strip()

    while True: 
        if uniq_username(username):
            username = input("username not found. try again \n").strip()
        else:
            break
    
    password = input('Enter your password \n').strip()
    while True:
        if global_user_info["password"] == password:
            os.system('cls')
            user_menu()
            break
        else:
            password = input('your pass is wrong. try again \n').strip()


#check if the user name is uniq or not
def uniq_username(username):
    global global_user_info

    try:
        with open("account.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
        return True
    for user_data in data:
        if user_data["username"] == username:
            global_user_info = user_data
            return False
        else:
            return True


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
        json.dump(data, file, indent= 5)


#delete a specific object from json and file and write the file 
def delete_from_json():
    global global_user_info

    # Load JSON data from file
    with open('account.json', 'r') as file:
        data = json.load(file)

    # Filter out the object with matching username
    filtered_data = [user for user in data if user.get('username') != global_user_info["username"]]

    # Save updated JSON data back to file
    with open('account.json', 'w') as file:
        json.dump(filtered_data, file, indent=5)

main_menu()