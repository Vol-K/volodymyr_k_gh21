# data from user
number_of_string_from_user = input("Please, input amount of string for join:")

# check, numbers only
if number_of_string_from_user.isdigit():
    
    # check,] numbers bigger than 0
    if int(number_of_string_from_user) > 0:
         
        # empty elements, for subsequent operations
        list_of_strings_by_user = []
        concatenated_strings = ""

        # get amount of strings equal of digit which we got from user and add they to the list
        for i in range(int(number_of_string_from_user)):
            
            new_string_from_user = input("Please, input value to the string:")
            list_of_strings_by_user.append(new_string_from_user)
            
            # joining the strings
            concatenated_strings = concatenated_strings + new_string_from_user

        # output results
        print(concatenated_strings)
    
    else:
        print("Sorry, please input number bigger than zero")

else:
    print("Sorry, at first input amount (positive numbers) of string for join") 