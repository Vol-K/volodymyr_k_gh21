""" Завдання_7

Ну і традиційно -> калькулятор :) повинна бути 1 ф-цiя яка б приймала 3 аргументи 
- один з яких операцiя, яку зробити!
"""
################
# Поправить скрипт щоб приймав тільки задану послідовність введення інфи 
################
# Calculator function, for the four mathematical operation (+, -, *, /)
def calculator(x, y, operator):
    # Mathematical operation
    if operator == "*":
        print(x * y)
    if operator == "-":
        print(x - y)
    if operator == "+":
        print(x + y)
    if operator == "/":
        print(x / y)

# User data
first_numbers = input("Please, input first number: ")
second_numbers = input("Please, input second number: ")
input_operator = input("Please, input one operator only (+, -, *, /): ")

# Check of length, are we have all data
if len(input_operator) != 1:
    print("Sorry, script accespt one symbol for operator")

elif first_numbers.isalpha() or second_numbers.isalpha():
    print("Sorry, script accespt numbers only")

else:
    # Transform data for the function input
    first_number = int(first_numbers)
    second_number = int(second_numbers)
    
    # Output results
    calculator(first_number, second_number, input_operator)    