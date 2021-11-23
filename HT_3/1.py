""" Завдання_1

Створити цикл від 0 до ... (вводиться користувачем). 
В циклі створити умову, яка буде виводити поточне значення, 
якщо остача від ділення на 17 дорівнює 0.
"""

# Data from user
user_number = input("Please, input first number: ")

# Check input data (is it number only)
if not user_number.isnumeric():
    print("Sorry, script accept digit only")

# Searching numbers which divisible by 17 without residue, and print it
else:
    for i in range(int(user_number)):
        if i % 17 == 0:
                print(i)

#x = 0
#while x < int(user_number):
#    if x % 17 == 0:  
#        print(x)
#    x += 1