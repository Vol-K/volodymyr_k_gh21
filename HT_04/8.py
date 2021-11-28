""" Завдання_8

Написати функцію, яка буде реалізувати логіку циклічного зсуву 
елементів в списку. Тобто, функція приймає два аргументи: 
список і величину зсуву (якщо ця величина додатня - 
то пересуваємо з кінця на початок, якщо від'ємна - 
то навпаки - пересуваємо елементи з початку списку в його кінець).
   Наприклад:
       fnc([1, 2, 3, 4, 5], shift=1) --> [5, 1, 2, 3, 4]
       fnc([1, 2, 3, 4, 5], shift=-2) --> [3, 4, 5, 1, 2]
"""

# Decoration for print nice first message
def decorator_function(func):
    def wrapper():
        print("Test list:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        func()
        print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    return wrapper

# Test data - list with empty elemets
test_list = ["abra", "", (), ["red", 56], ("tuple", 12),\
             {"car": "mustang"}, {}, []]

# Function for the first message
@decorator_function
def dor_deco_func():
    print(test_list)

# Nice first message 
dor_deco_func()

# Data from user
shift_number = input("Please, input one number for shift elements iside list: ")

# Checking is input data are numbers only
def isfloat(num_to_check):
    try:
        float(num_to_check)
        return True
    except ValueError:
        return False

# Reorder elements inside 'inp_lists'
def list_reorder(inp_lists, shift_step):
    
    # Corection shift step, if its bigger than length of test data
    if float(shift_step) > 0:
        if float(shift_step) > len(inp_lists):
            while float(shift_step) > len(inp_lists):
                new_shift_step = float(shift_step) - len(inp_lists)
                shift_step = new_shift_step
    
    elif float(shift_step) < 0:
        if abs(float(shift_step)) > len(inp_lists):
            while abs(float(shift_step)) > len(inp_lists):
                new_shift_step = float(shift_step) + len(inp_lists)
                shift_step = new_shift_step

    # Checking is it numbers or no
    if isfloat(shift_step) == False:
        func_result = "Sorry, script accept digits only"
    
    # Reorder list from the last element
    elif float(shift_step) < 0:
        negative_op_list = inp_lists.copy()
        for i in range(1, abs(int(shift_step))+1):
            temp_list_element = inp_lists[-i]
            negative_op_list.insert(0, temp_list_element)

        # Delete copied items
        del negative_op_list[int(shift_step):]   
        func_result = negative_op_list

    elif float(shift_step) == 0:
        func_result = inp_lists
    
    # Reorder list from the first element    
    else:
        positive_op_list = inp_lists.copy()
        for i in range(int(shift_step)):
            temp_list_element = inp_lists[i]
            positive_op_list.append(temp_list_element)

        # Delete copied items
        del positive_op_list[0: int(shift_step)]    
        func_result = positive_op_list

    return func_result

# Function implementation
print(list_reorder(test_list, shift_number))