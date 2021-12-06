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

# Data from user, file name & number of characters by this file
file_name = input("Please, input file name: ")
number_of_symbols = input("Please, input number of symbols: ")
 
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
        
        # Read the file and find our symbols
        try:
            with open("ss.txt", "r", encoding="utf-8") as file:
                file_len = len(file.read())
                file.seek(0)
                
                file_list = file.readlines()
                file.seek(0)

                start_file = file.read(input_numb_of_symbols)
                file.seek(0)
                """ЧЕРЕЗ file.SEEK"""
                # Select latest symbols by file
                end_file = file_list[-1]
                end_file = end_file[-input_numb_of_symbols:]

                """ЧЕРЕЗ (file_len - input_numb_of_symbols)/2 """
                """ЧЕРЕЗ file.SEEK"""
                #mid_file = int(round(file_len / 2, 0))
                mid_file = int(round(file_len / 2, 0))

                if input_numb_of_symbols == 0:
                    func_result = "Wrong, please, input number bigger than zero"
                elif input_numb_of_symbols > len(file.read()):
                    func_result = "Wrong, please, input less number"
                #else:

        except FileNotFoundError:
            func_result = "File doesn't exist, please input correct file name"
        
        mid_file = 2222
        #end_file = 33333
        #print(f"Star of file:: '{start_file}', Middle:: '{mid_file}', End:: '{end_file}'")  
        func_result = f"Star of file:: '{start_file}', Middle:: '{mid_file}', End:: '{end_file}'"
        
    return func_result
     

# Function implementation
print(get_symbols(file_name, number_of_symbols))


