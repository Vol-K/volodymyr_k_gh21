""" Завдання_4

Написати функцію < prime_list >, яка прийматиме 2 аргументи - початок і кінець 
діапазона, і вертатиме список простих чисел всередині цього діапазона.
"""

# Data from user
first_number = input("Please, input number (start range): ")
second_number = input("Please, input number (end range): ")

# Checking is input data are numbers only
def isfloat(num_to_check):
    try:
        float(num_to_check)
        return True
    except ValueError:
        return False

# Searching all prime numbers inside specified range
def prime_list(start_range, end_range):
    
    # Empty element, for subsequent operations
    prime_numbers_list = []

    # Checking is it numbers or no
    if isfloat(start_range) == False or isfloat(end_range) == False:
        prime_number_check = "Sorry, script accept digits only"
    elif float(end_range) < 0:
        prime_number_check = "Sorry, end of range must be bigger than 0"
    else:
        for item in range(int(start_range), int(end_range)):
            # Cut simple option 
            if item < 2:
                prime_number_check = False

            if item == 2 or item == 3:
                prime_number_check = True
                prime_numbers_list.append(item)

            ### Real check of Prime number (Primality test)
            elif item > 3:
                counter = 0
                for i in range(2, item):
                    if item % i == 0:
                        counter +=1
                if counter == 0:
                    prime_numbers_list.append(item)
                else:
                    prime_number_check = False

        prime_number_check = prime_numbers_list
    return prime_number_check

# Function implementation
print(prime_list(first_number, second_number))