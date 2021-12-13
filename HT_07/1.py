""" Завдання_1

Програма-банкомат.
Створити програму з наступним функціоналом:
    - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль (файл <users.data>);
    - кожен з користувачів має свій поточний баланс (файл <{username}_balance.data>) 
    та історію транзакцій (файл <{username}_transactions.data>);
    - є можливість як вносити гроші, так і знімати їх. Обов'язкова перевірка введених даних 
    (введено число; знімається не більше, ніж є на рахунку).

Особливості реалізації:
    - файл з балансом - оновлюється кожен раз при зміні балансу (містить просто цифру з балансом);
    - файл - транзакціями - кожна транзакція у вигляді JSON рядка додається в кінець файла;
    - файл з користувачами: тільки читається. Якщо захочете реалізувати функціонал додавання 
    нового користувача - не стримуйте себе :)

Особливості функціонала:
    - за кожен функціонал відповідає окрема функція;
    - основна функція - <start()> - буде в собі містити весь workflow банкомата:
    - спочатку - логін користувача - програма запитує ім'я/пароль. 
    Якщо вони неправильні - вивести повідомлення про це і закінчити роботу 
    (хочете - зробіть 3 спроби, а потім вже закінчити роботу - все на ентузіазмі :) )
    - потім - елементарне меню типа:
    Введіть дію:
        1. Продивитись баланс
        2. Поповнити баланс
        3. Вихід
    - далі - фантазія і креатив :)
    User-friendly буде, якщо ваш банкомат буде продовжувати роботу, 
    доки користувач спеціально не обере меню "завершити роботу".
"""

import pathlib
from pathlib import Path
import time
import json


## Output own mistake (wrong input parameter)
class WrongParameter(Exception):
    pass

# Checking username & password - login procces (is they valid) 
def login(user_name, passwod):
    
    file_path = Path(pathlib.Path.cwd(), "1_files", "users.csv")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            
            list_of_users = file.readlines()
            counter = 0
            f_result = False

            for lines in list_of_users:
                lines = lines.split(",")
                counter += 1

                if counter == len(list_of_users):
                    if lines[0] == user_name and lines[1] == passwod:
                        f_result = True

                elif counter > 1:
                    if lines[0] == user_name and str(lines[1])[:-1] == passwod:
                        f_result = True

    except FileNotFoundError:
        f_result = False

    return f_result

# Check & output user balance
def view_balance(vb_name):

    file_path = Path(pathlib.Path.cwd(), "1_files", f"{vb_name}_balance.csv")
    with open(file_path, "r", encoding="utf-8") as file:
        user_balance = file.readline()

    return user_balance
    
# Updayting user balanse (write to the file)
def update_balance(ub_name):
    
    input_sum = input("Please, input money sum (ex. '+;10' or '-;10'): ")
    input_sum = input_sum.split(";")

    balance_sum = view_balance(ub_name)
    balance_file_path = Path(pathlib.Path.cwd(), "1_files",
                             f"{ub_name}_balance.csv")
    transactions_file_path = Path(pathlib.Path.cwd(), "1_files",
                                  f"{ub_name}_transaction.csv")

    time_in_seconds = time.time()
    trans_time = time.ctime(time_in_seconds)

    # Update user balance in a file & added a new transaction to the file
    if input_sum[0] == "+":

        if int(input_sum[1]) < 0:
            print("#####_Inputed wrong value_#####")
        else:
            new_balance = int(balance_sum) + int(input_sum[1])
            with open(balance_file_path, "w", encoding="utf-8") as file_bal:
                file_bal.write(str(new_balance))
        
            trans_type = "plus"
            new_trans_item = f"{trans_time},{trans_type},{int(input_sum[1])}"

            with open(transactions_file_path, "a", encoding="utf-8") as file_trans:
                json.dump(new_trans_item, file_trans)

            print(f"###Your actual balance now: {view_balance(ub_name)} parrots ;)")

    elif input_sum[0] == "-":

        if abs(int(input_sum[1])) > int(balance_sum):
            print("Inputed to big number")
        elif int(input_sum[1]) > 0:    
            print("#####_Inputed wrong value_#####")
        else:
            new_balance = int(balance_sum) - abs(int(input_sum[1]))
            with open(balance_file_path, "w", encoding="utf-8") as file:
                file.write(str(new_balance))
            
            trans_type = "minus"
            new_trans_item = f"{trans_time},{trans_type},{int(input_sum[1])}"

            with open(transactions_file_path, "a", encoding="utf-8") as file_trans:
                json.dump(new_trans_item, file_trans)

            print(f"###Your actual balance now: {view_balance(ub_name)} parrots ;)")


# ATM menu
def atm_main_manu():
    
    print("Please choose operation")
    time.sleep(0.2)
    oparions = [[1, "Check balance"], [2, "Money operation"], [3, "Exit"]]
    
    for item in oparions:
        print(f"{item[0]} - {item[1]}")
        time.sleep(0.5)

    try:
        user_option = int(input("Select 1, 2 or 3: "))
    except ValueError:
        raise WrongParameter("Wrong input operation")

    return user_option

# ATM workflow   
def start():
    
    # user_name = input("Input your name: ")
    # user_pass = input("Input your password: ")

    user_name = "Bob"
    user_pass = "1234"
    
    if not login(user_name, user_pass):
        print(":::::::::::::::::::::::::::::::::")
        print("Soory, wrong username or password")
        print("Try again::::::::::::::::::::::::")

    else:
        time.sleep(0.2)
        print(".......................")
        print("## You are logged in ##")
        
        # Atm menu & choosen options
        user_option = atm_main_manu()
        menu_flag = True    
        while menu_flag == True:
            
            # Balance
            if user_option == 1:
                print(f"Your balance: {view_balance(user_name)} parrots ;)")
                menu_flag == True
                user_option = atm_main_manu()

            # Money operation
            elif user_option == 2:
                update_balance(user_name)
                menu_flag == True
                user_option = atm_main_manu()

            # Exit
            if user_option == 3:
                menu_flag = False
                print("You came out, Good luck...")

    return

# Function implementation
start()