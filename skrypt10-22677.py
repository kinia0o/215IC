def ascii_to_letters(liczba):
    return chr(liczba)

if __name__ == '__main__':
    letters = []
    for i in range(65,91):
        letters.append(ascii_to_letters(i))
    letters_string = ''.join(letters)
    print(letters)
    print(letters_string)
    with open("alfabet1-22677.txt","w") as file:
        file.write(letters_string)
    
    with open("alfabet1-22677.txt","w") as file:
        for letter in letters_string:
            file.write(f"{letter}\n")
        