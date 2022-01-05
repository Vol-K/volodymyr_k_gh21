""" Завдання_4

Видозмініть програму так, щоб метод __init__ мався в класі «геометричні фігури» 
та приймав кольор фігури при створенні екземпляру, а методи __init__ підкласів 
доповнювали його та додавали початкові розміри.
"""


class Figure(object):
    """ This class creating with one attribute and method to changint it"""

    # Initialization of the new class instance
    def __init__(self, figure_color):
        self.figure_color = figure_color

    def change_color(self, new_color):
        self.figure_color = new_color


class Oval(Figure):
    """It`s subclass by 'Figure' and 
    describe the geometry figure with one parameter - diameter"""
    
    # Initialization of the new class instance
    def __init__(self, figure_color, diameter_size):
        self.diameter_size = diameter_size
        super().__init__(figure_color)


class Square(Figure):
    """It`s subclass by 'Figure' and 
    describe the geometry figure with two parameters - width & height"""

    # Initialization of the new class instance
    def __init__(self, figure_color, width, height):
        self.width = width
        self.height = height
        super().__init__(figure_color)


# Get default color from Class
test_figure = Figure("black")
print(test_figure.figure_color)

# Change default color in the Class
test_figure.change_color("deep-blue")
print(test_figure.figure_color)

# Set up a new type of figure "Oval" with special parameter (diamater)
oval_1 = Oval("white", 12)
print(oval_1.diameter_size)
print(oval_1.figure_color)

# Set up a new type of figure "Oval" with special parameters (x, y)
square_1 = Square("gray", 3, 7)
print(square_1.width)
print(square_1.height)
print(oval_1.figure_color)