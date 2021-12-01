""" Завдання_7

Реалізуйте генератор, який приймає на вхід будь-яку ітерабельну послідовність (рядок, список, кортеж) і повертає генератор, який буде вертати значення з цієї послідовності, при цьому, якщо було повернено останній елемент із послідовності - ітерація починається знову.
   Приклад (якщо запустили його у себе - натисніть Ctrl+C ;) ):
   >>>for elem in generator([1, 2, 3]):
   ...    print(elem)
   ...
   1
   2
   3
   1
   2
   3
   1
   .......
"""

# Test iterable data
test_element = ["jj", 12, "fhfgh", ("ff", 55), "test"]

# Printing items from 'test_data' in a circle (as infinite loop)
def my_generator(input_element):

   my_iterator = iter(input_element)
   my_counter = 0

   while my_counter <= len(input_element):
      
      # Reset all parameters when we iterable element
      if my_counter == len(input_element):
         my_iterator = 0
         my_counter = 0 
         my_iterator = iter(input_element)
      
      # Next step (element) inside data
      else:
         print(next(my_iterator))
         my_counter +=1

# Function implementation
print(my_generator(test_element))


