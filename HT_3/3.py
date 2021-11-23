""" Завдання_3

Написати функцiю season, яка приймає один аргумент — 
номер мiсяця (вiд 1 до 12), яка буде повертати пору року, 
якiй цей мiсяць належить (зима, весна, лiто або осiнь).
"""
# Used data
month_number = input("Please, input number of month: ")

# Check input data (is it number only)
if not month_number.isnumeric():
    print("Sorry, script accept posotove digit only (from 1 to 12)")

# Function for connect number by user to the year season 
def season(number):
    x = int(month_number)
    if  x == 1 or x == 2 or x == 12:
        function_result = "Зима"
    elif x in range(3, 6, 1):
        function_result = "Весна"
    elif x in range(6, 9, 1):
        function_result = "Літо"       
    elif x in range(9, 12, 1):
        function_result = "Осінь"
    else:
        function_result = "Sorry, script accept digit only (from 1 to 12)"
    return function_result

# Function results
f_result = season(month_number)

# Output results
print(f_result)