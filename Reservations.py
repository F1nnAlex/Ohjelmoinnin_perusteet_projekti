#VERKKOKAUPPA ESIMERKKI - Tilaukset , meidän tapauksessa varaukset


# bookings.py

"""
Booking module
Connects customers and rooms
"""

import Customers
import Hotel_Rooms


# -------------------------
# Tee varaus (check-in)
# -------------------------
def book_room():
    print("\n--- Book a Room ---")

    # Näytä vapaat huoneet
    Hotel_Rooms.view_available_rooms(Customers.get_available_rooms)

    # Kutsutaan asiakkaan check-in funktiota
    Customers.assign_guest()

    print("Room booking completed.")


# -------------------------
# Check-out
# -------------------------
def checkout():
    print("\n--- Checkout ---")

    Customers.checkout_guest()

    print("Checkout completed.")


# -------------------------
# Näytä kaikki aktiiviset varaukset
# -------------------------
def view_bookings():
    print("\n--- Active Bookings ---")

    Customers.list_active_guests()


# -------------------------
# Etsi varaus
# -------------------------
def find_booking():
    print("\n--- Find Booking ---")

    Customers.view_customer()


"""
Tilaukset ja niiden hallinta
==============================

Ominaisuudet:
* lisää uusi tilaus
* poista tilaus
* hae tilauksen tiedot

import Tuotteet, Asiakkaat

tuotteet = Tuotteet.tuotteet
print(tuotteet[0])

tilaus = {
    "asiakas_ID": 101,
    "tuote_ID:t": [101, 102], #kokoelma tuotteita, TV ja läppäri 
    # "hinta" :  #miten toteutetaan? Miten voi tarkistaa, että mikä tuote 101, tai 102? Mitkä oli niiden hinnat?
}
"""