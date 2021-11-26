""" Завдання_2

Написати функцію < bank > , яка працює за наступною логікою: користувач 
робить вклад у розмірі < a > одиниць строком на < years > років 
під < percents > відсотків (кожен рік сума вкладу збільшується на цей відсоток, 
ці гроші додаються до суми вкладу і в наступному році на них також нараховуються відсотки). 
Параметр < percents > є необов'язковим і має значення по замовчуванню < 10 > (10%). 
Функція повинна принтануть і вернуть суму, яка буде на рахунку.
"""

# User data
money_sum = input("Please, input money sum (ex. 124.8 or 124890): ")
depo_duration = input("Please, input years of duration (ex. 1 or 100): ")
depo_percentage = input("Please, input percentage of deposit (ex. 5 or 5.5): ")

# Checking is input data are numbers only
def isfloat(num_to_check):
    try:
        float(num_to_check)
        return True
    except ValueError:
        return False

# Calculation of compound percentage
def bank(a, years, percents=10):

    # Checking is all our data are numbers 
    if isfloat(a) == True and isfloat(years) and isfloat(percents):

        # Mathematics
        final_sum = float(a) * (1 + (float(percents)/100)) ** float(years)

        # Output results
        print(round(final_sum, 2))
        
    else:
        print("Sorry, script accept digits only")

# First option: using all parameters 
if depo_percentage:
    bank(money_sum, depo_duration, depo_percentage)

# Second option: using only two parameters (if user forgot about percentages) 
else:
    bank(money_sum, depo_duration)    
