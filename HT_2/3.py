""" Завдання_3 

Написати скрипт, який видалить пусті елементи із списка. 
Список можна 'захардкодити'.

Sample data: 
    [(), (), ('',), ('a', 'b'), {}, ('a', 'b', 'c'), ('d'), '', []]
Expected output: 
    [('',), ('a', 'b'), ('a', 'b', 'c'), 'd']
"""

# Test data, list with empty elemets
test_list = ["abra", "", (), ["red", 56], ("tuple", 12),\
             {"car": "mustang"}, {}, []]

# Empty element, for subsequent operations
temp_list = []

# Checking whole list (item by item) 
# and copy (to the 'temp_list') non empty elements only.
for i in range(len(test_list)):

    if len(test_list[i]) > 0:

        temp_list.append(test_list[i])

# Transforming our test data ('test_list')
test_list.clear()
test_list = temp_list.copy()

# Output results
print(test_list)