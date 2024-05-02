
def chech_character(our_input):
    if our_input.isdigit():
        return True
    else:
        return False



if __name__ == '__main__':
    input_w = input("Podaj znak lub znaki: ")
    # 1 sposób z wykorzystaniem isdigit
    if len(input_w)>0: 
        if chech_character(input_w[0]):
            print(f"Podany znak jest cyfrą")
        else:
            print(f"Podany znak nie jest cyfrą")
    else:
        print(f"Nie wpisano znaku")