""" Завдання_1

Програма-банкомат.
Створити програму з наступним функціоналом:
    - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль (файл <users.data>);
    - кожен з користувачів має свій поточний баланс (файл <{username}_balance.data>) 
    та історію транзакцій (файл <{username}_transactions.data>);
    - є можливість як вносити гроші, так і знімати їх. Обов'язкова перевірка введених даних 
    (введено число; знімається не більше, ніж є на рахунку).
Особливості реалізації:
    - файл з балансом - оновлюється кожен раз при зміні балансу (містить просто цифру з балансом);
    - файл - транзакціями - кожна транзакція у вигляді JSON рядка додається в кінець файла;
    - файл з користувачами: тільки читається. Якщо захочете реалізувати функціонал додавання 
    нового користувача - не стримуйте себе :)
Особливості функціонала:
    - за кожен функціонал відповідає окрема функція;
    - основна функція - <start()> - буде в собі містити весь workflow банкомата:
    - спочатку - логін користувача - програма запитує ім'я/пароль. 
    Якщо вони неправильні - вивести повідомлення про це і закінчити роботу 
    (хочете - зробіть 3 спроби, а потім вже закінчити роботу - все на ентузіазмі :) )
    - потім - елементарне меню типа:
    Введіть дію:
        1. Продивитись баланс
        2. Поповнити баланс
        3. Вихід
    - далі - фантазія і креатив :)
"""

def start():
    pass


def transaction():
    pass


def login():
    pass


def view_balance():
    pass


def update_balance():
    pass
