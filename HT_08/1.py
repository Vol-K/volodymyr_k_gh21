""" Завдання_1

Доповніть програму-банкомат з попереднього завдання таким функціоналом, 
як використання банкнот.
Отже, у банкомата повинен бути такий режим як "інкассація", за допомогою 
якого в нього можна "загрузити" деяку кількість банкнот (вибирається 
номінал і кількість). 
Зняття грошей з банкомату повинно відбуватись в межах наявних банкнот за 
наступним алгоритмом - видається мінімальна кількість банкнот наявного 
номіналу (починаючи з більшого). 

P.S. Будьте обережні з використанням "жадібного" алгоритму (коли вибирається 
спочатку найбільша банкнота, а потім - наступна за розміром і т.д.) - 
в деяких випадках він працює неправильно або не працює взагалі. 
Наприклад, якщо треба видати 160 грн., а в наявності є банкноти 
номіналом 20, 50, 100, 500,  банкомат не зможе видати суму 
(бо спробує видати 100 + 50 + (невідомо), а потрібно було 100 + 20 + 20 + 20 ).

Особливості реалізації:
- перелік купюр: 10, 20, 50, 100, 200, 500, 1000;
- у одного користувача повинні бути права "інкасатора". 
Відповідно і у нього буде своє власне меню із пунктами:
- переглянути наявні купюри;
- змінити кількість купюр;
- видача грошей для користувачів відбувається в межах наявних купюр;
- якщо гроші вносяться на рахунок - НЕ ТРЕБА їх розбивати і вносити 
  в банкомат - не ускладнюйте собі життя, та й, наскільки я розумію, 
  банкомати все, що в нього входить, відкладає в окрему касету.
"""

# список транзакцій для інкасатора
# список інкасацій для інкасатора

# при знатті юзером бабла - вивод кіклькості купюр

import pathlib
from pathlib import Path
import time
import json

# ATM Login proccess, for 2 types of account (user & incasator)
def login(login_name, login_password):
    users_file_path = Path(pathlib.Path.cwd(), "volodymyr_k_gh21", "HT_08", "1_files", "users_db.csv")
    
    try:
        with open(users_file_path, "r", encoding="utf-8") as users_file:
            user_list = users_file.readlines()
            
            if len(user_list) == 1:
                check_result = False
                user_type = False
            
            else:    
                check_result = False
                user_type = False

                for i in range(1, len(user_list)):
                    user = user_list[i].split(",")
                    if i == (len(user_list) - 1):
                        if user[1] == login_name and str(user[2]) == login_password:
                            check_result = True
                            user_type = user[0]
                    else:
                        if user[1] == login_name and str(user[2])[:-1] == login_password:
                            check_result = True
                            user_type = user[0]

    except FileNotFoundError:
        check_result = False
        user_type = False
    
    return check_result, user_type


# Check the current user balance
def view_balance_of_user(inp_name):

    user_bal_file_path = Path(pathlib.Path.cwd(), "volodymyr_k_gh21", "HT_08", "1_files", f"{inp_name}_balance.csv")
    with open(user_bal_file_path, "r", encoding="utf-8") as ub_file:
        user_balance = ub_file.readline()

    return user_balance


# 
def cash_in_operation():
    pass


# ATM menu for both account type (user & incasator)
def atm_menu(atm_user, user_status):
    
    print("Please choose one operation from this list")
    #time.sleep(0.2)

    if user_status == "incasator":
        
        incasator_menu = [[1, "Check banknots"], [2, "Cash-in (CVIT)"], [3, "Exit"]]
        oper_flag = False

        while not oper_flag:
            for item in incasator_menu:
                print(f"{item[0]} - {item[1]}")
                #time.sleep(0.5)

            user_option = input("Select 1, 2 or 3: ")
            oper_flag = check_atm_option(user_option)
        
    elif user_status == "user":

        user_oparions = [[1, "Check balance"], [2, "Money operation"], [3, "Exit"]]
        oper_flag = False

        while not oper_flag:
            for item in user_oparions:
                print(f"{item[0]} - {item[1]}")
                #time.sleep(0.5)

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


# Recharge ATM by the new banknots
def incasator_operation():
    banknots_file_path = Path(pathlib.Path.cwd(), "volodymyr_k_gh21", "HT_08", "1_files", "banknots.txt")
    with open(banknots_file_path, "r", encoding="utf-8") as banknots_file:
        banknots_status = banknots_file.readline()

        print(banknots_status)
        print(type(banknots_status))
        banknots_status = dict(banknots_status)
        print(banknots_status)
    
        #print(f"Your balance: {view_balance_of_user(user_name)} parrots ;)")
    ten_new = 0
    twenty_new = 0
    fifty_new = 0
    handred_new = 0
    two_hand_new = 0
    half_th_new = 0
    thousand_new = 0

    banknots_update = (f'{"10":{ten_new}, \
                        "20":{twenty_new}, \
                        "50":{fifty_new}, \
                        "100":{handred_new}, \
                        "200":{two_hand_new}, \
                        "500":{half_th_new}, \
                        "1000":{thousand_new},}')
                        


def atm_workflow():
    # user_name = input("Input your name: ")
    # user_pass = input("Input your password: ")
    user_name = "Jon"
    user_pass = "43210"

    user_check_result = login(user_name, user_pass)
    
    if not user_check_result[0]:
        print(":::::::::::::::::::::::::::::::::")
        print("Soory, wrong username or password")
        print("Try again::::::::::::::::::::::::")
    #
    else:
        time.sleep(0.2)
        print(".......................")
        print("## You are logged in ##")
        # Incasator side
        if user_check_result[1] == "incasator":
            print("___ADMIN____")

        # User side
        elif user_check_result[1] == "user":
            
            user_atm_menu = atm_menu(user_check_result[0], user_check_result[1])
            exit_flag = False    

            while exit_flag == False:

                if int(user_atm_menu[1]) == 1:
                    print(f"Your balance: {view_balance_of_user(user_name)} USD ;)")
                    menu_flag = False
                    user_atm_menu = atm_menu(user_check_result[0], user_check_result[1])
                    
                elif int(user_atm_menu[1]) == 2:
                    balance_operation(user_name)
                    menu_flag = False
                    user_atm_menu = atm_menu(user_check_result[0], user_check_result[1])

                elif int(user_atm_menu[1]) == 3:
                    menu_flag = True
                    print("You came out, Good luck...")
    
    return

atm_workflow()