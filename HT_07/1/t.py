import os

def login(user_name, passwod):
    
    #target_path_1 = os.path.dirname(os.path.abspath(__file__))

    users_database = "users.csv"
    try:
        with open(users_database, "r", encoding="utf-8") as file:
            list_of_users = file.readlines()
            

            for lines in list_of_users:
                lines = lines.split(",")
                #if lines[0] == user_name:
                #if lines[1] == passwod:
                if lines[0] == user_name and lines[1] == passwod:
                    f_result = True
                else:
                    f_result = False
    except FileNotFoundError:
        f_result = "looool"

    return f_result

if not login('Thoms', 'ppassww'):
    print("Soory, wrong username or password, try again")
else: