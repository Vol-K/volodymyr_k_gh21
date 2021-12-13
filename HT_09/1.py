""" Завдання_1

Перепишіть програму-банкомат на використання бази даних для збереження всих даних.
Використовувати БД sqlite3 та натівний Python.

Дока з прикладами: https://docs.python.org/3/library/sqlite3.html
Туторіал (один із): https://www.sqlitetutorial.net/sqlite-python/

Для уніфікації перевірки, в базі повинні бути 3 користувача:
    ім'я: user1, пароль: user1
    ім'я: user2, пароль: user2
    ім'я: admin, пароль: admin (у цього коритувача - права інкасатора)
"""

import pathlib
from pathlib import Path
import time
import sqlite3


# Connect for database
# database_file_path = Path(pathlib.Path.cwd(), "atm_database.db")
database_file_path = Path(pathlib.Path.cwd(), "volodymyr_k_gh21", "HT_09", "atm_database.db")
db = sqlite3.connect(database_file_path, check_same_thread=False)
db = db.cursor()


# ATM Login proccess, for 2 types of account (user & incasator)
def login(login_name, login_password):

    check_result = False
    user_type = False
    check_user = db.execute("SELECT * FROM users WHERE name=? AND password=?",\
                            (login_name, login_password)).fetchone()

    if check_user != None:
        check_result = True
        user_type = check_user[3]
  
    return check_result, user_type


# Check the current user balance
def view_balance_of_user(inp_name):
    user_balance = db.execute("SELECT user_balance FROM balances WHERE user_name=?", (inp_name,)).fetchone()
                        
    return user_balance


# ATM menu for both account type (user & incasator)
def atm_menu(user_status):

    print("...................................................")
    print("Please choose one operation from this list")
    time.sleep(0.2)

    if user_status == "admin":
        
        incasator_menu = [[1, "Check banknots"], [2, "Cash-in (CVIT)"], [3, "Exit"]]
        oper_flag = False

        for item in incasator_menu:
            print(f"{item[0]} - {item[1]}")
            time.sleep(0.5)

        user_option = input("Select 1, 2 or 3: ")
        oper_flag = check_atm_option(user_option)
        
    elif user_status == "user":

        user_oparions = [[1, "Check balance"], [2, "Money operation"], [3, "Exit"]]
        oper_flag = False

        for item in user_oparions:
            print(f"{item[0]} - {item[1]}")
            time.sleep(0.5)

        user_option = input("Select 1, 2 or 3: ")
        oper_flag = check_atm_option(user_option)

    return user_status, user_option, oper_flag


# Validation of chosen menu option
def check_atm_option(inp_option):
    granted_symbols = "123"

    if len(inp_option) != 1:
        f_result = False
    elif inp_option not in granted_symbols:
        f_result = False
    else:
        f_result = True

    return f_result


# Checkin availability of banknots inside ATM
def check_banknots():
    
    banknots_status = db.execute("SELECT * FROM banknots").fetchall()
    print("...................................................")
    time.sleep(0.2)
    print("### Available banknots in ATM ###")
    print("### Nominal: Quantity ###")
    
    for item in banknots_status:
        print('{:<4}: {}'.format(item[0], item[1]))
        time.sleep(0.2)


# ATM logic
def atm_workflow():

    # user_name = input("Input your name: ")
    # user_pass = input("Input your password: ")
    user_name = "admin"
    user_pass = "admin"

    user_check_result = login(user_name, user_pass)
    enter_flag = False

    if user_check_result[0]:
            enter_flag = True

    while not enter_flag:
        print(":::::::::::::::::::::::::::::::::")
        print("Soory, wrong username or password")
        print("Try again::::::::::::::::::::::::")

        user_name = input("Input your name: ")
        user_pass = input("Input your password: ")
        user_check_result = login(user_name, user_pass)
        print(user_check_result)

        if user_check_result[0]:
            enter_flag = True

    time.sleep(0.2)
    print("...................................................")
    print(f"## Hello, '{user_name}' You are logged in. ##")

    # 'Incasator' side of ATM menu
    if user_check_result[1] == "admin":
        print("__ADMIN__")
        admin_atm_menu = atm_menu(user_check_result[1])
        exit_flag = False 

        while exit_flag == False:
            if not admin_atm_menu[2]:
                print("Soory, inputed wrong symbols")
                admin_atm_menu = atm_menu(user_check_result[1])
                
            elif int(admin_atm_menu[1]) == 1:
                check_banknots()
                admin_atm_menu = atm_menu(user_check_result[1])

            # elif int(admin_atm_menu[1]) == 2:
            #     cash_in_operation()
            #     admin_atm_menu = atm_menu(user_check_result[0], user_check_result[1])

            elif int(admin_atm_menu[1]) == 3:
                exit_flag = True
                print("...................................................")
                print("..............You came out, Good luck..............")
                print("...................................................")

    # 'User' side of ATM menu
    elif user_check_result[1] == "user":

        user_atm_menu = atm_menu(user_check_result[1])
        exit_flag = False    

        while exit_flag == False:
            if not user_atm_menu[2]:
                print("Soory, inputed wrong symbols")
                user_atm_menu = atm_menu(user_check_result[1])

            elif int(user_atm_menu[1]) == 1:
                print("...................................................")
                print(f"Your balance: {view_balance_of_user(user_name)[0]} USD")
                user_atm_menu = atm_menu(user_check_result[1])
                
            # elif int(user_atm_menu[1]) == 2:
            #     user_balance_operation(user_name)

            #     user_atm_menu = atm_menu(user_check_result[1])

            elif int(user_atm_menu[1]) == 3:
                exit_flag = True
                print("...................................................")
                print("..............You came out, Good luck..............")
                print("...................................................")
    
    return

atm_workflow()