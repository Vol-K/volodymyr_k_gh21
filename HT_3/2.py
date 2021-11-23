""" Завдання_2

Користувачем вводиться початковий і кінцевий рік. 
Створити цикл, який виведе всі високосні роки в цьому проміжку (границі включно).
"""

# Data from user
first_user_year = input("Please, input start year: ")
second_user_year = input("Please, input last year: ")

# Check input data (is it number only)
if not first_user_year.isnumeric() or not second_user_year.isnumeric():
    print("Sorry, script accept digit only")

else:   
    # Searching each 'Leap year' between user input years
    for year in range(int(first_user_year), int(second_user_year)+1, 1):
        if year % 400 == 0:
            print(year)
        elif year % 4 == 0 and year % 100 != 0:
            print(year)