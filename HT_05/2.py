""" Завдання_2

Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
   - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
   - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну цифру;
   - щось своє :)
   Якщо якийсь із параментів не відповідає вимогам - породити виключення із відповідним текстом.
"""

input_user_name = input("Create your user-name: ")
input_user_password = input("Input your password: ")

def login_validation(user_name, user_pass):
    
    password_digit_counter = 0
    for item in user_pass:
        if item.isdigit():
            password_digit_counter += 1

    upper_letter_counter = 0
    for letter in user_pass:

        if letter.isupper():   
            upper_letter_counter += 1

    if len(user_name) < 3:
        func_result = "Length of user-name must be bigger than 3 symbols"
    elif len(user_name) > 50:
        func_result = "Length of user-name must be less than 50 symbols"
    elif len(user_pass) < 8:
        func_result = "Length of user-password must be bigger than 7 symbols"
    elif password_digit_counter < 1:
        func_result = "User-password must contain min 1 digit"
    elif upper_letter_counter < 1:
        func_result = "User-password must contain min CAPITAL letter"
    else:
        func_result = "Yours user-name and password are valid"

    return func_result

print(login_validation(input_user_name, input_user_password))