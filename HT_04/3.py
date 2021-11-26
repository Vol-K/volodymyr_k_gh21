""" Завдання_3

Написати функцию < is_prime >, яка прийматиме 1 аргумент - число від 0 до 1000, 
і яка вертатиме True, якщо це число просте, и False - якщо ні.
"""

# Data from user
user_number = input("Please, input one number: ")

# Checking input number: is it a Prime number
def is_prime(x):

    counter = 0
    # Checking is it numbers or no
    if  x.isdigit():

        # Checking number inside our range or no
        if 0 <= int(x) <= 1000:
            
            # Cut simple option 
            if int(x) < 2:
                prime_number_check = False

            if int(x) == 2 or int(x) == 3:
                prime_number_check = True

            ### Real check of Prime number (Primality test)
            elif int(x) > 3:
                for item in range(2, int(x)):
                    if int(x) % item == 0:
                        counter +=1
                if counter == 0:
                    prime_number_check = True
                else:
                    prime_number_check = False

        else:
            prime_number_check = "Sorry, number outside the range"
    
    else:
        prime_number_check = "Sorry, script accept digits only"

    return prime_number_check

# Function implementation
print(is_prime(user_number))

## or sympy.isprime()