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
    users_file_path = Path(pathlib.Path.cwd(), "1_files", "users_db.csv")
    
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

    user_bal_file_path = Path(pathlib.Path.cwd(), "1_files", f"{inp_name}_balance.csv")
    with open(user_bal_file_path, "r", encoding="utf-8") as ub_file:
        user_balance = ub_file.readline()

    return user_balance


# ATM menu for both account type (user & incasator)
def atm_menu(atm_user, user_status):

    print("...................................................")
    print("Please choose one operation from this list")
    time.sleep(0.2)

    if user_status == "incasator":
        
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


# Operation by user balance (adding & withdrawing money)
def user_balance_operation(ub_name):

    input_sum = input("Please, input money sum (ex. '+;10' or '-;10'): ")
    input_sum = input_sum.split(";")

    balance_sum = view_balance_of_user(ub_name)
    balance_file_path = Path(pathlib.Path.cwd(), "1_files",
                             f"{ub_name}_balance.csv")
    transactions_file_path = Path(pathlib.Path.cwd(), "1_files",
                                  f"{ub_name}_transaction.csv")

    time_in_seconds = time.time()
    transaction_time = time.ctime(time_in_seconds)

    # Update user balance in a file & added a new transaction to the file
    if input_sum[0] == "+":

        if int(input_sum[1]) < 0:
            print("#####_Inputed wrong value_#####")
        else:
            new_balance = int(balance_sum) + int(input_sum[1])
            with open(balance_file_path, 'w', encoding="utf-8") as file_bal:
                file_bal.write(str(new_balance))
        
            trans_type = "plus"
            new_trans_item = f"{transaction_time},{trans_type},{int(input_sum[1])}"

            with open(transactions_file_path, 'a', encoding="utf-8") as file_trans:
                file_trans.write("\n")
                json.dump(new_trans_item, file_trans)

            print("_________________________")
            print(f"###Your actual balance now: {view_balance_of_user(ub_name)} USD")

    elif input_sum[0] == "-":

        if abs(int(input_sum[1])) > int(balance_sum):
            print("Inputed less than you have")
        elif int(input_sum[1]) < 0:    
            print("#####_Inputed wrong value_#####")
        elif (int(input_sum[1]) % 10) > 0:
            print("Please, input number divided by 10")
        else:
             
            ckecking_banknots = output_banknot_algorithm(input_sum[1])
            if not ckecking_banknots[1]:
                print("...................................................")
                print("")
                print("### Please, ATM can not withdraw this sum ###")
                print("### Please, input smoller number")
                print("")
            
            else:
                new_balance = int(balance_sum) - abs(int(input_sum[1]))
                with open(balance_file_path, 'w', encoding="utf-8") as file:
                    file.write(str(new_balance))

                trans_type = "minus"
                new_trans_item = f"{transaction_time},{trans_type},{int(input_sum[1])}"

                with open(transactions_file_path, 'a', encoding="utf-8") as file_trans:
                    file_trans.write("\n")
                    json.dump(new_trans_item, file_trans)
                    
                banknots_for_print = list(ckecking_banknots[0].items())
                for elem in banknots_for_print:
                    print("Nominal '{}' USD; Quantity - {} banknot/s".format(elem[0], elem[1]))
                               
                # Update banknots numbers after operation
                update_banknots_by_user_operation(ckecking_banknots[0])
                print("_________________________")
                print(f"###Your actual balance now: {view_balance_of_user(ub_name)} USD")


# Algorithm of cash withdrawal for user (from MAX banknot to MIN)
def output_banknot_algorithm(inp_value):
    
    inp_value = int(inp_value)
    banknots_for_withdrawal = {}

    banknots_file_path = Path(pathlib.Path.cwd(), "1_files", "banknots.txt")
    with open(banknots_file_path, "r", encoding="utf-8") as banknots_file:
        banknots_status = banknots_file.readline()
        banknots_status = json.loads(banknots_status)

        banknots = list(banknots_status.items())
        list_for_algorithm = []
        total_atm_money = 0

        # Quantity of banknots available for withdrawal
        # find a start position
        for item in banknots:
            if int(item[0]) <= inp_value and item[1] > 0:
                list_for_algorithm.append(item)
                total_atm_money += (int(item[0]) * item[1])
        list_for_algorithm.reverse()

        #backup = list_for_algorithm.copy()

        etalon = list_for_algorithm.copy()
        temp_listt = []
        nickelback = 0
        status_of_operation = False
        start_flag = False
        end_algorithm_flag = False
        while not end_algorithm_flag:
            
            if len(list_for_algorithm) < 1 or total_atm_money < inp_value:
                end_algorithm_flag = True
                banknots_for_withdrawal = {"10": 0, 
                                            "20": 0, 
                                            "50": 0, 
                                            "100": 0, 
                                            "200": 0, 
                                            "500": 0, 
                                            "1000": 0}

            else:    
                for element in list_for_algorithm:
                        
                    if not start_flag:
                        quant_for_insert = inp_value // int(element[0])
                        
                        if quant_for_insert <= element[1]:
                            nickelback = inp_value % int(element[0])
                            temp_listt.append([element[0], quant_for_insert])
                        else:
                            quant_for_insert = element[1]
                            nickelback = (inp_value % int(element[0])) + int(element[0])
                            temp_listt.append([element[0], quant_for_insert])

                        start_flag = True

                    elif nickelback >= int(element[0]):
                        quant_for_insert = nickelback // int(element[0])
                        
                        if quant_for_insert <= element[1]:
                            nickelback = nickelback % int(element[0])
                            temp_listt.append([element[0], quant_for_insert])
                        else:
                            quant_for_insert = element[1]
                            nickelback = (inp_value % int(element[0])) + int(element[0])
                            temp_listt.append([element[0], quant_for_insert])

                if nickelback != 0:
                    if len(list_for_algorithm) >= 2:
                        list_for_algorithm.pop(1)
                        nickelback = 0
                        temp_listt.clear()
                        start_flag = False
                    elif len(list_for_algorithm) == 1:
                        nickelback = 0
                        temp_listt.clear()
                        list_for_algorithm = etalon.copy()
                        list_for_algorithm.pop(0)
                        etalon.pop(0)
                        start_flag = False
                            
                elif nickelback == 0:
                    end_algorithm_flag = True
                    banknots_for_withdrawal = dict(temp_listt)
                    status_of_operation = True

    return banknots_for_withdrawal, status_of_operation

# Update status of available banknots inside ATM
def update_banknots_by_user_operation(banknots_dict):

    banknots_file_path = Path(pathlib.Path.cwd(), "1_files", "banknots.txt")
    with open(banknots_file_path, "r+", encoding="utf-8") as banknots_file_update:
        old_banknots_status = banknots_file_update.readline()
        old_banknots_status = json.loads(old_banknots_status)

        list_banknots_for_withdrawal = banknots_dict.keys()

        for i in list_banknots_for_withdrawal:
            new_quantity = old_banknots_status[i] - banknots_dict[i]
            old_banknots_status[i] = new_quantity
        
        # Wright changes
        banknots_file_update.seek(0)
        json.dump(old_banknots_status, banknots_file_update)


# Recharge ATM by the new banknots
def cash_in_operation():

    print("...................................................")
    print("#### Cash-in (CVIT) operations ####")
    inp_nominal_quantity = input("Please, input banknot nomial & quantity for added to ATM (ex. '10';21): ")
    inp_nominal_quantity = inp_nominal_quantity.split(";")

    banknots_file_path = Path(pathlib.Path.cwd(), "1_files", "banknots.txt")
    with open(banknots_file_path, "r+", encoding="utf-8") as banknots_file:
        banknots_status = banknots_file.readline()
        banknots_status = json.loads(banknots_status)

        
        old_quantity = banknots_status[inp_nominal_quantity[0]]
        new_quantity = (old_quantity + int(inp_nominal_quantity[1]))    
        banknots_status[inp_nominal_quantity[0]] = new_quantity
        
        # Wright changes
        item = banknots_status[inp_nominal_quantity[0]]
        banknots_file.seek(0)
        json.dump(banknots_status, banknots_file)
        print("...................................................")
        print(f"A new quantity of banknots nominal '{inp_nominal_quantity[0]}': {item} items")


# Checkin availability of banknots inside ATM
def check_banknots():
    
    banknots_file_path = Path(pathlib.Path.cwd(), "1_files", "banknots.txt")
    with open(banknots_file_path, "r", encoding="utf-8") as banknots_file:
        banknots_status = banknots_file.readline()
        banknots_status = json.loads(banknots_status)
        
        print("...................................................")
        #time.sleep(0.2)
        print("### Available banknots in ATM ###")
        print("### Nominal: Quantity ###")
        for x, y in banknots_status.items():
            print(f"'{x}': ", y)
 

# ATM logic
def atm_workflow():

    user_name = input("Input your name: ")
    user_pass = input("Input your password: ")

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

        if user_check_result[0]:
            enter_flag = True

    time.sleep(0.2)
    print("...................................................")
    print(f"## Hello, '{user_name}' You are logged in. ##")

    # 'Incasator' side of ATM menu
    if user_check_result[1] == "incasator":

        admin_atm_menu = atm_menu(user_check_result[0], user_check_result[1])
        exit_flag = False 

        while exit_flag == False:
            if not admin_atm_menu[2]:
                print("Soory, inputed wrong symbols")
                admin_atm_menu = atm_menu(user_check_result[0], user_check_result[1])
                
            elif int(admin_atm_menu[1]) == 1:
                check_banknots()
                admin_atm_menu = atm_menu(user_check_result[0], user_check_result[1])

            elif int(admin_atm_menu[1]) == 2:
                cash_in_operation()
                admin_atm_menu = atm_menu(user_check_result[0], user_check_result[1])

            elif int(admin_atm_menu[1]) == 3:
                exit_flag = True
                print("...................................................")
                print("..............You came out, Good luck..............")
                print("...................................................")

    # 'User' side of ATM menu
    elif user_check_result[1] == "user":
        
        user_atm_menu = atm_menu(user_check_result[0], user_check_result[1])
        exit_flag = False    

        while exit_flag == False:
            if not user_atm_menu[2]:
                print("Soory, inputed wrong symbols")
                user_atm_menu = atm_menu(user_check_result[0], user_check_result[1])

            elif int(user_atm_menu[1]) == 1:
                print("...................................................")
                print(f"Your balance: {view_balance_of_user(user_name)} USD")
                user_atm_menu = atm_menu(user_check_result[0], user_check_result[1])
                
            elif int(user_atm_menu[1]) == 2:
                user_balance_operation(user_name)

                user_atm_menu = atm_menu(user_check_result[0], user_check_result[1])

            elif int(user_atm_menu[1]) == 3:
                exit_flag = True
                print("...................................................")
                print("..............You came out, Good luck..............")
                print("...................................................")
    
    return

    
# Function implementation
atm_workflow()