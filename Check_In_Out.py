import Functions

while True:
    print("\n========== HOTEL CUSTOMER MANAGEMENT ==========")
    print("1. Check in / assign guest to room")
    print("2. Check out guest")
    print("3. Exit")

    choice = input("Choose an option: ").strip() #Asks the user to choose an option from the main menu by entering a number corresponding to the desired action. The input is stripped of leading and trailing whitespace for cleaner processing.

    if choice == "1":
        Functions.assign_guest()
    elif choice == "2":
        Functions.checkout_guest()
    elif choice == "3":
        print("Exiting system.")
        break
    else:
        print("Invalid option. Please try again.")