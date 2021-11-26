""" Завдання_5

Користувач вводить змiннi "x" та "y" з довiльними цифровими значеннями;
   -  Створiть просту умовну конструкцiю(звiсно вона повинна бути в тiлi ф-цiї), 
      пiд час виконання якої буде перевiрятися рiвнiсть змiнних "x" та "y" 
      і при нерiвностi змiнних "х" та "у" вiдповiдь повертали рiзницю чисел.
   -  Повиннi опрацювати такi умови:
   -  x > y;       вiдповiдь - х бiльше нiж у на z
   -  x < y;       вiдповiдь - у бiльше нiж х на z
   -  x == y.      вiдповiдь - х дорiвнює z
"""

# Data from user
first_user_number = input("Please, input first number: ")
second_user_number = input("Please, input second number: ")

# Function for calculation of difference two numbers
def compare(x, y):
        
    if int(x) == int(y):
        function_result = f"{x} дорівнює {y}"
    elif int(x) > int(y):
        z = int(x) - int(y)
        function_result = f"{x} бiльше нiж {y} на {z}" 
    elif int(x) < int(y):
        z = int(y) - int(x)
        function_result = f"{y} бiльше нiж {x} на {z}"
    return function_result

# Output results
print(compare(first_user_number, second_user_number))