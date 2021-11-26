""" Завдання_8

Написати скрипт, який отримує від користувача позитивне ціле число і створює словник, 
з ключами від 0 до введеного числа, а значення для цих ключів - це квадрат ключа.
Приклад виводу при введеному значенні 5 :
	{0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
"""

# Data from user 
number_from_user = input("Please, input one positive integer:")

# Empty element, for subsequent operations
new_dict = {}

# Creating  pair 'key: value' inside tuple, and update our dictionary.
for i in range(int(number_from_user)+1):
    
    temp_tuple = (i, i**2)
    new_dict.update({temp_tuple[0]: temp_tuple[1]})

# Output results
print(new_dict)       