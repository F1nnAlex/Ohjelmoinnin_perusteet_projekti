import Functions

Functions.setup_database()
while True:
    print("\n========== HOTEL CUSTOMER MANAGEMENT ==========")
    print("1. List active guests")
    print("2. Exit")

    choice = input("Choose an option: ").strip() #Asks the user to choose an option from the main menu by entering a number corresponding to the desired action. The input is stripped of leading and trailing whitespace for cleaner processing.
    if choice == "1":
        Functions.list_active_guests()
    elif choice == "2":
        print("Exiting system.")
        break
    else:
        print("Invalid option. Please try again.") 