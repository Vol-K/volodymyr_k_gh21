""" Завдання_5

Створіть за допомогою класів та продемонструйте свою реалізацію 
шкільної бібліотеки (включіть фантазію).
"""


class Library(object):
    """Class include only one attribute - list of the all books in library. 
    Librarian are managed all books inside library. 
    Students can take book by library and give back. Book which student taken 
    temporarily unavailable to other students."""

    book_list = [{"author": "J.R.R. Tolkien", "book": "The Silmarillion"}, 
                 {"author": "A. Christie", "book": "Murder on the Orient Express"}, 
                 {"author": "A.I. Conan Doyle", "book": "The White Company"},
                 {"author": "A.I. Conan Doyle", "book": "The Adventures of Sherlock Holmes"}, 
                 {"author": "E.N. Luttwak", "book": "Strategy: The Logic of War and Peace"}, 
                 {"author": "R.A. Heinlein", "book": "Orphans of the Sky"}, 
                 {"author": "A.C. Clarke", "book": "Space Odyssey"}, 
                 {"author": "A. Christie", "book": "Poirot Investigates"}]


class Librarian_man(Library):
    """Librarian can add a new item or delete item from the book list, 
    by the author/book_name parameter. 
    If added book exist in library, librarian get a message that he try 
    add a duplicate book. If book unavailable for delete (someone reading it),
     librarian get an error message."""

    def add_book(self, author, book):
        item = {"author": author, "book": book}
        if item in self.book_list:
            print("Sorry, but you try add a book duplicate.")
        else:
            self.book_list.append({"author": author, "book": book})

    def del_book(self, author, book):
        item = {"author": author, "book": book}
        if item not in self.book_list:
            print("Sorry, but this book are reading by someone now.")
        else:
            self.book_list.remove({"author": author, "book": book})


class Student(Library):
    """Student can take a book by library and give back a book.
    Also he has a "reading book" flag, and student can`t take a new book 
    if he didn't give back previous."""

    reading_book = None

    def take_book(self, author, book):
        
        if self.reading_book:
            print(f"You read now: {self.reading_book['author']} - {self.reading_book['book']}.")
            print("Please, give back this book before take a new.")
        else:
            if self.book_list:
                self.reading_book = {"author": author, "book": book}
                self.book_list.remove({"author": author, "book": book})
            else:
                print("Libriary doesn't have available book now.")

    def give_book(self, author, book):
        if not self.reading_book:
            print("You don't read book now")
        else:
            self.reading_book = None
            self.book_list.append({"author": author, "book": book})


# Implementation
test_libliarian = Librarian_man()
student_1 = Student()
student_2 = Student()
student_3 = Student()


test_libliarian.add_book("I. Asimov", "The Bicentennial Man")
# print(test_libliarian.book_list)

student_1.take_book("I. Asimov", "The Bicentennial Man")
student_2.take_book("J.R.R. Tolkien", "The Silmarillion")

# student_1.give_book("A. Christie", "Poirot Investigates")
student_3.take_book("A. Christie", "Poirot Investigates")

test_libliarian.del_book("I. Asimov", "The Bicentennial Man")
# print(test_libliarian.book_list)