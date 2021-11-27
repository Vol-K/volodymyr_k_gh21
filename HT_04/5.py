""" Завдання_5

Написати функцію < fibonacci >, яка приймає один аргумент 
і виводить всі числа Фібоначчі, що не перевищують його.
"""

# Data from user
user_number = input("Please, input one positive number: ")

# Checking is input data are numbers only
def isfloat(num_to_check):
    try:
        float(num_to_check)
        return True
    except ValueError:
        return False

# Calculate a new fibonacci numbers
def fibonacci(inp_numb):

    # Empty element, for subsequent operations
    fibonacci_number_list = []
    # First two elementa of fibonacci numbers
    fibonacci_number_1 = 0
    fibonacci_number_2 = 1

    # Checking is it numbers or no
    if isfloat(inp_numb) == False:
        fibonacci_number_check = "Sorry, script accept digits only"
    elif int(inp_numb) < 0:
        fibonacci_number_check = "Sorry, script accept positive number only"
    
    elif int(inp_numb) == 0:
        fibonacci_number_check = fibonacci_number_list[fibonacci_number_1]
    elif int(inp_numb) == 1:
        fibonacci_number_check = fibonacci_number_list[fibonacci_number_1, 
                                                       fibonacci_number_2]
    
    ### Real check calculation
    else:
        counter = 0

        # Calculate a new fibonacci numbers, based on two previous, 
        # And replace our numbers on onw step (left)
        while counter < int(inp_numb):

            new_fibonacci_number = fibonacci_number_1 + fibonacci_number_2
            fibonacci_number_list.append(new_fibonacci_number)

            fibonacci_number_1 = fibonacci_number_2
            fibonacci_number_2 = new_fibonacci_number

            counter = fibonacci_number_2 + fibonacci_number_1

        fibonacci_number_check = fibonacci_number_list

    return fibonacci_number_check

# Function implementation
print(fibonacci(user_number))