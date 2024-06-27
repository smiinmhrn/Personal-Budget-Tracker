#BUGS TO FIX RIMINDER


# IF THE AMOUNT OF USER CASH IS NOT ENOUGH FOR COST THEN WHAT ?
# CATEGORIES MANAGEMENT -> has bug in delet



from enum import Enum
import os
import json
import re
import keyboard
import datetime
import time

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

global_user_info = {}

def main_menu():
    #print the menu
    print(FirstMenu.SIGN_UP.value[0], FirstMenu.SIGN_IN.value[0], FirstMenu.EXIST.value[0], sep='\n')

    #get the command
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
    
    print(UserMenu.TRANSACTION_REGISTRATION.value[0], UserMenu.MANAGE_CATEGORIES.value[0],
           UserMenu.BILL.value[0], UserMenu.STATISTICS_AND_REPORTING.value[0], UserMenu.BACK.value[0], sep='\n')
    
    choice = valid_number_input(input("choose your command...\n"))

    while True:
            if choice == UserMenu.TRANSACTION_REGISTRATION.value[1]:
                Transaction_registration()
                break
            elif choice == UserMenu.MANAGE_CATEGORIES.value[1]:
                mange_categories()
                break
            elif choice == UserMenu.BILL.value[1]:
                show_bill()
                break
            elif choice == UserMenu.STATISTICS_AND_REPORTING.value[1]:
                reportes()
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
            if transaction_type == 1:
                transaction_type = "Income"
            else:
                transaction_type = "Cost"
            break

    #give the info of transaction from user 
    receiver = valid_string_input(input("enter the name of receiver: "))
    depositor = valid_string_input(input("enter the name of depositor: "))
    amount = valid_money_input()
    date = str(get_user_date())
    category = get_category_input()

    #make a dictionary of it to save
    transactions = {
        "type": transaction_type,
        "reciver": receiver,
        "depositor": depositor,
        "amount": amount,
        "date": date,
        "category": category,
    }


    #check if the transaction is income increase the user cash else decrease it and update the user cash
    if transaction_type == "Income" :
        global_user_info["cash"] = global_user_info["cash"] + amount
    else:
        global_user_info["cash"] = global_user_info["cash"] - amount
    
    #for finding the max cash in the account
    if global_user_info["cash"] > global_user_info["maxCash"]:
        global_user_info["maxCash"] = global_user_info["cash"]
    
    #for finding the min cash in the account
    if global_user_info["cash"] < global_user_info["minCash"]:
        global_user_info["minCash"] = global_user_info["cash"]

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


#use to print the category list
def print_categories():
    for index, category in enumerate(global_user_info["categories"], start=1):
        print(f"{index}. {category}")
    print()


#do the mange categories option in user menu
def mange_categories():
    os.system("cls")
    print("[ ACCESSIBLE CATEGORIES ]")
    print("The category list is as follows: \n")
    print_categories()

    user_activity = valid_number_input(input("1.Add          2.Delete          3.Edit          4.Back \nchoose your action: "))

    while True:
        if user_activity >= 1 and user_activity <= 4:
            break
        else:
            user_activity = valid_number_input(input("choose from options above \n"))
    
    if user_activity == 1:
       add_new_category()
       back_perivious("New category added successfully.")
    elif user_activity == 2:
        remove_category()
    elif user_activity == 3:
        edit_category()
    else:
        os.system("cls")
        user_menu()


#let user to customis the category list by adding new categories
def add_new_category():
    new_category = valid_string_input(input("Enter the name of the new category: ").lower())

    while True:
        if new_category in global_user_info["categories"]:
            new_category = valid_string_input(input("This name of category already used enter another name for new category: ").lower())
        else:
            global_user_info["categories"].append(new_category)
            delete_from_json()
            append_to_file(global_user_info)
            break


#let user to remove a aspecial category
def remove_category():
    deleted_category = valid_string_input(input("Enter the name of the category that want to delete: ").lower())

    while True:
        if deleted_category in global_user_info["categories"]:
            print("ATTENTION -> If you delete this, all of your transactions in this category will be deleted.")
            confirm = input("Are you sure? Y/N\n").lower()

            while True:
                if confirm == "y":
                    print("The action will proceed.")
                    time.sleep(1)

                    filtered_transactions = [transaction for transaction in global_user_info["transactions"] 
                                             if transaction['category'] != deleted_category]
                    
                    global_user_info["transactions"] = filtered_transactions
                    global_user_info["categories"].remove(deleted_category)
    
                    print("delete succsefully")
                    break
                elif confirm == "n":
                    print("The action is cancelled.")
                    time.sleep(1)
                    break
            
            delete_from_json()
            append_to_file(global_user_info)
            break
        else:
            deleted_category = valid_string_input(input("This name of the category does not exitsted. try again").lower())

    time.sleep(0.5)
    back_perivious("")


#let user to edit name of the category
def edit_category():
    edit_category = valid_string_input(input("Enter the name of the category to edit: ").lower())

    while True:
        if edit_category in global_user_info["categories"]:
            new_name = valid_string_input(input("Enter the new name of this category: ").lower())

            while True:
                if new_name in global_user_info["categories"]:
                    new_name = valid_string_input(input("This name of category is already existed. choose another: ").lower())
                else:
                    for transaction in global_user_info["transactions"]:
                        if transaction["category"] == edit_category:
                            transaction["category"] = new_name

                    global_user_info["categories"].remove(edit_category)
                    global_user_info["categories"].append(new_name)

                    delete_from_json()
                    append_to_file(global_user_info)
                    break

            break
        else:
            edit_category = valid_string_input(input("This category does not existed. try again: ").lower())
    
    back_perivious("Category edited succesfully.")


#access the user to show and do other actions or back to previous menue for manage categories
def back_perivious(input_string):
    command = valid_number_input(input(input_string + "\n1. Do other actions          2. Back to perivious menu\n"))

    while True:
        if command != 1 and command != 2:
            command = valid_number_input(input("choose from options above \n"))
        else: 
            break
    
    if command == 1:
        os.system('cls')
        mange_categories()
    else:
        os.system('cls')
        user_menu()


#get the category from defualt or add new
def get_category_input():
    print("Choose the category you want: ")

    print_categories()

    user_category = valid_number_input(input("choose from above     or     0. add more \n"))

    while True:
        if user_category >= 0 and user_category <= len(global_user_info["categories"]):
            break
        else:
            user_category = valid_number_input(input("choose from options above \n"))
    
    if user_category == 0:
        add_new_category()
        return global_user_info["categories"][len(global_user_info["categories"]) - 1]
    return global_user_info["categories"][user_category - 1]


#show the number of bills that user wanted
def show_bill():

    os.system('cls')
    print("[ SHOW BILL ]")

    if not trasaction_existed():
        print("THER IS NO TRANSACTION EXISTED\n")
    else:
        result = []

        #show the transactions base on user expectation
        choice_the_type = valid_number_input(input("which bills you want to see?\n1. Incomes          2. Costs          3. all\n"))

        while True:
            if choice_the_type != 1 and choice_the_type != 2 and choice_the_type != 3:
                choice_the_type = valid_number_input(input("choose from options above \n"))
            else:
                if choice_the_type == 1:
                    choice_the_type = "Income"
                    result = filter(choice_the_type, global_user_info["transactions"])

                elif choice_the_type == 2:
                    choice_the_type = "Cost"
                    result = filter(choice_the_type, global_user_info["transactions"])
                else:
                    result = global_user_info["transactions"]
                break

        
        choice_to_prnit = valid_number_input(input("how many bill you want to see?\n1. 10          2. 50          3. all\n"))

        while True:
            if choice_to_prnit != 1 and choice_to_prnit != 2 and choice_to_prnit != 3:
                choice_to_prnit = valid_number_input(input("choose from options above \n"))
            else:
                if choice_to_prnit == 1:
                    result = number_of_bill(10, result)
                elif choice_to_prnit == 2:
                    result = number_of_bill(50, result)
                break
        
        
        choice_to_sort = valid_number_input(input("How do you want to sort by the amount?\n1. ascending          2. Descending          3. Dont\n"))

        while True:
            if choice_to_sort != 1 and choice_to_sort != 2 and choice_to_sort != 3:
                choice_to_sort = valid_number_input(input("choose from options above \n"))
            else:
                if choice_to_sort == 1:
                    result = sorted(result, key=lambda x: x['amount']) 
                elif choice_to_sort == 2:
                    result = sorted(result, key=lambda x: x['amount'], reverse=True)
                break
        
        
        #clean the consol and print the total cash, total incomes, total costs and all filterd transactions
        os.system("cls")
        print(f"Total Cash : {total_user_transactions()[2]}")
        print(f"Total Incomes : {total_user_transactions()[0]}          Total Costs : {total_user_transactions()[1]} \n")
        print_array_of_dict(result)


    #access the user to show again the transcations or back to previous menue
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
        user_menu()


#show the report part of the menu
def reportes():
    os.system('cls')
    print("[ STATISTICS AND REPORTING ]\n")

    #sure that the user has transactiones or not and print the result 
    if not trasaction_existed():
        print("There is no transaction existed\n".upper())
    else:
        find_min_max_month_day_cost_and_income(True, "Day")
        find_min_max_month_day_cost_and_income(False, "Month")

        print("================================================\n")
        #print the most and least money that existed in account
        print(f'The maximum of the account cash is {global_user_info["maxCash"]}')
        print(f'The minimum of the account cash is {global_user_info["minCash"]}\n')

    #access the user back to previous menue
    command = valid_number_input(input("1. Back\n"))

    while True:
        if command != 1:
            command = valid_number_input(input("choose from option above \n"))
        else: 
            break
    
    if command == 1:
        os.system('cls')
        user_menu()


#show if user hase transactiones or not
def trasaction_existed():
    if len(global_user_info["transactions"]) == 0:
        return False
    return True


#find the max and min incomes and costs in days and monthes
def find_min_max_month_day_cost_and_income(day, string):
    #creat a matrix like this for days
    #date         costs         incomes
    #2024-02-02   200             0
    #2023-02-02   200             500

    #creat a matrix like this for monthes
    #date     costs         incomes
    #2024-02   200             0
    #2023-02   200             500

    date_matrix = [["date", "costs", "incomes"]]

    for transaction in global_user_info["transactions"]:
        date = transaction["date"]
        if not day:
            #cut the 2024-02 part of the day
            date = date[:7]
            
        row_index, exists = string_exists_in_matrix(date_matrix, date)

        #sum the costs and incomes if the date existed before
        if exists:
            if transaction["type"] == "Cost":
                date_matrix[row_index][1] += int(transaction["amount"])
            else:
                date_matrix[row_index][2] += int(transaction["amount"])
            
        else:
            if transaction["type"] == "Cost":
                date_matrix.append([date, int(transaction["amount"]), 0])
            else:
                date_matrix.append([date, 0, int(transaction["amount"])])
    
    #return non if the column of costs or incomes are completely 0 which means there is no transactions in costs or incomes
    #return the index of the max and min values of the cost and incomes and then find it in matrix and print the date of it

    cost_indices = find_min_and_max(1, date_matrix)

    print(f"[ {string.upper()} ]")
    if cost_indices == None:
        print("There is no transaction in cost section\n")
    else:
        most_cost_dates = [date_matrix[index + 1][0] for index in cost_indices[0]]
        print(f"The most cost {string} is:", ", ".join(most_cost_dates))

        min_cost_dates = [date_matrix[index + 1][0] for index in cost_indices[1]]
        print(f"The min cost {string} is:", ", ".join(min_cost_dates) + "\n")


    income_indices = find_min_and_max(2, date_matrix)

    print(f"[ {string.upper()} ]")
    if income_indices == None:
        print("There is no transaction in income section\n")
    else:
        most_income_dates = [date_matrix[index + 1][0] for index in income_indices[0]]
        print(f"The most income {string} is:", ", ".join(most_income_dates))

        min_income_dates = [date_matrix[index + 1][0] for index in income_indices[1]]
        print(f"The min income {string} is:", ", ".join(min_income_dates) + "\n")


def string_exists_in_matrix(matrix, target_string):
    for index, row in enumerate(matrix):
        if target_string in row:
            return index, True
    return -1, False


def find_min_and_max(column_index, matrix):
    column = [row[column_index] for row in matrix[1:]]  # Exclude header row

    if all_elements_are_zero(column):
        return None
    else:
        max_element = max(column)
        min_element = min(column)

        max_indices = [i for i, x in enumerate(column) if x == max_element]
        min_indices = [i for i, x in enumerate(column) if x == min_element]

        return max_indices, min_indices


def all_elements_are_zero(array):
    for element in array:
        if element != 0:
            return False
    return True 


#return the totall amount of each transactions and all users money as touple 
def total_user_transactions():
    Incomes = 0
    Costs = 0
    for transaction in global_user_info["transactions"]:
        if transaction["type"] == "Income":
            Incomes = Incomes + transaction["amount"]
        else:
            Costs = Costs + transaction["amount"]
    return (Incomes, Costs, global_user_info["cash"])


#print the dictionary in column way base on the keys
def print_array_of_dict(dict_array):
    # Determine the maximum width for each key
    keys = dict_array[0].keys()
    max_widths = {key: max(len(str(key)), max(len(str(d[key])) for d in dict_array)) for key in keys}
    
    # Print the header
    header = "     ".join(f"{key:<{max_widths[key]}}" for key in keys)
    print(header)
    print("=" * len(header))
    
    # Print each transaction in column format
    for transaction in dict_array:
        print("     ".join(f"{str(value):<{max_widths[key]}}" for key, value in transaction.items()))


#return the number of transaction that user wanted
def number_of_bill(number_of_bill, info_array):
    if number_of_bill >= len(info_array):
        return info_array
    else:
        return info_array[-number_of_bill:]


#filter and return the transactons base on incomes or costs
def filter(to_filter, info_array):
    if to_filter == "Income":
        info_array = [transaction for transaction in info_array if transaction["type"] == "Income"]
    else:
        info_array = [transaction for transaction in info_array if transaction["type"] == "Cost"]
    return info_array


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
def get_user_date(prompt="Enter a date (YYYY-MM-DD): "):
    while True:
        user_input = input(prompt)
        try:
            # Use datetime.datetime.strptime to parse the input into a datetime object
            user_date = datetime.datetime.strptime(user_input, "%Y-%m-%d")
            # Return the formatted date as a string
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
        "maxCash": 0,
        "minCash": 0,
        "categories": ["food", "wearing", "trasports"],
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
            file_content = file.read().strip()
            if not file_content:  # Check if the file is empty
                return True
            data = json.loads(file_content)
    except FileNotFoundError:
        data = []
        return True
    
    for user_data in data:
        if user_data["username"] == username:
            global_user_info = user_data
            return False
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
            file_content = file.read().strip()
            if file_content:
                data = json.loads(file_content)
            else:
                data = []
    except FileNotFoundError:
        # If file doesn't exist, initialize with an empty list
        data = []

    # Append new data to existing list
    data.append(new_data)

    # Write updated data back to file
    with open("account.json", "w") as file:
        json.dump(data, file, indent=2)


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
        json.dump(filtered_data, file, indent=2)

main_menu()