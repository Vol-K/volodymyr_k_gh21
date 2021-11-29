""" Завдання_1

Написати функцію < square > , яка прийматиме один аргумент - сторону квадрата, 
і вертатиме 3 значення (кортеж): периметр квадрата, площа квадрата та його діагональ.
"""

# Data from user
user_number = float(input("Please, input one positive number: "))

# Calculation of the shape options: perimeter (square), square, and diagonal
def square(number):

    if user_number > 0:
        shape_perimeter = number * 4
        shape_square = number * number
        shape_diagonal = (number ** 2 + number ** 2) ** (0.5)
        func_result = (round(shape_perimeter, 2), round(shape_square, 2), 
                       round(shape_diagonal, 2))
    else:
        func_result = "Sorry, put number bigger zero"

    return func_result

# Output results
print(square(user_number))

