import Funtions

while True:
    print("\n========== HOTEL CUSTOMER MANAGEMENT ==========")
    print("1. Check in / assign guest to room")
    print("2. Check out guest")
    print("3. View customer")
    print("4. List active guests")
    print("5. Exit")

    choice = input("Choose an option: ").strip() #Asks the user to choose an option from the main menu by entering a number corresponding to the desired action. The input is stripped of leading and trailing whitespace for cleaner processing.

    if choice == "1":
        Funtions.assign_guest()
    elif choice == "2":
        Funtions.checkout_guest()
    elif choice == "3":
        Funtions.view_customer()
    elif choice == "4":
        Funtions.list_active_guests()
    elif choice == "5":
        print("Exiting system.")
        break
    else:
        print("Invalid option. Please try again.") 


if __name__ == "__main__":
    Funtions.main_menu() #This line checks if the script is being run directly (as the main program) and if so, it calls the main_menu function to start the hotel customer management system.