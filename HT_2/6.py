""" Завдання_6
Написати скрипт, який об'єднає три словника в самий перший. 
Оновлюється тільки перший словник. Дані можна "захардкодити".
Sample Dictionary :
	dict_1 = {1:10, 2:20}
	dict_2 = {3:30, 4:40}
	dict_3 = {5:50, 6:60}
Expected Result : 
    dict_1 = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60}
"""

# Test data
first_dict = {"name": "Bond"}
second_dict = {"full name": "James Bond"}
third_dict = {"agent code": "007"}

# Updating first dictionary
first_dict = first_dict | second_dict | third_dict

# Output results
print(first_dict)