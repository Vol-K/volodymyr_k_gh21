""" Завдання_2

Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
   - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
   - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну цифру;
   - щось своє :)
   Якщо якийсь із параментів не відповідає вимогам - породити виключення із відповідним текстом.
"""

input_user_name = input("Create your user-name: ")
input_user_password = input("Input your password: ")

# Our own exception
class MyException(Exception):
    pass

# Validation of username & password by user
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
       raise MyException("Length of user-name must be bigger than 3 symbols")
    elif len(user_name) > 50:
        raise MyException("Length of user-name must be less than 50 symbols")
    elif len(user_pass) < 8:
       raise MyException("Length of user-password must be bigger than 7 symbols")
    elif password_digit_counter < 1:
        raise MyException("User-password must contain min 1 digit")
    elif upper_letter_counter < 1:
        raise MyException("User-password must contain min CAPITAL letter")
    else:
        func_result = "Yours user-name and password are valid"

    return func_result

# Function implementation
print(login_validation(input_user_name, input_user_password))