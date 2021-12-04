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

# Library with a traffic lights (in tuples) for 'Cars' & 'People'
# First element from tuple its sygnal for 'Cars', second for 'People'
traffic_light_lib = [("Red", "Green"), ("Red", "Green"), ("Red", "Green"),
                     ("Red", "Green"), ("Yellow", "Green"), ("Yellow", "Green"),
                     ("Green", "Red"), ("Green", "Red"), ("Green", "Red"),
                     ("Green", "Red"), ("Yellow", "Red"), ("Yellow", "Red")]

# Showing traffic lites sygnal for 'cars' & 'peoples'
def traffic_light():

    # Timer of signal frequency (1 second)
    signal_timer = 1
    
    for item in traffic_light_lib:
        print('{:<8} {}'.format(item[0], item[1]))
        time.sleep(signal_timer)

# Function implementation
while True:
    traffic_light()