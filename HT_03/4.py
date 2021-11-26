""" Завдання_4

Створiть 3 рiзних функцiї (на ваш вибiр). 
Кожна з цих функцiй повинна повертати якийсь результат. 
Також створiть четверу ф-цiю, яка в тiлi викликає 3 попереднi, 
обробляє повернутий ними результат та також повертає результат. 
Таким чином ми будемо викликати 1 функцiю, а вона в своєму тiлi ще 3
"""

# Test data
username_pass_dict = {"Tom": "thomas2", "Jon": "blabla", "Bob": "1234"}
access_dict = {"Tom": "user", "Jon": "admin", "Bob": "user"}

list_of_users = list(username_pass_dict.keys())
print("Hello, please login by one of these accounts")
print(list_of_users)
print("-------") #decoration

# User data
input_user_name = input("Please, input username: ")
input_pass = input("Please, input password: ")
print("-------") #decoration

# Checking is the 'input_user_name' include imputed username, or not 
def user_check(username, user_pass):
    if not username_pass_dict.get(username):
        user_check_result = False
    elif username_pass_dict.get(username) != user_pass:
        user_check_result = False
    else:
        user_check_result = True
    return user_check_result 

# Checking leve of access by imputed username
def access_level(username):
    if access_dict.get(username) == "admin":
        access_level_result = True
    else: 
        access_level_result = False
    return access_level_result

# 
def short_list_of_users(list_of_users, act_user):
    short_list_of_users_result = []
    for account_name in list_of_users:
        if account_name != act_user:
            short_list_of_users_result.append(account_name)
    return short_list_of_users_result


# Main function for user with admin acces (Jon)
def all_in_1_function():
   
    # Checking, containe username in database 
    if not user_check(input_user_name, input_pass):
        print("Sorry, wrong username or password")

    # Checking, is it admin
    elif access_level(input_user_name) == True:
        print("Hello amin, now you can delete on of the others account")

        # Creating list of accounts, exlude admin 
        temp_list = short_list_of_users(list_of_users, input_user_name)
        print(temp_list)
        print("-------") #decoration

        # Select accoun to delete
        del_acc = input("Please, input name of accounr to delete: ")
                
        # Delete account from two databsases (user and access)
        username_pass_dict.pop(del_acc)
        access_dict.pop(del_acc)
        
        # Printing modified database, for understanding that delete was successful
        available_accs = list(username_pass_dict.keys())
        print(available_accs)

    else:
        # Message
        print("Soory, You don not have any available options")

# Login with admin access, and delete other account 
all_in_1_function()