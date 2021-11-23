""" Завдання_6

Маємо рядок --> 
"f98neroi4nr0c3n30irn03ien3c0rfekdno400wenwkowe00koijn35pijnp46ij7k5j78p3kj546p465jnpoj35po6j345" -> 
просто потицяв по клавi
Створіть ф-цiю, яка буде отримувати рядки на зразок цього, яка оброблює наступні випадки:
    -  якщо довжина рядка в діапазонi 30-50 -> прiнтує довжину, кiлькiсть букв та цифр
    -  якщо довжина менше 30 -> прiнтує суму всiх чисел та окремо рядок без цифр (лише з буквами)
    -  якщо довжина бульше 50 - > ваша фантазiя
"""

# Data from user
symbols_by_user = input("Please, input letters/numbers: ")

# Function for 3 action with input data
def f_symbols_by_user(symbols_by_user):
    
    # First action - sum of all numbers inside 'str', 
    # and output letters only
    if len(symbols_by_user) < 30:
        
        letters_only = ""
        sum_numbers = 0

        for item in symbols_by_user:

            if item.isalpha():
                letters_only += item
            if item.isdigit():
                sum_numbers += int(item)

        print("Сума всіх чисел в рядку - ", sum_numbers)
        print("Рядок без цифр - ", letters_only)

    # Second action - calculate length of the 'str', 
    # also number of letters and numbers inside 'str'
    if (30 < len(symbols_by_user) < 51):
        f_letters = 0
        f_numbers = 0

        for item in symbols_by_user:

            if item.isalpha():
                f_letters += 1
            if item.isdigit():
                f_numbers += 1
        print("Довжина рядка - ", len(symbols_by_user),\
              "Кількість букв в рядку - ", f_letters,\
              "Кількість цифр в рядку - ", f_numbers)        
    
    # Shift ASCII code of input letters inside 'str'
    # step of shifting will be five(5)
    if len(symbols_by_user) > 50:
        step = 5
        shifted_str = ''

        for item in symbols_by_user:

            if item.isalpha():
                if ord(item) > 96 and ord(item) < 123:
                    item = chr(ord(item) + step)
                    shifted_str += item
            if item.isdigit():
                shifted_str += item

        print("Рядок зі зсувом символів (на 5) по ASCII - ", shifted_str)
    
    # Function output
    return

# Function implementation
f_symbols_by_user(symbols_by_user)
