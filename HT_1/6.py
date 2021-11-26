# data from user
numbers_group_from_user = input("Please, input a few numbers, use coma as a separator:")
number_from_user = input("Please, input one number:")

# transform input data
numbers_group_from_user = numbers_group_from_user.split(",")
number_from_user = int(number_from_user)

false_counter = 0

# checking all digits from list (step by step)
for i in range(len(numbers_group_from_user)):

    # check input data (is it digit)
    if not numbers_group_from_user[i].isdigit():
        print("Sorry, script accept decimal (positive or negative) digits only")
        break
    
    elif number_from_user == int(numbers_group_from_user[i]):
        print("True")
        break        
    
    # count false answer (for the situation when 'required digit' on the last position)
    # or do not contained in the list
    else:
        false_counter +=1

# when we did not find 'required digit' inside the list
if false_counter == len(numbers_group_from_user):
    print("False")