""" Завдання_7

Ну і традиційно -> калькулятор :) повинна бути 1 ф-цiя яка б приймала 3 аргументи 
- один з яких операцiя, яку зробити!
"""

# User data
first_numbers = input("Please, input first number: ")
second_numbers = input("Please, input second number: ")
input_operator = input("Please, input one operator only (+, -, *, /): ")

# Strings with acceptable symbols
acceptable_numbers = "-0123456789"
acceptable_operator = "-+*/"

# Calculator function, for the four mathematical operation (+, -, *, /)
def calculator(x, y, operator):
    
    # Checking input data from user
    # Protect by empty input for first number
    if len(x) < 1:
        output_message_x = "No symbol in first number"
        check_emp_x = False
        check_x = False
    else:
        check_emp_x = True
        # Is it number only in first number
        for item in x:
            if item not in acceptable_numbers:
                output_message_x = "Mistake in first number"
                check_x = False
            else:
                check_x = True
                check_len_x = True
    
        # Block '-' only in the first number
        if len(x) < 2 and x == "-":
            output_message_x = "Mistake in first number"
            check_len_x = False
    
    # Protect by empty input for second number
    if len(y) < 1:
        output_message_y = "No symbol in second number"
        check_emp_y = False
        check_y = False
    else:
        check_emp_y = True
        # Is it number only in second number
        for item in y:
            if item not in acceptable_numbers:
                output_message_y = "Mistake in second number"
                check_y = False
            else:
                check_y = True
                check_len_y = True

        # Block '-' only in second number
        if len(y) < 2 and y == "-":
            output_message_op = "Mistake in second number"
            check_len_y = False
    
    # Protect by empty input for operator
    if len(operator) < 1:
        output_message_op = "No symbol in operator"
        check_operator = False
        check_emp_op = False
    elif len(operator) > 1:
        output_message_op = "Mistake in second number"
        check_operator = False
        check_emp_op = True
    else:
        for item in operator:
            if item not in acceptable_operator:
                output_message_op = "Mistake in operator"
                check_operator = False
                check_emp_op = True
            else:   
                check_operator = True
                check_emp_op = True
    
    # Stopping script if we found mistake (one or more)
    if (check_x == False or check_len_x == False or check_emp_x == False 
        or check_y == False or check_len_y == False or check_emp_y == False 
        or check_operator == False or check_emp_op == False):
        
        if check_x == False or check_len_x == False or check_emp_x == False:
            print(output_message_x)
        if check_y == False or check_len_y == False or check_emp_y == False:
            print(output_message_y)
        if check_operator == False or check_emp_y == False:
            print(output_message_op)
    
    # Mathematical operation (finaly)
    else: 
        # Convert input data
        x = int(x)
        y = int(y)

        # And calculation
        if operator == "*":
            print(x * y)
        if operator == "-":
            print(x - y)
        if operator == "+":
            print(x + y)
        if operator == "/":
            if y == 0:
                print("Soory, division by zero is impossible")
            else:
                print(x / y)

# Function implementation
calculator(first_numbers, second_numbers, input_operator) 