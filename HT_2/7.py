""" Завдання_7

Написати скрипт, який отримає максимальне і мінімальне значення із словника. 
Дані захардкодити.
Приклад словника (можете використовувати свій):
    dict_1 = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60}
Вихідний результат:
    MIN: 10
    MAX: 60
"""

# Test data
test_dict = {"first": 30, "second": 5, "third": 99, "fourth": -7, "fifth": 57}

# Highest and lowest value inside dictionary
min_value = min(test_dict.values())
max_value = max(test_dict.values())

# Output results
print("MIN:", min_value)
print("MAX:", max_value) 