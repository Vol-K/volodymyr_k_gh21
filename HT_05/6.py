""" Завдання_6

Всі ви знаєте таку функцію як <range>. Напишіть свою реалізацію цієї функції.
   P.S. Повинен вертатись генератор.
   P.P.S. Для повного розуміння цієї функції - можна почитати документацію по ній: 
   https://docs.python.org/3/library/stdtypes.html#range
"""

def empty():
    return
    yield 

# 
def my_range(*args):

    # Check amount of input arguments, and define of values
    if len(args) == 1:
        my_start = 0
        my_stop = args[0]
        my_step = 1
    elif len(args) == 2:
        my_start = args[0]
        my_stop = args[1]
        my_step = 1
    elif len(args) == 3:
        my_start = args[0]
        my_stop = args[1]
        my_step = args[2]
    else:
        raise OverflowError 

    # Logic of 'my_range' function
    if my_step == 0:
        raise ValueError
    elif my_stop == 0:
        yield from empty()
    else:
        # positive 'step'
        if my_step > 0:
            while my_start < my_stop:
                yield my_start
                my_start += my_step  
        # negative 'step" 
        if my_step < 0:
            while my_stop > my_start:
                yield my_stop
                my_stop += my_step

# Function implementation
test = my_range(20)
print(tuple(my_range(6)))
print(list(my_range(20)))

try:
    while True:
        print(next(test))
except StopIteration:
    pass
