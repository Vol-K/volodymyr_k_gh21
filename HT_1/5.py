# data from user
number_from_user = input("Please, input one decimal integer:")

# checking input data, and convert it
if number_from_user.isdigit() == True or number_from_user[0] == "-":
    
    number_converter = hex(int(number_from_user))
    print(number_converter)
   
else:
    print("Sorry, script accept decimal (positive or negative) digits only")