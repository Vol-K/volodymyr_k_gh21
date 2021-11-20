""" Завдання_1

Написати скрипт, який конкатенує всі елементи в списку і виведе їх на екран. 
Список можна "захардкодити".
Елементами списку повинні бути як рядки, так і числа.
"""

# List with test data
list_for_concatenation = ['AbBa', 5, 'FooBar2k', '1xA', -20]

# Concatenation with transform all elements in the list to 'str' type.
concatenated_all_elements = ''.join(map(str, list_for_concatenation))

print(concatenated_all_elements)