""" Завдання_1

Створіть функцію, всередині якої будуть записано список 
із п'яти користувачів (ім'я та пароль).
Функція повинна приймати три аргументи: 
    - два - обов'язкових (<username> та <password>) 
    - і третій - необов'язковий параметр <silent> (значення за замовчуванням - <False>).
Логіка наступна:
    - якщо введено коректну пару ім'я/пароль - вертається <True>;
    - якщо введено неправильну пару ім'я/пароль і <silent> == <True> - функція вертає <False>, 
      інакше (<silent> == <False>) - породжується виключення func_result = False
"""

input_user_name = input("Input your user-name: ")
input_user_password = input("Input your password: ")
input_silent = input("Silent put something/or empty: ")

# Our own exception
class LoginException(Exception):
    pass

# Checking input data by user
def user_pass_check(username, password, silent = False):
    
    # Our test database
    username_and_pass_dict = [["Tom", "thoMas2"], ["Jon", "blAbla"], ["Bob", "12_l34"],
                              ["Billy", "asr7Bj"], ["Urgen", "iurn_6"]]

    valid = False
    silent_check = False

    if silent:
        silent_check = True

    for i in range(len(username_and_pass_dict)):

        if username == username_and_pass_dict[i][0]:
            password == username_and_pass_dict[i][1]
            valid = True

    if valid == True:
        func_result = True
    elif silent_check == True and valid == False:
        raise LoginException("func_result = False")
    else:
        func_result = False

    return func_result

# Function implementation
if len(input_silent) == 0:  
    print(user_pass_check(input_user_name, input_user_password))
else:
    print(user_pass_check(input_user_name, input_user_password, input_silent))