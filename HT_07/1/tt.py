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

import os
import json



def transaction():
    pass

# Checking username & password (is they valid) 
def login(user_name, passwod):
    
    #target_path_1 = os.path.dirname(os.path.abspath(__file__))

    users_database = "users.csv"
    try:
        with open(users_database, "r", encoding="utf-8") as file:
            list_of_users = file.readlines()
            
            for lines in list_of_users:
                lines = lines.split(",")
                #if lines[0] == user_name:
                #if lines[1] == passwod:
                if lines[0] == user_name and lines[1] == passwod:
                    f_result = True
                else:
                    f_result = False
    except FileNotFoundError:
        f_result = False

    return f_result

# 
def view_balance(name):
    print(name)
    #file_name = f"{name}_balance.csv"
    file_name = "thomas_balance.csv"
    with open(file_name, "r", encoding="utf-8") as file:
        xxx = file.readlines()
        print(xxx)
    


def update_balance(x):
    #target_path_1 = os.path.join(os.path.dirname(__file__), x)
    #target_path_1 = open(os.path.join('h222', x), 'r')
    target_path_1 = os.path.dirname(os.path.abspath(__file__))
    return target_path_1


def start():
    # user_name = input("Input your name: ")
    # user_pass = input("Input your password: ")
    user_name = "Thomas"
    user_pass = "ppassww"

    if not login(user_name, user_pass):
        print("Soory, wrong username or password, try again")
    else:
        print("You are logged in, please choose operation")
        oparions = [[1, "Check balance"], [2, "Money operation"], [3, "Exit"]]
        for item in oparions:
            print(f"{item[0]} - {item[1]}")

        user_option = input("Select 1, 2 or 3: ")
        if int(user_option) == 1:
            view_balance(user_name)
        elif int(user_option) == 2:
            update_balance(user_name)
        elif int(user_option) == 3:
            print("You came out, Good luck...")

    return 

start()

#print(update_balance('users.csv'))

#print(login('x', 'y'))
