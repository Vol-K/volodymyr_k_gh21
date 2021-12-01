""" Завдання_6

Всі ви знаєте таку функцію як <range>. Напишіть свою реалізацію цієї функції.
   P.S. Повинен вертатись генератор.
   P.P.S. Для повного розуміння цієї функції - можна почитати документацію по ній: 
   https://docs.python.org/3/library/stdtypes.html#range
"""


def my_range(my_start=0, my_stop, my_step=1):

    while my_start < my_stop:
        my_start += my_step
        yield my_start
        print(my_start)

#
def my_range(input_item):
    i = 0
    while i < input_item:
        i += 1
        yield i
        print(i)


xx = my_range(7)
next(xx)
next(xx)