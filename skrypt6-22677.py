import random
import string


if __name__ == '__main__':
    S22677 = dict()
    for i in range(10,21):
        element = ''.join(random.choices(string.ascii_letters, k=8))
        print(element)
        S22677[i]=element
    print(S22677)
