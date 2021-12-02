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
def my_range(my_stop, my_start=0, my_step=1):

    if my_step == 0:
        raise ValueError
    elif my_stop == 0:
        yield from empty()
    #my_step = my_start + my_step 
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
test = my_range(20, 1, 2)
print(tuple(my_range(20, 1, 2)))
print(list(my_range(20, 1, 2)))

try:
    while True:
        print(next(test))
except StopIteration:
    pass
