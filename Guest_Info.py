import Functions

def get_guest_details(search_term, mode):
    if mode == "ID":
        guest = Functions.find_active_guest_by_id(search_term)
        if guest:
            # guest-tuplen rakenne: (id, name, phone, email, type, room)
            return f"--- Customer found ---\n\nID: {guest[0]}\nName: {guest[1]}\nRoom type: {guest[4]}\nRoom number: {guest[5]}"
        else:
            return "Error: ID-number doesn't come back to active guests!"
            
    elif mode == "Name":
        guests = Functions.find_active_guests_by_name(search_term)
        if not guests:
            return "Error: Given name doesn't come back to active guests!"
        
        res = f"--- Found guests ({len(guests)}) ---\n\n"
        for g in guests:
            res += f"Nimi: {g[1]} | ID: {g[0]} | Huone: {g[5]}\n"
        return res

# Vanha tekstipohjainen valikko säilytetään, mutta se ajetaan vain suoraan käynnistettäessä
if __name__ == "__main__":
    Functions.setup_database()
    while True:
        print("\n========== HOTEL CUSTOMER MANAGEMENT ==========")
        print("1. View customer")
        print("2. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            Functions.view_customer()
        elif choice == "2":
            break