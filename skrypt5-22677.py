import math

def find_sqrt(a):
    return math.sqrt(a)

if __name__ == '__main__':
    # wersja 1
    lista_pierwiastkow = []
    for x in range(1, 257):
        if math.sqrt(x)%2==0:
            lista_pierwiastkow.append(x)
    print(lista_pierwiastkow)
    
    # wersja 2
            
    listapierwiastkow = [x for x in range(1,257) if math.sqrt(x)%2 == 0]
    print(listapierwiastkow)
    