from enum import Enum

class FirstMenu(Enum):
    SIGN_IN = ("1. Sign In", 1)
    SIGN_OUT = ("2. Sign Out", 2)
    EXIST = ("3. Exist", 3)

def main_menu():
    #print the menu
    print(FirstMenu.SIGN_IN.value[0], FirstMenu.SIGN_OUT.value[0], FirstMenu.EXIST.value[0], 'choose your command...', sep='\n')

    #give the command
    choice = valid_command()

    #match the options with user choice
    while True:
        if choice == FirstMenu.SIGN_IN.value[1]:
            print('1')
            break
        elif choice == FirstMenu.SIGN_OUT.value[1]:
            print('2')
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
        user_input = input()
        try:
            valid_input = int(user_input)
            break
        except ValueError:
            print("Invalid command. choose another one")
    return valid_input

main_menu()