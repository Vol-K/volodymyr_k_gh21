""" Завдання_2

2. Створити клас Person, в якому буде присутнім метод __init__ 
    який буде приймати * аргументів, які зберігатиме в відповідні змінні. 
    Методи, які повинні бути в класі Person - show_age, print_name, та
    show_all_information.
    - Створіть 2 екземпляри класу Person та в кожному з екземплярів 
    створіть атребут profession.
"""


class Person(object):
    """Description on Person class.
    
    Each person has a few parameters, as a: person first & second name, 
    full name, age, birth date.

    'show_all_information' method of instance can show information 
    which is not defined in advance."""

    # Initialization of the new class instance
    def __init__(self, f_name, l_name, age, birth_date):
        self.f_name = f_name
        self.l_name = l_name
        self.full_name = " ".join([f_name, l_name])
        self.age = str(age)
        self.birth_date = birth_date

    # Show person age only
    def show_age(self):
        print(f"Person age: {self.age} years")

    # Show person full name only
    def print_name(self):
        print(f"Person full name: {self.full_name}")

    # Show all info about person
    def show_all_information(self):
        print("::All info about Person::")
        person_info = list(self.__dict__.items())
        person_info_len = len(person_info)
        for i in range(2, person_info_len):
            print(f"{person_info[i][0]}: {person_info[i][1]}")


# First test person
person_1 = Person("Jon", "Dou", 12, "12.12.2009")
person_1.print_name()
person_1.show_age()
person_1.profession = "Driver"
person_1.show_all_information()

# Second test person
person_2 = Person("William", "Figo", 51, "08.07.1970")
person_2.print_name()
person_2.show_age()
person_2.profession = "Policeman"
person_2.show_all_information()