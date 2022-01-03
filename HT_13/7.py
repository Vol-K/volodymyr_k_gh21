""" Завдання_7

Створити пустий клас, який називається Thing. Потім створіть об'єкт example 
цього класу. Виведіть типи зазначених об'єктів.
"""


class Thing(object):
    pass


# Test instatnse of class
example = Thing()

# Implementation
print(type(Thing))
print(type(example))