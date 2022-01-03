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
        print(f"Sum of {x} and {y} = {x+y}")
        self.last_result = x+y

    def subtraction(self, x, y):  
        print(f"Difference of {x} and {y} = {x-y}")
        self.last_result = x-y

    def multiplication(self, x, y):  
        print(f"Multiplication of {x} and {y} = {x*y}")
        self.last_result = x*y

    def division(self, x, y):  
        print(f"Division of {x} by {y} = {round(x/y, 4)}")
        self.last_result = round(x/y, 4)


# Test instatnse of class
test_calculation = Calc()
print(test_calculation.last_result)

# Result of calculations
test_calculation.addition(2, 3)
print(test_calculation.last_result)

test_calculation.subtraction(2, 3)
print(test_calculation.last_result)

test_calculation.multiplication(2, 3)
print(test_calculation.last_result)

test_calculation.division(2, 3)
print(test_calculation.last_result)