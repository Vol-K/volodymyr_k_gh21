""" Завдання_2

Написати скрипт, який пройдеться по списку, який складається із кортежів, 
і замінить для кожного кортежа останнє значення.
Список із кортежів можна захардкодити. 
Значення, на яке замінюється останній елемент кортежа вводиться користувачем.
Значення, введене користувачем, можна ніяк не конвертувати (залишити рядком). 
Кількість елементів в кортежу повинна бути різна.

Приклад списка котежів: 
    [(10, 20, 40), (40, 50, 60, 70), (80, 90), (1000,)]
Очікуваний результат, якщо введено '100':
	Expected Output: 
    [(10, 20, '100'), (40, 50, 60, '100'), (80, '100'), ('100',)]
"""

# Data from user
data_from_user = input("Please, input value (numbers, letters, etc) for replace it inside tuples: ")

# Tuples with test data
test_list_with_tuples = [("banana",), (12, "Foo", "Bar", -40), ("red", "car", "gg"),\
                         ("testdata", 3410, "milan", "art", 22), ("112", "1xA")]

# Check all elements(tuples) in the list and changing 
# (through transformation to list) last item inside element(tuple) 
# to the user input data.
for i in range(len(test_list_with_tuples)):
    
    #number_of_items = len(test_list_with_tuples[i])        ### Correction by GH lector
    list_from_tuple = list(test_list_with_tuples[i])
    #list_from_tuple[number_of_items-1] = data_from_user    ### Correction by GH lector
    list_from_tuple[-1] = data_from_user                    ### Correction by GH lector
    test_list_with_tuples[i] = tuple(list_from_tuple)

# Output results
print(test_list_with_tuples)