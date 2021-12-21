""" Завдання_1

Сайт для виконання завдання: https://jsonplaceholder.typicode.com

Написати програму, яка буде робити наступне:
1. Робить запрос на https://jsonplaceholder.typicode.com/users і вертає коротку інформацію про користувачів (ID, ім'я, нікнейм)
2. Запропонувати обрати користувача (ввести ID)
3. Розробити наступну менюшку (із вкладеними пунктами):
1. Повна інформація про користувача
2. Пости:
- перелік постів користувача (ID та заголовок)
- інформація про конкретний пост (ID, заголовок, текст, кількість коментарів + перелік їхніх ID)
3. ТУДУшка:
- список невиконаних задач
- список виконаних задач
4. Вивести URL рандомної картинки
"""

import requests
import json
import time
from random import choice


# Main menu
def menu(user_id):
    print("")
    if int(user_id) != 10:
        print(f"................## {user_id} ##...................")
    else:
        print(f"...............## {user_id} ##...................")
    print("Please choose one operation from this list")
    time.sleep(0.2)

    menu = [[1, "All info by User"], [2, "Posts by Users"], [3, "User TODO"],
            [4, "Get random photo url"], [5, "Exit"]]
    oper_flag = False

    for item in menu:
        print(f"{item[0]} - {item[1]}")
        time.sleep(0.5)

    user_option = input("Select 1, 2, 3 4, or 5: ")
    oper_flag = check_valid(user_option, "menu")

    return user_option, oper_flag


# Validation of chosen menu option
def check_valid(value, func_name):
    
    # Select granted symbols for each function
    if func_name == "menu":
        granted_symbols = "12345"
    elif func_name == "check_id_selection":
        granted_symbols = "12345678910"
    elif func_name == "post_menu" or func_name == "todo_menu":
        granted_symbols = "12"
    elif func_name == "one_post_info":
        granted_symbols = [str(n) for n in range(1, 101)]

    # Check selcted option (is it valid)
    if value not in granted_symbols:
        f_res = False
    elif len(value) < 1:
        f_res = False
    elif value == "0":
        f_res = False
    else:
        f_res = True

    return f_res


# Menu for Post option
def post_menu():
    print("")
    print("..........................................")
    print("Please choose one option")
    time.sleep(0.2)

    menu = [[1, "All posts by User"], [2, "Detailed info about one post"]]
    for item in menu:
        print(f"{item[0]} - {item[1]}")
        time.sleep(0.5)

    user_option = input("Select 1, or 2: ")
    oper_flag = check_valid(user_option, "post_menu")
    
    return user_option, oper_flag


# Short info about all posts by user
def all_user_posts(user_id):

    print(".............All posts by User............")
    print("")

    api_link = f'https://jsonplaceholder.typicode.com/posts?userId={user_id}'
    all_posts =  requests.get(api_link)
    all_posts = json.loads(all_posts.text)

    for item in all_posts:
        print("..........................................")
        print(f"Post id::     {item['id']}")
        print(f"Post title::  {item['title']}")
        time.sleep(0.3)


# Info about selected post by user
def one_post_info(user_id):
    
    api_link = f"https://jsonplaceholder.typicode.com/posts?userId={user_id}"
    all_posts =  requests.get(api_link)
    all_posts = json.loads(all_posts.text)

    list_of_posts = []
    print("..........................................")
    for item in all_posts:
        list_of_posts.append(item['id'])
        print(f"Post id: {item['id']}")
        time.sleep(0.2)
    print("..........................................")

    post_id = input("Please choose one post to the view detail info: ")
    print("..........................................")
    oper_flag = check_valid(post_id, "one_post_info")

    if not oper_flag:
        print("Input wrong value")
    elif int(post_id) not in list_of_posts:
        print("Inputed uncorrect post ID")
    else:
        for item in all_posts:
            if int(post_id) == item['id']:
                print("{:<20} {}".format('Post id::', item['id']))
                time.sleep(0.2)
                print("{:<20} {}".format('Post title::', item['title']))
                time.sleep(0.2)
                print("{:<20} {}".format('Post body::', item['body']))
                time.sleep(0.2)

                post_comments_api = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"
                post_comments =  requests.get(post_comments_api)
                post_comments = json.loads(post_comments.text)

                print("{:<20} {}".format('Amount of comments::', len(post_comments)))
                time.sleep(0.2)

                comments_id = []
                for element in post_comments:
                    comments_id.append(element["id"])
                comments_id = ', '.join([str(elem) for elem in comments_id])
                print("{:<20} {}".format("Comments ID's::", comments_id))
                time.sleep(0.2)


# To-Do list options
def todo_menu():
    print("")
    print("..........................................")
    print("Please choose one option")
    time.sleep(0.2)

    menu = [[1, "In progress task"], [2, "Finished task"]]
    for item in menu:
        print(f"{item[0]} - {item[1]}")
        time.sleep(0.5)

    user_option = input("Select 1, or 2: ")
    oper_flag = check_valid(user_option, "todo_menu")
    
    return user_option, oper_flag


# Select todo status & print 
def task_workflow(user_id, todo_status):
    
    td_api_link = f'https://jsonplaceholder.typicode.com/users/{user_id}/todos'
    todos_db =  requests.get(td_api_link)
    todos_db = json.loads(todos_db.text)

    for item in todos_db:
        if todo_status == "done":
            if item["completed"] == True:
                print("..........................................")
                print("{:<12} {}".format('Post id::', item['id']))
                time.sleep(0.2)
                print("{:<12} {}".format('Post title::', item['title']))
                time.sleep(0.2)

        elif todo_status == "progress":
            if item["completed"] == False:
                print("..........................................")
                print("{:<12} {}".format('Post id::', item['id']))
                time.sleep(0.2)
                print("{:<12} {}".format('Post title::', item['title']))
                time.sleep(0.2)


# Get all info about User
def all_info(user_id, users):
    print(".............All info by User.............")
    for item in users:
        if int(user_id) == item['id']:
            print("{:<30} {}".format('User ID::', item['id']))
            time.sleep(0.2)
            print("{:<30} {}".format('Name::', item['name']))
            time.sleep(0.2)
            print("{:<30} {}".format('Username::', item['username']))
            time.sleep(0.2)
            print("{:<30} {}".format('User email:: ', item['email']))
            time.sleep(0.2)
            print("{:<30} {} {}".format('User address (city & street)::', item['address']['city'], item['address']['street']))
            time.sleep(0.2)
            print("{:<30} {}".format('Phone::', item['phone']))
            time.sleep(0.2)
            print("{:<30} {}".format('Website:: ', item['website']))
            time.sleep(0.2)
            print("{:<30} {}".format('Company (work)::', item['company']['name']))
            time.sleep(0.2)


# Get & print random photo link
def random_photo():
    print("")
    print("........Short info of random photo........")
    photo_lib = requests.get('https://jsonplaceholder.typicode.com/photos')
    photo_lib = json.loads(photo_lib.text)

    random_photo_url = choice(photo_lib)
    print("{:<13} {}".format('Photo ID::', random_photo_url["id"]))
    print("{:<13} {}".format('Album ID::', random_photo_url["albumId"]))
    print("{:<13} {}".format('Photo title::', random_photo_url["title"]))
    print("{:<13} {}".format('Photo url::', random_photo_url["url"]))


# Application workflow 
def main_workflow():

    user_db = requests.get("https://jsonplaceholder.typicode.com/users")
    user_db = json.loads(user_db.text)

    print("..........................................")
    for item in user_db:
        print(f"User ID: {item['id']}")
        time.sleep(0.2)
    print("..........................................")
    choose_user_id = input("Please select user from this ist: ")
    
    choose_user_id_check = False
    while not choose_user_id_check:
        if check_valid(choose_user_id, "check_id_selection"):
            choose_user_id_check = True
        else:
            print("Inputed wrong option")
            time.sleep(0.2)
            choose_user_id = input("Please select user from this ist: ")

    app_menu = menu(choose_user_id)
    exit_flag = False
    while exit_flag == False:
        if not app_menu[1]:
            print("Inputed wrong menu option")
            time.sleep(0.2)
            app_menu = menu(choose_user_id)

        elif int(app_menu[0]) == 1:
            all_info(choose_user_id, user_db)
            app_menu = menu(choose_user_id)

        elif int(app_menu[0]) == 2:
            p_menu_option = post_menu()
            
            if not p_menu_option[1]:
                print("Inputed wrong selection")
                time.sleep(0.2)
            elif int(p_menu_option[0]) == 1:
                all_user_posts(choose_user_id)
            elif int(p_menu_option[0]) == 2:
                one_post_info(choose_user_id)
            app_menu = menu(choose_user_id)

        elif int(app_menu[0]) == 3:
            td_menu = todo_menu()

            if not td_menu[1]:
                print("Inputed wrong selection")
                time.sleep(0.2)
            elif int(td_menu[0]) == 1:
                task_workflow(choose_user_id, "progress")
            elif int(td_menu[0]) == 2:
                task_workflow(choose_user_id, "done")
            app_menu = menu(choose_user_id)

        elif int(app_menu[0]) == 4:
            random_photo()
            app_menu = menu(choose_user_id)    
        elif int(app_menu[0]) == 5:
            exit_flag = True
            print("...............Good luck..................")

    
# Function implementation
main_workflow()