# data from user
number_from_user = input("Please, input one positive integer:")

# checking input data, and make operation with it
if number_from_user.isnumeric():
    
    x = int(number_from_user)
    sum_of_integers = x*(1+x)//2
    print(sum_of_integers)

else:
    print("Sorry, script accept one positive integer only")
