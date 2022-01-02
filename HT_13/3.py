""" Завдання_3

3. Напишіть програму, де клас «геометричні фігури» (figure) містить властивість 
color з початковим значенням white і метод для зміни кольору фігури, а його 
підкласи «овал» (oval) і «квадрат» (square) містять методи __init__ 
для завдання початкових розмірів об'єктів при їх створенні.
"""


class Figure(object):
    """ This class has one default attribute and method to changint it"""

    color = "white"
    
    def change_color(self, new_color):
        self.color = new_color


class Oval(Figure):
    """It`s subclass by 'Figure' and 
    describe the geometry figure with one parameter - diameter"""

    # Initialization of the new class instance
    def __init__(self, diameter_size):
        self.diameter_size = diameter_size


class Square(Figure):
    """It`s subclass by 'Figure' and 
    describe the geometry figure with two parameters - width & height"""

    # Initialization of the new class instance
    def __init__(self, width, height):
        self.width = width
        self.height = height


# Get default color from Class
test_figure = Figure()
print(test_figure.color)

# Change default color in the Class
test_figure.change_color("blue")
print(test_figure.color)


# Set up a new type of figure "Oval" with special parameter (diamater)
oval_1 = Oval(12)
print(oval_1.diameter_size)

# Set up a new type of figure "Oval" with special parameters (x, y)
square_1 = Square(3, 7)
print(square_1.width)
print(square_1.height)