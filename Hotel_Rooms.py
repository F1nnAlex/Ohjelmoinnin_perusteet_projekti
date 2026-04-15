#vapaat ja varatut hotellihuoneet 

#huonetyypit

"""
Room management based on ROOM_TYPES
"""

ROOM_TYPES = {
    "budget": (1, 50),
    "comfort": (51, 99),
    "luxury": (100, 120),
}



# Näytä kaikki huoneet

def view_all_rooms():
    print("\n--- All Rooms ---")

    for room_type, (start, end) in ROOM_TYPES.items():
        for room_number in range(start, end + 1):
            print(f"Room {room_number} | Type: {room_type}")




# Näytä vapaat huoneet

def view_available_rooms(get_available_rooms_function):
    print("\n--- Available Rooms ---")

    for room_type in ROOM_TYPES:
        available_rooms = get_available_rooms_function(room_type)

        if available_rooms:
            print(f"\n{room_type.upper()} rooms:")
            for room in available_rooms:
                print(f"Room {room}")





                

""" #ESIMERKKI Verkkokauppa - Tuotteet, Meidän tapausksessa hotellihuoneet


"""
Tuotteisiin ja tuotteiden hallintaan liittyvät toiminnot
"""

tuote_id = 101
nimi = "TV",
hinta = 499.99
kuvaus = "SmartTV"

tv = {
    "tuote_id": 101,
    "nimi": "TV",
    "hinta": 499.99,
    "kuvaus": "TV",
} 

laptop = {
    "tuote_id": 102,
    "nimi": "Laptop",
    "hinta": 999.99,
    "kuvaus": "Laptop",
}

puhelin = {
    "tuote_id": 103,
    "nimi": "Puhelin",
    "hinta": 199.99,
    "kuvaus": "Puhelin",
           }

# uuden tuotteen luominen
uusi_tuote = {
    "tuote_id": int(input("Tuote ID: ")),
    "nimi": input("Tuotteen nimi: "),
    "hinta": float(input("Tuotteen hinta: ")),
    "kuvaus": input("Tuotteen kuvaus: "),
}

print(uusi_tuote)

# yksinkertaisin tapa ylläpitää tuotekokoelmaa: lista

tuotteet = [tv, laptop, puhelin]

# uuden tuotteen lisääminen: listoille append
# uuden tuotteen voi lisätä myös insert-komennolla, mutta täytyy tietää, mihin indeksiin
# järkevintä, että uudet menee listan loppuun --> append
tuotteet.append(uusi_tuote)

# TODO: poista tuote

# TODO: hae tuote

# TODO: listaa kaikki tuotteet

# TODO: muokkaa tuote
#moi """
