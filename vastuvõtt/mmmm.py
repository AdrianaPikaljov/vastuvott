import random 
import smtplib
from email.message import EmailMessage
import ssl



# Funktsioon e-kirja saatmiseks
def saada_email(teade_emailile, teema, sisu):
    server = 'smtp.gmail.com'
    port = 587  # Säilitatud algne port
    saatja = "pikaljovadri@gmail.com"
    parool = "muir tvyq fdls idfr"

    # Loome e-kirja
    kiri = EmailMessage()
    kiri['Subject'] = teema
    kiri['From'] = saatja
    kiri['To'] = teade_emailile
    kiri.set_content(sisu)

    # Ühendume serveriga ja saadame sõnumi
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(server, port) as server:
            server.starttls(context=context)
            server.login(saatja, parool)
            server.send_message(kiri)
            print("Tulemused saadetud!")
    except Exception as e:
        print(f"Kirja saatmine ebaõnnestus: {e}")

# Loeb failist küsimused ja vastused
def loe_kysimused():
    kysimused = {}
    with open("kusimused_vastused.txt", "r", encoding="utf-8") as f:
        for rida in f:
            if ":" in rida:
                kysimus, vastus = rida.strip().split(":", 1) #strip() eemaldab tühikud ja reavahed ja split() jagab küsimuse ja vastuse
                kysimused[kysimus.strip()] = vastus.strip()
    return kysimused

# Funktsioon testimise läbiviimiseks
def testi_tegemine():
    kysimused = loe_kysimused()
    vastajad = []
    osalejate_arv = 2
    kysimuste_arv = 5


    for i in range(osalejate_arv):
        print(f"\nOsaleja {i+1}") #i algab 0-st, seega +1, \n teeb reavahet
        nimi = input("Sisesta oma nimi: ")
        email = input("Sisesta oma e-mail: ")

        if nimi in vastajad:
            print("See nimi on juba kasutusel.")
            continue

        vastajad.append(nimi) #lisab nimekirja loppu
        valitud_kysimused = random.sample(list(kysimused.items()), kysimuste_arv)  #valib juhuslikult küsimused ja kysimused teeme listiks sest random.sample 
        oigesti = 0

        # Küsimuste esitamine
        for kysimus, oige_vastus in valitud_kysimused:
            vastus = input(kysimus + " ")
            if vastus.strip().lower() == oige_vastus.lower():
                oigesti += 1

        tulemus = f"{nimi} – {oigesti} õigesti"

        # Salvestamine vastavalt tulemusele
        if oigesti >= (kysimuste_arv // 2 + 1): #loetakse nullist selle parast +1 ja loetakse ainult taisarve
            with open("vastuvõetud.txt", "a", encoding="utf-8") as f:
                f.write(tulemus + "\n")
            seis = "Test edukalt sooritatud."
        else:
            with open("eisoobi.txt", "a", encoding="utf-8") as f:
                f.write(nimi + "\n")
            seis = "Testi ei sooritatud edukalt."

        # Salvestame kõik tulemused
        with open("kõik.txt", "a", encoding="utf-8") as f:
            f.write(f"{nimi} – {oigesti} – {email}\n")

        # Saadame e-maili
        teema = "Sinu testitulemused"
        sisu = f"Tere {nimi}!\nSaid õigesti {oigesti} küsimust.\n{seis}"
        saada_email(email, teema, sisu)


    print("\nKõik testid on tehtud.")
    print("Tulemused saadetud e-posti aadressidele.")


# Funktsioon uue küsimuse lisamiseks
def lisa_kysimus():
    uus = input("Sisesta uus küsimus: ")
    vastus = input("Sisesta õige vastus: ")
    with open("kusimused_vastused.txt", "a", encoding="utf-8") as f:
        f.write(uus + ":" + vastus + "\n")
    print("Küsimus lisatud!")
