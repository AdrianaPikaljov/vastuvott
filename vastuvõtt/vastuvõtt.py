from mmmm import *

def menu():
    while True:
        print("\n1. Alusta testi")
        print("2. Lisa uus küsimus")
        print("3. Välju")

        valik = input("Vali tegevus (1-3): ")
        if valik == "1":
            testi_tegemine()
        elif valik == "2":
            lisa_kysimus()
        elif valik == "3":
            print("Programmist väljumine.")
            break
        else:
            print("Vale valik. Proovi uuesti.") 
menu()
