
def view_balance(name):
    print(name)
    #file_name = f"{name}_balance.csv"
    file_name = "thomas_balance.csv"
    with open(file_name, "r", encoding="utf-8") as file:
        xxx = file.readlines()
        print(xxx)

view_balance("Thomas")
print("nnn")