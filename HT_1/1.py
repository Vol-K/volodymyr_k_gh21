# data from user
numbers_from_user = input("Please, input a few integer, use coma as a separator:")

# transform string to the list (for including negative number)
numbers_from_user = numbers_from_user.split(",")

# empty element, for subsequent operations
list_from_user_data = []

# check all symbols in user data
for i in range(len(numbers_from_user)):

    # accept numbers only
    if numbers_from_user[i].isdigit() or numbers_from_user[i][0] == "-":

        list_from_user_data.append(numbers_from_user[i])

# transforming list to the tuple
tuple_from_user_data = tuple(list_from_user_data)

# print of results
print(list_from_user_data)
print(tuple_from_user_data)
