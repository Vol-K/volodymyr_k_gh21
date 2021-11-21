""" Завдання_5

Написати скрипт, який залишить в словнику тільки пари з унікальними значеннями 
(дублікати значень - видалити). Словник для роботи захардкодити свій.

Приклад словника (не використовувати):
    {'a': 1, 'b': 3, 'c': 1, 'd': 5}
Очікуваний результат:
    {'a': 1, 'b': 3, 'd': 5}
"""

# Test data
test_dict = {"first": 30, "second": 5, "third": 99, "fourth": 5, "fifth": 57,\
             "sixth": 57, "seventh": 43}

# Support elements, for subsequent operations, 
# 'dict' copy and 'list of items' for iteration.
new_dict = test_dict.copy()
list_of_items = list(test_dict.items())

# Comparing all values in dictionary by each other, 
# and removing duplicates inside 'new_dict' by 'keys'.
for i in range(len(test_dict)):
    
    for j in range(i+1, len(test_dict)):

        if list_of_items[i][1] == list_of_items[j][1]:
      
            new_dict.pop(list_of_items[j][0])

# Output results
print(new_dict)

### Correction by GH lector
# простіше рішення - 
# https://stackoverflow.com/questions/8749158/removing-duplicates-from-dictionary