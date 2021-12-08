""" Завдання_2

Написати функцію, яка приймає два параметри: ім'я файлу та кількість символів.
   На екран повинен вивестись список із трьома блоками - 
   символи з початку, із середини та з кінця файлу.
   Кількість символів в блоках - та, яка введена в другому параметрі.
   Придумайте самі, як обробляти помилку, наприклад, коли кількість 
   символів більша, ніж є в файлі (наприклад, файл із двох символів 
   і треба вивести по одному символу, то що виводити на місці 
   середнього блоку символів?)
   В репозиторій додайте і ті файли, по яким робили тести.
   Як визначати середину файлу (з якої брать необхідні символи) - 
   кількість символів поділити навпіл, а отримане "вікно" символів 
   відцентрувати щодо середини файла і взяти необхідну кількість. 
   В разі необхідності заокруглення одного чи обох параметрів - 
   дивіться на свій розсуд.

   Наприклад:
   █ █ █ ░ ░ ░ ░ ░ █ █ █ ░ ░ ░ ░ ░ █ █ █    - правильно
                     ⏫ центр

   █ █ █ ░ ░ ░ ░ ░ ░ █ █ █ ░ ░ ░ ░ █ █ █    - неправильно
                     ⏫ центр
"""
## For checking wright path of files
import pathlib
from pathlib import Path

## Output mistake that input number bigger than number of symbols in file
class WrongNumber(Exception):
    pass


# # Data from user, file name & number of characters by this file
# file_name = input("Please, input file name: ")
# number_of_symbols = input("Please, input number of symbols: ")

"""" Test input parameters to the function """
file_name = "symbols.txt"
number_of_symbols = "3"

# Find and get symbols from file (by 3 places).
# From Start of file, Middle and End. 
def get_symbols(*args):

    # Checking input data, is available all parameters
    if len(args) != 2:
        func_result = "Something went wrong, please, input parameters correctly"
    elif not args[1]:
        func_result = "Wrong, please, input number correctly" 
    # If all is good, read the file and select our goals
    else:

        input_file_name = args[0]
        input_numb_of_symbols = int(args[1])

        if input_numb_of_symbols == 0:
            func_result = "Wrong, please, input number bigger than zero"

        else:
            # Read the file and find our symbols for each blocks
            try:
                path = Path(pathlib.Path.cwd(), "2_files", input_file_name)
                with open(path, "r", encoding="utf-8") as file:
                    
                    # Calculate real length of file
                    file_symbols = len(file.read())
                    file.seek(0)
                    file_lines = file.readlines()
                    file.seek(0)
                    if len(file_lines) > 1:
                        file_len = file_symbols + (len(file_lines) - 1)
                    elif len(file_lines) == 1:
                        file_len = file_symbols

                    # Checking is we have enough symbols for output
                    if input_numb_of_symbols > file_len:
                        raise WrongNumber("Uncorrect input number")
                    elif (input_numb_of_symbols * 3) > file_len:
                        raise WrongNumber("Not enough symbols for output")

                    else:
                        # Start block
                        start_file = file.read(input_numb_of_symbols)
                        file.seek(0)

                        # End block
                        if len(file_lines) > 1:
                            file.seek(file_len - input_numb_of_symbols)
                        elif len(file_lines) == 1:
                            file.seek(file_len - input_numb_of_symbols)                       
                        end_file = file.read(-input_numb_of_symbols)
                        file.seek(0)
                        end_file = end_file.replace('\n', '\\n')

                        # Middle block, 3 option by length of file & input number ()
                        # First - all numbers are pair
                        if (file_len % 2) == 0 and (input_numb_of_symbols % 2) == 0:
                            position_of_mid_read = (file_len - input_numb_of_symbols) / 2
                            file.seek(position_of_mid_read)
                            mid_file = file.read(input_numb_of_symbols)
                            file.seek(0)
                            mid_file = mid_file.replace('\n', '\\n')

                        # Second - all numbers are odd
                        elif (file_len % 2) > 0 and (input_numb_of_symbols % 2) > 0:
                            position_of_mid_read = (file_len - (input_numb_of_symbols)) / 2
                            file.seek(position_of_mid_read)
                            mid_file = file.read(input_numb_of_symbols)
                            file.seek(0)
                            mid_file = mid_file.replace('\n', '\\n')
                        
                        # Third - numbers are mixed
                        # Expand middle range for correct output
                        else:
                            position_of_mid_read = (file_len - (input_numb_of_symbols + 1)) / 2
                            file.seek(position_of_mid_read)
                            mid_file = file.read(input_numb_of_symbols + 1)
                            file.seek(0)
                            mid_file = mid_file.replace('\n', '\\n')

                func_result = f"Star of file:: '{start_file}', Middle:: '{mid_file}', End:: '{end_file}'"

            except FileNotFoundError:
                func_result = "File doesn't exist, please input correct file name"
          
    return func_result
     
# Function implementation
print(get_symbols(file_name, number_of_symbols))


