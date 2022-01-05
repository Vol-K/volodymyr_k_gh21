""" Завдання_1

Створити клас Calc, який буде мати атребут last_result та 4 методи. 
Методи повинні виконувати математичні операції з 2-ма числами, а саме:
додавання, віднімання, множення, ділення.
   - Якщо під час створення екземпляру класу звернутися до атребута last_result він повинен повернути пусте значення
   - Якщо використати один з методів - last_result повенен повернути результат виконання попереднього методу.
   - Додати документування в клас (можете почитати цю статтю: https://realpython.com/documenting-python-code/ )
"""

class Calc(object):
    """Short class description
    
    Class has one default attribute and four methods for simple calculation
    with the two numbers: additions, subtraction, multiplication & dividing.
    Each method save result of its calculation into default attribute."""

    last_result = None

    def addition(self, x, y):
        self.last_result = x+y
        method_result = f"Sum of {x} and {y} = {x+y}"
        return method_result

    def subtraction(self, x, y):  
        self.last_result = x-y
        method_result = f"Difference of {x} and {y} = {x-y}"
        return method_result

    def multiplication(self, x, y):  
        self.last_result = x*y
        method_result = f"Multiplication of {x} and {y} = {x*y}"
        return method_result

    def division(self, x, y):
        if y != 0:  
            self.last_result = round(x/y, 4)
            method_result = f"Division of {x} by {y} = {round(x/y, 4)}"
        else:
            method_result = "You can't divide to by zero"
        return method_result

# Test instatnse of class
test_calculation = Calc()
print(test_calculation.last_result)

# Result of calculations
numbers_addition = test_calculation.addition(2, 3)
print(numbers_addition)
print(test_calculation.last_result)

numbers_subtraction = test_calculation.subtraction(2, 3)
print(numbers_subtraction)
print(test_calculation.last_result)

numbers_multiplication = test_calculation.multiplication(2, 3)
print(numbers_multiplication)
print(test_calculation.last_result)

numbers_divided = test_calculation.division(2, 0)
print(numbers_divided)
print(test_calculation.last_result)