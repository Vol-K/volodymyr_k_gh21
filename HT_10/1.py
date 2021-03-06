""" Завдання_1

1. Доповніть програму-банкомат наступним функціоналом:
   - новий пункт меню, який буде виводити поточний курс валют (API Приватбанк)

2. Написати скрипт, який буде приймати від користувача назву валюти і початкову дату.
   - Перелік валют краще принтануть.
   - Також не забудьте указати, в якому форматі коритувач повинен ввести дату.
   - Додайте перевірку, чи введена дата не знаходиться у майбутньому ;)
   - Також перевірте, чи введена правильна валюта.
   Виконуючи запроси до API архіву курсу валют Приватбанку, вивести інформацію про зміну
   курсу обраної валюти (Нацбанк) від введеної дати до поточної. Приблизний вивід наступний:

   Currency: USD

   Date: 12.12.2021
   NBU:  27.1013   -------

   Date: 13.12.2021
   NBU:  27.0241   -0,0772

   Date: 14.12.2021
   NBU:  26.8846   -0,1395

3. Конвертер валют. Прийматиме від користувача назву двох валют і суму (для першої).
   Робить запрос до API архіву курсу валют Приватбанку (на поточну дату) і виконує
   конвертацію введеної суми з однієї валюти в іншу.
"""

import pathlib
from pathlib import Path
import requests
import json
import time
import datetime
import sqlite3


# Connect for database
database_file_path = Path(pathlib.Path.cwd(), "atm_database.db")
database = sqlite3.connect(database_file_path, check_same_thread=False)
db_cur = database.cursor()


# ATM Login proccess, for 2 types of account (user & incasator)
def login(login_name, login_password):

    check_result = False
    user_type = False
    check_user = db_cur.execute("SELECT * FROM users WHERE name=? AND password=?",\
                            (login_name, login_password)).fetchone()

    if check_user != None:
        check_result = True
        user_type = check_user[3]
  
    return check_result, user_type


# Check the current user balance
def view_balance_of_user(inp_name):
    user_balance = db_cur.execute("SELECT user_balance FROM balances WHERE user_name=?", (inp_name,)).fetchone()
                        
    return user_balance


# Algorithm of cash withdrawal for user (from MAX banknot to MIN)
def output_banknot_algorithm(inp_value):
    
    inp_value = int(inp_value)

    # Empty and support elements, for subsequent operations
    banknots_for_withdrawal = {}
    total_atm_money = 0
    temp_listt = []
    nickelback = 0
    status_of_operation = False
    start_flag = False
    end_algorithm_flag = False

    # Quantity of banknots available for withdrawal, & find a start position
    banknots_status = db_cur.execute("SELECT * FROM banknots WHERE quantity > 0\
                                      AND nominal BETWEEN 1 AND ?", (inp_value,)\
                                      ).fetchall()
   
    list_for_algorithm = banknots_status.copy()
    list_for_algorithm.reverse()

    # Total sum of money inside ATM
    for item in banknots_status:
        total_atm_money += (int(item[0]) * item[1])

    #etalon = banknots_status.copy()

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
                    list_for_algorithm = banknots_status.copy()
                    list_for_algorithm.pop(0)
                    banknots_status.pop(0)
                    start_flag = False
                        
            elif nickelback == 0:
                end_algorithm_flag = True
                banknots_for_withdrawal = dict(temp_listt)
                status_of_operation = True
               

    #print(banknots_for_withdrawal)
    return banknots_for_withdrawal, status_of_operation


# Update status of available banknots inside ATM
def update_banknots_by_user_operation(banknots_dict):

    old_banknots_status = dict(db_cur.execute("SELECT * FROM banknots").fetchall())
    # Calculation new quantity
    list_banknots_for_withdrawal = banknots_dict.keys()
    for item in list_banknots_for_withdrawal:
        new_quantity = old_banknots_status[item] - banknots_dict[item]
        db_cur.execute("UPDATE banknots SET quantity=? Where nominal=?", (new_quantity, item,))
        database.commit()


# Operation by user balance (adding & withdrawing money)
def user_balance_operation(ub_name):

    input_sum = input("Please, input money sum (ex. '+;10' or '-;10'): ")
    input_sum = input_sum.split(";")

    if len(input_sum) != 2:
        print("...................................................")
        print("#####_Inputed not all parameters_#####")
    # elif not input_sum[0] or not input_sum[1]:
    #     print("...................................................")
    #     print("#####_Inputed empty parameter/s_#####")
    elif not input_sum[1].isnumeric():
        print("...................................................")
        print("#####_Inputed uncorrect parameter_#####")
    elif int(input_sum[1]) < 0:    
        print("...................................................")
        print("###_Inputed wrong value_###")
    else:
        balance_sum = db_cur.execute("SELECT user_balance FROM balances WHERE user_name=?", (ub_name,)).fetchone()
        user_id = db_cur.execute("SELECT id FROM users WHERE name=?", (ub_name,)).fetchone()

        # Time of user transaction
        time_in_seconds = time.time()
        transaction_time = time.ctime(time_in_seconds)

        # Update user balance in a file & added a new transaction to the file
        if input_sum[0] == "+":

            # if int(input_sum[1]) < 0:
            #     print("#####_Inputed wnegative number_#####")
            # else:
            new_balance = int(balance_sum[0]) + int(input_sum[1])
            db_cur.execute("UPDATE balances SET user_balance=? WHERE user_name=?", (new_balance, ub_name))
            database.commit()

            trans_type = "plus"
            transaction = (transaction_time, user_id[0], ub_name, trans_type, int(input_sum[1]))
            db_cur.execute("INSERT INTO transactions (operation_time, user_id, user_name,\
                            operation_type, operation_sum) VALUES (?, ?, ?, ?, ?)", transaction)
            database.commit()
            
            print("_________________________")
            print(f"### Your actual balance now: {view_balance_of_user(ub_name)[0]} USD ###")

        elif input_sum[0] == "-":

            if abs(int(input_sum[1])) > int(balance_sum[0]):
                print("### Inputed less than you have ###")
            elif (int(input_sum[1]) % 10) > 0:
                print("Please, input number divided by 10")
            else:
                
                ckecking_banknots = output_banknot_algorithm(input_sum[1])
                if not ckecking_banknots[1]:
                    min = db_cur.execute("SELECT MIN (nominal) FROM banknots\
                                         WHERE quantity > 0").fetchone()
                    print("...................................................")
                    print("")
                    print("###..Sorry, ATM can not withdraw this sum.......###")
                    print("###..Please, input smoller number...............###")
                    print("###..Minimal available nominal is: {:<4} USD.....###".format(min[0]))
                    print("")
            
                else:
                    new_balance = int(balance_sum[0]) - int(input_sum[1])
                    db_cur.execute("UPDATE balances SET user_balance=? WHERE \
                                    user_name=?", (new_balance, ub_name))
                    database.commit()

                    trans_type = "minus"
                    transaction = (transaction_time, user_id[0], ub_name, trans_type, int(input_sum[1]))
                    db_cur.execute("INSERT INTO transactions (operation_time, user_id,\
                                    user_name, operation_type, operation_sum)\
                                    VALUES (?, ?, ?, ?, ?)", transaction)
                    database.commit()
                    
                    banknots_for_print = list(ckecking_banknots[0].items())
                    for elem in banknots_for_print:
                        print("Nominal '{}' USD; Quantity - {} banknot/s".format(elem[0], elem[1]))
                        
                    # Update banknots numbers after operation
                    update_banknots_by_user_operation(ckecking_banknots[0])
                    print("_________________________")
                    print(f"### Your actual balance now: {view_balance_of_user(ub_name)[0]} USD ###")
        else:
            print("...................................................")
            print("###_Inputed wrong first parameter_###")


# Checking of current exchange rate
def check_current_exchange_rate():

    pb_api_link = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"

    exchange_rate = requests.get(pb_api_link)
    exchange_rate = json.loads(exchange_rate.text)

    time.sleep(0.2)
    print("...................................................")
    print("Currancy code: Buying // Selling")
    for item in exchange_rate:
        print("{}: {:10} // {:10}".format(item['ccy'], item['buy'], item['sale']))
        time.sleep(0.5)


# Archive of current exchange rate
def exchange_rate_archive():
    print("...................................................")
    pb_cut_link = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

    list_of_available_currencies = [["USD", "US dollars"], ["EUR", "Euro"], 
                                    ["CAD", "Canadian dollars"], ["GBP", "UK pounds"], 
                                    ["JPY", "Japanese yen"], ["PLN", "Polish złoty"], 
                                    ["CHF", "Swiss franc"]]
    
    for element in list_of_available_currencies:
        print(f"{element[0]}: {element[1]}")
        time.sleep(0.2)
   
    print("...................................................")
    currency_by_user = input("Please choose one currency from this list: ") 
    date_by_user = input("Please input date from 01.01.2016 until today (ex.: 13.12.2020): ")
    print("...................................................")

    # Check inputed currency & date from user (is it correct)
    check_list = list(list(zip(*list_of_available_currencies))[0])
    if currency_by_user not in check_list:
        print("")
        print("### Wrong Currency code ###")
    else:
        try:      
            transform_date_by_user = datetime.datetime.strptime(date_by_user, "%d.%m.%Y")
            time_delta = datetime.timedelta(days=1)
            date_now = datetime.datetime.now()

            date_limitation = "01.01.2016"
            date_limitation = datetime.datetime.strptime(date_limitation, "%d.%m.%Y")

            if date_now < transform_date_by_user:
                print("Inputed future date")
            elif transform_date_by_user < date_limitation:
                print("Inputed to old date")
            else:
                print("")
                print(f"Currancy code: {currency_by_user}")
                print("")
                start_flag = True
                previos_day_rate = 0

                while transform_date_by_user <= date_now:
                    
                    pb_api_link = pb_cut_link + transform_date_by_user.strftime("%d.%m.%Y")
                    exchange_rate_arch = requests.get(pb_api_link)
                    exchange_rate_arch = json.loads(exchange_rate_arch.text)
                    
                    nbu_db = exchange_rate_arch["exchangeRate"]
                    nbu_db.pop(0)
                    for elem in nbu_db:
                    
                        if elem["currency"] == currency_by_user:
                            nbu_rate =  elem["saleRateNB"]
                            diff_rate = previos_day_rate - nbu_rate
                            previos_day_rate = elem["saleRateNB"]

                    print(f"Date: {transform_date_by_user.strftime('%d.%m.%Y')}")
                    if start_flag:
                        print(f"NBU: {nbu_rate}")
                        start_flag = False
                    else:
                        print(f"NBU: {nbu_rate} // {round(diff_rate, 4)}")
                    print("")
                
                    transform_date_by_user += time_delta
                    time.sleep(0.5)

        except ValueError:
            print("Inputed Wrong date parameters")


# Archive of current exchange rate
def money_exchange():
    print("...................................................")
    print("Currencies available for exchange")
    print("")

    list_of_available_currencies = [["USD", "US dollars"], ["EUR", "Euro"], 
                                    ["CHF", "Swiss franc"], ["GBP", "UK pounds"], 
                                    ["CZK", "Czech koruna"], ["PLN", "Polish złoty"], 
                                    ["UAH", "Ukrainian hryvnia"]]

    for element in list_of_available_currencies:
        print(f"{element[0]}: {element[1]}")
        time.sleep(0.2)
   
    print("...................................................")
    currency_pir_by_user = input("Please input currency pair for exchange (ex. USD/EUR): ")
    money_sum_by_user = input("Please input money sum for exchange (ex.: 157 or 4073): ")
    currency_pir_by_user = currency_pir_by_user.split("/")
    print("...................................................")

    # Check inputed currency pair from user (is it correct)
    check_list = list(list(zip(*list_of_available_currencies))[0])
    if (currency_pir_by_user[0] not in check_list or 
        currency_pir_by_user[1] not in check_list):
        
        print("")
        print("### Wrong Currency code ###")
    elif not money_sum_by_user.isdigit():
        print("")
        print("### Wrong money sum numbers ###")
    elif currency_pir_by_user[0] == currency_pir_by_user[1]:
        print("")
        print("### Please input two different currency to the pair ###")
    else:

        pb_cut_link = "https://api.privatbank.ua/p24api/exchange_rates?json&date="
        date_now = datetime.datetime.now()

        pb_api_link = pb_cut_link + date_now.strftime("%d.%m.%Y")
        exchange_rates = requests.get(pb_api_link)
        exchange_rates= json.loads(exchange_rates.text)
        
        currencies_db = exchange_rates["exchangeRate"]
        
        if not currencies_db:
            time_delta = datetime.timedelta(days=1)
            date_now = date_now - time_delta

            pb_api_link = pb_cut_link + date_now.strftime("%d.%m.%Y")
            exchange_rates = requests.get(pb_api_link)
            exchange_rates= json.loads(exchange_rates.text)
        
            currencies_db = exchange_rates["exchangeRate"]
        
        # Delete first row     
        currencies_db.pop(0)

        #! Operation when UAH is a part of currency pair
        # We are buying UAH
        if currency_pir_by_user[1] == "UAH":
            for elem in currencies_db:
                if elem["currency"] == currency_pir_by_user[0]:
                    output_sum = elem["saleRate"] * int(money_sum_by_user)

            message = (f"You will get {round(output_sum, 2)} {currency_pir_by_user[1]}"
                       f" for your money ({money_sum_by_user} {currency_pir_by_user[0]})")
            print(message)

        # We are selling UAH
        elif currency_pir_by_user[0] == "UAH":
            for elem in currencies_db:
                if elem["currency"] == currency_pir_by_user[1]:
                    output_sum = int(money_sum_by_user) / elem["saleRate"] 

            message = (f"You will get {round(output_sum, 2)} {currency_pir_by_user[1]}"
                       f" for your money ({money_sum_by_user} {currency_pir_by_user[0]})")
            print(message)

        #! Operation when UAH is not a part of currency pair (double exchange)
        else:
            # Find UAH tranzit sum
            uah_tranz_sum = 0
            for elem in currencies_db:
                if elem["currency"] == currency_pir_by_user[0]:
                    uah_tranz_sum = elem["purchaseRate"] * int(money_sum_by_user)

            # Find sum of output Corrency 
            for elem in currencies_db:
                if elem["currency"] == currency_pir_by_user[1]:
                    output_sum = uah_tranz_sum / elem["saleRate"] 

            message = (f"You will get {round(output_sum, 2)} {currency_pir_by_user[1]}"
                       f" for your money ({money_sum_by_user} {currency_pir_by_user[0]})")
            print(message)


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
        oper_flag = check_atm_option(user_option, user_status)
        
    elif user_status == "user":

        user_oparions = [[1, "Check balance"], [2, "Balance operation"], [3, "Current exchange rate"],
                         [4, "Archive of exchange rates"], [5, "Money exchange"], [6, "Exit"]]
        oper_flag = False

        for item in user_oparions:
            print(f"{item[0]} - {item[1]}")
            time.sleep(0.5)
        print("___________________________")        
        user_option = input("Select 1, 2, 3, 4, 5 or 6: ")
        oper_flag = check_atm_option(user_option, user_status)

    return user_status, user_option, oper_flag


# Validation of chosen menu option
def check_atm_option(inp_option, user_status):
    
    if user_status == "admin":
        granted_symbols = "123"

        if len(inp_option) != 1:
            f_result = False
        elif inp_option not in granted_symbols:
            f_result = False
        else:
            f_result = True

    elif user_status == "user":
        granted_symbols = "123456"

        if len(inp_option) != 1:
            f_result = False
        elif inp_option not in granted_symbols:
            f_result = False
        else:
            f_result = True

    return f_result


# Checkin availability of banknots inside ATM
def check_banknots():
    
    banknots_status = db_cur.execute("SELECT * FROM banknots").fetchall()
    print("...................................................")
    time.sleep(0.2)
    print("### Available banknots in ATM ###")
    print("### Nominal: Quantity ###")
    
    for item in banknots_status:
        print('{:<4}: {}'.format(item[0], item[1]))
        time.sleep(0.2)


# Recharge ATM by the new banknots
def cash_in_operation():

    print("...................................................")
    print("#### Cash-in (CVIT) operations ####")
    inp_nominal_quantity = input("Please, input banknot nomial & quantity for added to ATM (ex. '10';21): ")
    inp_nominal_quantity = inp_nominal_quantity.split(";")
    
    # Validation input data
    if len(inp_nominal_quantity) < 2:
        print("Wrong, please input all parameters")
    elif not inp_nominal_quantity[0] or not inp_nominal_quantity[1]:
        print("Wrong, please input all parameters")
    elif (not inp_nominal_quantity[0].isnumeric() 
        or not inp_nominal_quantity[1].isnumeric()):

        print("Wrong, please input correct nominal/quantity")

    elif int(inp_nominal_quantity[0]) <=0 or int(inp_nominal_quantity[1]) < 0:
        print("Wrong, do not accept negative parameters")

    else:
        banknots_status = db_cur.execute("SELECT * FROM banknots WHERE nominal=?",\
                                         (inp_nominal_quantity[0],)).fetchone()

        if not banknots_status:
            print("Wrong, please input correct nominal")
        else:
            old_quantity = banknots_status[1]
            new_quantity = old_quantity + int(inp_nominal_quantity[1])

            # Wright changes
            db_cur.execute("UPDATE banknots SET quantity=? WHERE nominal=?",\
                           (new_quantity, inp_nominal_quantity[0]))
            database.commit()
            print("...................................................")
            print(f"A new quantity of banknots: Nominal '{inp_nominal_quantity[0]}': {new_quantity} items")


# ATM workflow logic
def atm_workflow():

    user_name = input("Input your name: ")
    user_pass = input("Input your password: ")
    # user_name = "user2"
    # user_pass = "user2"

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

    user_type = user_check_result[1]
    # 'Incasator' side of ATM menu
    if user_type == "admin":

        admin_atm_menu = atm_menu(user_type)
        exit_flag = False 

        while exit_flag == False:
            if not admin_atm_menu[2]:
                print("Soory, inputed wrong symbols")
                admin_atm_menu = atm_menu(user_type)
                
            elif int(admin_atm_menu[1]) == 1:
                check_banknots()
                admin_atm_menu = atm_menu(user_type)

            elif int(admin_atm_menu[1]) == 2:
                cash_in_operation()
                admin_atm_menu = atm_menu(user_type)

            elif int(admin_atm_menu[1]) == 3:
                exit_flag = True
                print("...................................................")
                print("..............You came out, Good luck..............")
                print("...................................................")

    # 'User' side of ATM menu
    elif user_type == "user":

        user_atm_menu = atm_menu(user_type)
        exit_flag = False    

        while exit_flag == False:
            if not user_atm_menu[2]:
                print("Soory, inputed wrong symbols")
                user_atm_menu = atm_menu(user_type)

            elif int(user_atm_menu[1]) == 1:
                print("...................................................")
                print(f"Your balance: {view_balance_of_user(user_name)[0]} USD")
                user_atm_menu = atm_menu(user_type)
                
            elif int(user_atm_menu[1]) == 2:
                user_balance_operation(user_name)
                user_atm_menu = atm_menu(user_type)

            elif int(user_atm_menu[1]) == 3:
                check_current_exchange_rate()
                user_atm_menu = atm_menu(user_type)

            elif int(user_atm_menu[1]) == 4:
                exchange_rate_archive()
                user_atm_menu = atm_menu(user_type)
            
            elif int(user_atm_menu[1]) == 5:
                money_exchange()
                user_atm_menu = atm_menu(user_type)

            elif int(user_atm_menu[1]) == 6:
                exit_flag = True
                print("...................................................")
                print("..............You came out, Good luck..............")
                print("...................................................")
    
    return


# Function implementation
atm_workflow()