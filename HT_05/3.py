""" Завдання_3

 На основі попередньої функції створити наступний кусок кода:
   а) створити список із парами ім'я/пароль різноманітних видів 
   (орієнтуйтесь по правилам своєї функції) - як валідні, так і ні;
   б) створити цикл, який пройдеться по цьому циклу і, користуючись валідатором, 
   перевірить ці дані і надрукує для кожної пари значень відповідне повідомлення, 
   наприклад:
      Name: vasya
      Password: wasd
      Status: password must have at least one digit
      -----
      Name: vasya
      Password: vasyapupkin2000
      Status: OK
   P.S. Не забудьте використати блок try/except ;)
"""

# Our own exception
class MyException(Exception):
    pass

# Our test database
username_and_pass_dict = [["Ty", "thoMMhas2"], ["Jon", "blAbl11a"], ["Bob", "12_l3gggg4j"],
                            ["Billy", "as7Bj"], ["Urgen5678jgdsdvh", "iuFBrn_6"], ["error"]]

# Validation of username & password
def login_validation(user_name, user_pass):
    
    # Calculation digits inside password
    password_digit_counter = 0
    for item in user_pass:
        if item.isdigit():
            password_digit_counter += 1

    # Calculation CAPITAL letters inside password
    upper_letter_counter = 0
    for letter in user_pass:
        if letter.isupper():   
            upper_letter_counter += 1

    if len(user_name) < 3:
        func_result = "Length of user-name must be bigger than 3 symbols"
    elif len(user_name) > 15:
        func_result = "Length of user-name must be less than 15 symbols"
    elif len(user_pass) < 8:
        func_result = "Length of user-password must be bigger than 7 symbols"
    elif password_digit_counter < 1:
        func_result = "User-password must contain min 1 digit"
    elif upper_letter_counter < 1:
        func_result = "User-password must contain min CAPITAL letter"
    else:
        func_result = "OK"

    return func_result

# Validation of username & password from the list 'username_and_pass_dict'
for i in range(len(username_and_pass_dict)):
    
    try:
        username_and_pass_dict[i][0]
        username_and_pass_dict[i][1]
    except IndexError:
        print("!--Error in DataBase---")
        print("!--Please connect with tech support---")
    else:
        print("Name: ", username_and_pass_dict[i][0])
        print("Password: ", username_and_pass_dict[i][1])
        print("Status: ", login_validation(username_and_pass_dict[i][0], 
                                           username_and_pass_dict[i][1]))
        print("-----------------------------")

