""" Завдання_6

Створіть клас в якому буде атребут який буде рахувати 
кількість створених екземплярів класів.
"""

class MyClass(object):
    """Class has one goal: calculation of class instanses"""

    instanse_counter = 0

    def __init__(self):
        MyClass.instanse_counter += 1
        print(f"{MyClass.instanse_counter} instanses of class was created")


# Implementation
test1 = MyClass()
test2 = MyClass()
test3 = MyClass()
test4 = MyClass()
test5 = MyClass()