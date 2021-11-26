""" Завдання_1

Написати функцію < square > , яка прийматиме один аргумент - сторону квадрата, 
і вертатиме 3 значення (кортеж): периметр квадрата, площа квадрата та його діагональ.
"""

# Data from user
user_number = input("Please, input one number: ")

dot = "."

# Checking is input data are numbers only
def isfloat(num_to_check):
    try:
        float(num_to_check)
        return True
    except ValueError:
        return False

# Calculation of the shape options: perimeter (square), square, and diagonal
def square(number):

    # Save the number for int check/output
    origin_num = number

    if isfloat(number) == True:
        number = float(number)
        shape_perimeter = number * 4
        shape_square = number + number
        shape_diagonal = (number ** 2 + number ** 2) ** (0.5)
        func_result = (shape_perimeter, shape_square, round(shape_diagonal, 2))

    # Wrong input data message
    else:
        func_result = "Sorry, script accept one positive digit only"

    # Output 'int' style of number if user put 'int'
    if dot not in origin_num:
        func_result = (int(shape_perimeter), int(shape_square), 
                       round(shape_diagonal, 2))

    return func_result

# Output results
print(square(user_number))

