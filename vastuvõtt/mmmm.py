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
                kysimus, vastus = rida.strip().split(":", 1)
                kysimused[kysimus.strip()] = vastus.strip()
    return kysimused

# Funktsioon testimise läbiviimiseks
def testi_tegemine():
    kysimused = loe_kysimused()
    vastajad = []
    osalejate_arv = 3
    kysimuste_arv = 5
    koondaruanne = []  # Salvestame kõik tulemused koondaruande jaoks

    for i in range(osalejate_arv):
        print(f"\nOsaleja {i+1}")
        nimi = input("Sisesta oma nimi: ")
        email = input("Sisesta oma e-mail: ")

        if nimi in vastajad:
            print("See nimi on juba kasutusel.")
            continue

        vastajad.append(nimi)
        valitud_kysimused = random.sample(list(kysimused.items()), kysimuste_arv)
        oigesti = 0

        # Küsimuste esitamine
        for kysimus, oige_vastus in valitud_kysimused:
            vastus = input(kysimus + " ")
            if vastus.strip().lower() == oige_vastus.lower():
                oigesti += 1

        tulemus = f"{nimi} – {oigesti} õigesti"

        # Salvestamine vastavalt tulemusele
        if oigesti >= (kysimuste_arv // 2 + 1):
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

        koondaruanne.append((nimi, oigesti, email, seis))

    print("\nKõik testid on tehtud.")
    print("Tulemused saadetud e-posti aadressidele.")

        # Tööandjale saatmine
    saadetav_koondaruanne = "\n".join([f"{i+1}. {k[0]} - {k[1]} punkti - {k[2]} - {'SOBIB' if k[1] >= (kysimuste_arv // 2 + 1) else 'EI SOBI'}" for i, k in enumerate(koondaruanne)])
    parim_kandidaat = max(koondaruanne, key=lambda x: x[1])

    koondaruanne_sisu = f"""
    Tere!

    Allpool on nimekiri kõigist tänases sessioonis testitud kandidaatidest:

    {saadetav_koondaruanne}

    Parim kandidaat: {parim_kandidaat[0]} ({parim_kandidaat[1]} punkti)

    Lugupidamisega,
    Automaatne Testimissüsteem
    """

    # Saadame koondaruande tööandjale
    teema = "Testitulemuste koondaruanne"
    tööandja_email = "tootaja@firma.ee"
    saada_email(tööandja_email, teema, koondaruanne_sisu)

# Funktsioon uue küsimuse lisamiseks
def lisa_kysimus():
    uus = input("Sisesta uus küsimus: ")
    vastus = input("Sisesta õige vastus: ")
    with open("kusimused_vastused.txt", "a", encoding="utf-8") as f:
        f.write(uus + ":" + vastus + "\n")
    print("Küsimus lisatud!")


# Peamenüü
def menuu():
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
menuu()