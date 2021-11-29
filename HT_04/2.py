""" Завдання_2

Написати функцію < bank > , яка працює за наступною логікою: користувач 
робить вклад у розмірі < a > одиниць строком на < years > років 
під < percents > відсотків (кожен рік сума вкладу збільшується на цей відсоток, 
ці гроші додаються до суми вкладу і в наступному році на них також нараховуються відсотки). 
Параметр < percents > є необов'язковим і має значення по замовчуванню < 10 > (10%). 
Функція повинна принтануть і вернуть суму, яка буде на рахунку.
"""

# User data
money_sum = float(input("Please, input money sum (ex. 124 or 124890): "))
depo_duration = float(input("Please, input years of duration (ex. 1 or 100): "))
depo_percentage = input("Please, input percentage of deposit (ex. 5 or 9): ")

# Calculation of compound percentage
def bank(a, years, percents='10'):
    
    final_sum = a * (1 + (float(percents)/100)) ** years
    print(round(final_sum, 2))  

# Function implementation: using all parameters 
if depo_percentage:
    bank(money_sum, depo_duration, depo_percentage)
# Using only two parameters (if user forgot about percentages) 
else:
    bank(money_sum, depo_duration)    
