

if __name__ == '__main__':
    input_w = input("Podaj znak lub znaki: ")
   
    if len(input_w)>0: 
        if all(literka.isdigit() for literka in input_w):
            print(f"Podany ciąg jest liczbą")
        else:
            print(f"Podany ciąg nie jest liczbą")
    else:
        print(f"Nie wpisano znaku")

