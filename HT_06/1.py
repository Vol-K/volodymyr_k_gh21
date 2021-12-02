""" Завдання_1

Програма-світлофор.
Створити програму-емулятор світлофора для авто і пішоходів.
Після запуска програми на екран виводиться в лівій половині - колір 
автомобільного, а в правій - пішохідного світлофора.
Кожну секунду виводиться поточні кольори. 
Через декілька ітерацій - відбувається зміна кольорів - 
логіка така сама як і в звичайних світлофорах.
Приблизний результат роботи наступний:
      Red        Green
      Red        Green
      Red        Green
      Red        Green
      Yellow     Green
      Yellow     Green
      Green      Red
      Green      Red
      Green      Red
      Green      Red
      Yellow     Red
      Yellow     Red
      Red        Green
      .......
"""

import time

print("Print now")
n = 1
x = time.sleep(n)
print(n)
print("Printing after {} seconds".format(n))

# 
list of tuples