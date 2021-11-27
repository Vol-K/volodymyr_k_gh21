""" Завдання_6

Вводиться число. Якщо це число додатне, знайти його квадрат, 
якщо від'ємне, збільшити його на 100, якщо дорівнює 0, не змінювати.
"""

# Data from user
user_number = input("Please, input one number: ")

# Checking is input data are numbers only
def isfloat(num_to_check):
    try:
        float(num_to_check)
        return True
    except ValueError:
        return False

# Function for calculation by 'user_number' a 3 option:
# 1) number square; 2) plus 100; and 3) dont tuch zero
def number_func(inp_numb):
    
    # Checking is it numbers or no
    if isfloat(inp_numb) == False:
        func_result = "Sorry, script accept digits only"
    
    # Main part ot calculation
    elif float(inp_numb) > 0:
        func_result = float(inp_numb) ** 2
    elif float(inp_numb) == 0:
        func_result = 0
    else:
        func_result = float(inp_numb) + 100

    return func_result

# Function implementation
print(number_func(user_number))