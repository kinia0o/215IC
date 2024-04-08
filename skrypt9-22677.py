class Vehicle:
    def __init__(self, nazwa, rok_produkcji, przebieg):
        self.nazwa = nazwa
        self.rok_produkcji = rok_produkcji
        self.przebieg = przebieg
        
    def is_long(self):
        return self.przebieg>200000
        
    def is_old(self):
        return self.rok_produkcji<2000

class Car:
    def __init__(self, nazwa, rok_produkcji, przebieg):
        self.nazwa = nazwa
        self.rok_produkcji = rok_produkcji
        self.przebieg = przebieg
    def is_long(self):
        return self.przebieg>200000
    @property    
    def is_old(self):
        return self.rok_produkcji<2000
        
class Third(Car, Vehicle):
    pass

if __name__ == '__main__':
    v1 = Vehicle("Ford", 1999,150000)
    c1 = Car("VW", 1990,500000)
    t1 = Third("Toyota",2007,50000)
    
    print(v1.is_old())
    print(c1.is_old)
    print(t1.is_old)
    
    
    print(v1.nazwa)