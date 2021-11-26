# data from user
color_list_1_from_user = input("Please, input colors in a list #1, use coma as a separator:")
color_list_2_from_user = input("Please, input colors in a list #2, use coma as a separator:")

# delete whitespace before/after word
color_list_1_from_user = color_list_1_from_user.replace(" ", "")
color_list_2_from_user = color_list_2_from_user.replace(" ", "")

# convert strings to the lists
color_list_1_from_user = color_list_1_from_user.split(",")
color_list_2_from_user = color_list_2_from_user.split(",")

# empty element, for subsequent operations
color_compared_list = []

# comparing two lists, and add unique values from the first list only
for i in range(len(color_list_1_from_user)):

    if color_list_1_from_user[i] not in color_list_2_from_user:

        color_compared_list.append(color_list_1_from_user[i])

print(color_compared_list)