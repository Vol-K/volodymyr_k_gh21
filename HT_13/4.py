""" Завдання_4

4. Видозмініть програму так, щоб метод __init__ мався в класі «геометричні фігури» 
та приймав кольор фігури при створенні екземпляру, а методи __init__ підкласів 
доповнювали його та додавали початкові розміри.
"""


class Figure(object):
    """ This class creating with one attribute and method to changint it"""

    figure_color = ""

    # Initialization of the new class instance
    def __init__(self, figure_color):
        self.figure_color = figure_color

    def change_color(self, new_color):
        self.figure_color = new_color


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
test_figure = Figure("black")
print(test_figure.figure_color)

# Change default color in the Class
test_figure.change_color("deep-blue")
print(test_figure.figure_color)

# Set up a new type of figure "Oval" with special parameter (diamater)
oval_1 = Oval(12)
print(oval_1.diameter_size)

# Set up a new type of figure "Oval" with special parameters (x, y)
square_1 = Square(3, 7)
print(square_1.width)
print(square_1.height)