""" Завдання_1

Написати функцію < square > , яка прийматиме один аргумент - сторону квадрата, 
і вертатиме 3 значення (кортеж): периметр квадрата, площа квадрата та його діагональ.
"""

# Data from user
user_number = input("Please, input one positive number: ")

# Calculation of the shape options: perimeter (square), square, and diagonal
def square(number):

    if number.isnumeric():
        number = int(number)
        shape_perimeter = number * 4
        shape_square = number * number
        shape_diagonal = (number ** 2 + number ** 2) ** (0.5)
        func_result = (shape_perimeter, shape_square, round(shape_diagonal, 2))
    else:
        func_result = "Sorry, script accept positive number only"

    return func_result

# Output results
print(square(user_number))

