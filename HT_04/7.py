""" Завдання_7

Написати функцію, яка приймає на вхід список 
і підраховує кількість однакових елементів у ньому.
Уточнение к заданию 7: нужно вывести количество повторений элементов в списке 
(элементом может быть что-угодно - число, буква, символ, список, кортеж и т.д.). 
Например для списка [1, 3, 3, 1, 1, 1, 1, g, (1, "a", 2), (1, "a", 2)] - 
результат : 1 - 5 раз, 3 - 2 раза, g - 1 раз, (1, "a", 2) - 2 раза и т.д. 
Считать 1 за повторение или нет - на ваше усмотрение. 
Цель задания: повторение циклов и типов данных
"""

# Data from user
user_list = input("Please, input data to the 'list', use coma as separator: ")
user_count_parameter = input("Do you want to count one item as repeating? Y/N: ")

# Searching repeated values inside input 'list'
def repeat_counter(inp_str):

    if len(inp_str) == 0:
        func_result = "Sorry, you did not put data"
    else:
        count_dict = {}
        inp_list = inp_str.split(",")
        
        # Added each elements to the 'dict' and count how many times its repeated
        for item in inp_list:
            if not item in count_dict:
                count_dict[item] = 1
            else:
                count_dict[item] += 1

        func_result = count_dict.copy()
    return func_result

if len(user_count_parameter) == 0 or len(user_count_parameter) > 1 or user_count_parameter == None:
    print("Sorry, wrong counter parameter2")

elif len(user_count_parameter) == 1 and user_count_parameter == "Y":
    if len(user_list) == 0:
        print("Sorry, you did not put data")
    else:
        # Function implementation
        print(list(repeat_counter(user_list).items()))

elif len(user_count_parameter) == 1 and user_count_parameter == "N":
    if len(user_list) == 0:
        print("Sorry, you did not put data")
    else:
        list_of_tuples = list(repeat_counter(user_list).items())
        
        # Empty element, for subsequent operations
        more_than_one_repeat = []

        for i in range(len(list_of_tuples)):
            if list_of_tuples[i][1] > 1:
                more_than_one_repeat.append(list_of_tuples[i])
        print(more_than_one_repeat)

# from collections import Counter
#def repeat_counter(inp_str):
#    inp_str = inp_str.split(",")
#    f_result = dict(Counter(inp_str))
#    return f_result