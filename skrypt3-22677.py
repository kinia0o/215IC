

if __name__ == '__main__':
    input_1 = input("Podaj jakiś łańcuch znakowy: ")
    input_2 = input("Podaj szukanego ciągu znaków")
    if len(input_1)>0 and len(input_2)>0: 
        print(input_1.find(input_2))
    else:
        print(f"Nie podano jednego z łańcuchów")