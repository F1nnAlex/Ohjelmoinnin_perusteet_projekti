import sqlite3
import random
from typing import Optional, List, Tuple #Importing necessary modules: sqlite3 for database operations, random for generating unique customer IDs, and typing for type annotations to improve code readability and maintainability.

DB_NAME = "customer_database.db" #Name of the SQLite database file where customer information will be stored. If the file does not exist, it will be created when the database connection is established.

ROOM_TYPES = {
    "budget": (1, 50),
    "comfort": (51, 99),
    "luxury": (100, 120),
}
#Cipher key for encrypting and decrypting private customer information

DECRYPTION_KEY = "WALLEYE" #Decryption key; "WALLEYE", used for accessing private customer data. IRL this is definetly not secure
MAX_ATTEMPTS = 3 #MAX 3 attempts before access is denied


#------------------------------------------------------------------------------
#Encryption and decryption functions
#------------------------------------------------------------------------------
def encryption_parameters(char: str, key_char: str) -> str: #Shift plaintext by key character using modular arithmetic
    return chr((ord(char) + ord(key_char)) % 65536)


def decryption_parameters(char: str, key_char: str) -> str: #Reverse shift ciphertext by key character using modular arithmetic
    return chr((ord(char) - ord(key_char)) % 65536)


def encrypt_plaintext(plain_text: str, key: str = DECRYPTION_KEY) -> str: #encrypt plaintext using a simple repeating-key cipher
    """Encrypt text using a simple repeating-key cipher."""
    if not plain_text:
        return ""

    encrypted_chars = []
    key_length = len(key)

    for i, char in enumerate(plain_text):
        key_char = key[i % key_length]
        encrypted_chars.append(encryption_parameters(char, key_char)) #Shift character by key character using modular arithmetic

    return "".join(encrypted_chars)


def decrypt_cipher(cipher_text: str, key: str) -> str:
    """Decrypt text using the provided key."""
    if not cipher_text:
        return ""

    decrypted_chars = []
    key_length = len(key)

    for i, char in enumerate(cipher_text):
        key_char = key[i % key_length]
        decrypted_chars.append(decryption_parameters(char, key_char))

    return "".join(decrypted_chars)


def verify_decryption_key() -> Optional[str]:
    """
    Ask for decryption key.
    Allows 3 attempts.
    Returns the correct key if successful, otherwise None.
    """
    for attempt in range(1, MAX_ATTEMPTS + 1):
        entered_key = input(f"Enter decryption key (attempt {attempt}/{MAX_ATTEMPTS}): ").strip()

        if entered_key == DECRYPTION_KEY:
            print("Access granted.")
            print("DECRYPTING...............")
            return entered_key

        print("Incorrect key.")

    print("Access denied. Maximum attempts reached.")
    return None


#------------------------------------------------------------------------------
# Database functions
#------------------------------------------------------------------------------
def get_connection(): #Function to establish a connection to the SQLite database, creating the database file if it doesn't exist
    return sqlite3.connect(DB_NAME) #Connect to the SQLite database specified by DB_NAME. Returns the connection to the code


def setup_database(): #Function to set up the database by creating the necessary tables for active guests and checkout history
    conn = get_connection()
    cursor = conn.cursor() #cursor object is used to execute SQL commands and queries on the database connection

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS active_guests (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone_encrypted TEXT NOT NULL,
            email_encrypted TEXT NOT NULL,
            room_type TEXT NOT NULL,
            room_number INTEGER NOT NULL UNIQUE
        )
    """)
#Execute SQL command to create the active_guests table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checkout_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT NOT NULL,
            name TEXT NOT NULL,
            room_number INTEGER NOT NULL,
            room_type TEXT NOT NULL
        )
    """)
#Execute SQL command to create the checkout_history table
    conn.commit()
    conn.close() #Commit the changes to the database and close the connection


def generate_unique_customer_id() -> str: #Function to generate a unique 8-digit customer ID by checking against both active guests and checkout history tables to ensure uniqueness
    """Generate a unique 8-digit customer ID."""
    conn = get_connection() #Establish a connection to the database
    cursor = conn.cursor() #Create a cursor object to execute SQL commands

    while True:
        customer_id = str(random.randint(10_000_000, 99_999_999)) #Generate a random 8-digit number as a string

        cursor.execute("SELECT 1 FROM active_guests WHERE customer_id = ?", (customer_id,)) #Check if the generated customer ID already exists in the active_guests table
        active_exists = cursor.fetchone() #Fetch the result of the query to check if the customer ID exists in active_guests

        cursor.execute("SELECT 1 FROM checkout_history WHERE customer_id = ?", (customer_id,)) #Check if the generated customer ID already exists in the checkout_history table
        history_exists = cursor.fetchone() #Fetch the result of the query to check if the customer ID exists in checkout_history

        if not active_exists and not history_exists: #If the customer ID does not exist in either table, it is unique and can be returned
            conn.close() #Close the database connection before returning the unique customer ID
            return customer_id


def get_available_rooms(room_type: str) -> List[int]: 
    """Return available room numbers for the selected room type."""
    start, end = ROOM_TYPES[room_type]

    conn = get_connection() #Establish a connection to the database
    cursor = conn.cursor() #Create a cursor object to execute SQL commands

    cursor.execute("SELECT room_number FROM active_guests") #Execute a SQL query to select all room numbers from the active_guests table
    occupied_rooms = {row[0] for row in cursor.fetchall()} #Fetch all results from the query and create a set of occupied room numbers for lookup

    conn.close()

    return [room for room in range(start, end + 1) if room not in occupied_rooms] #Return a list of available room numbers for the specified room type by checking against the set of occupied rooms


#------------------------------------------------------------------------------
# Hotel customer management functions
#------------------------------------------------------------------------------
def assign_guest(): #Function to handle the process of checking in a guest and assigning them to a room. It prompts the user for customer information, validates the input, checks for available rooms, encrypts private information, and stores the guest data in the active_guests table of the database.
    print("\n--- Check In / Assign Guest to Room ---")

    name = input("Enter customer name: ").strip() #Prompt the user to enter the customer's name, .strip removes any leading or trailing whitespace from the input
    if not name:
        print("Name cannot be empty.")
        return

    phone = input("Enter phone number: ").strip()
    if not phone:
        print("Phone number cannot be empty.")
        return

    email = input("Enter email: ").strip()
    if not email:
        print("Email cannot be empty.")
        return

    room_type = input("Enter room type (budget / comfort / luxury): ").strip().lower() #Asks the user for the desired room type, .strip().lower() converts the input to lowercase for case-insensitive comparison
    if room_type not in ROOM_TYPES:
        print("Invalid room type.")
        return

    available_rooms = get_available_rooms(room_type)
    if not available_rooms:
        print(f"No available {room_type} rooms.")
        return

    room_number = available_rooms[0]
    customer_id = generate_unique_customer_id() #Generate a unique customer ID for the new guest

    encrypted_phone = encrypt_plaintext(phone) 
    encrypted_email = encrypt_plaintext(email) #Encrypts the customers phone number and email using the encrypt_plaintext function before storing it in the database

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO active_guests (customer_id, name, phone_encrypted, email_encrypted, room_type, room_number)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer_id, name, encrypted_phone, encrypted_email, room_type, room_number)) #Execute a SQL command to insert the new guest's information into the active_guests table
 #Parameterized query is used to prevent SQL injection
    conn.commit() #Commit the changes to the database to save the new guest's information
    conn.close()

    print("\nGuest checked in successfully.")
    print(f"Assigned room number: {room_number}")
    print(f"Customer ID: {customer_id}") #Prints the new customers assigned room number and unique customer ID


def find_active_guest_by_id(customer_id: str) -> Optional[Tuple]: #Function to find an active customer using their assigned ID
    conn = get_connection() #Establish connection to the database
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_id, name, phone_encrypted, email_encrypted, room_type, room_number
        FROM active_guests
        WHERE customer_id = ?
    """, (customer_id,)) #Execute a SQL query to select the customer's information from the active_guests table based on the customer ID. The query uses a parameterized statement to prevent SQL injection.
    guest = cursor.fetchone() #Fetch the result of the query

    conn.close()
    return guest #Return the guest's information as a tuple if found, otherwise return None


def find_active_guests_by_name(name: str) -> List[Tuple]: #Same as above, but searches for active customers by the name instead of the ID.
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_id, name, phone_encrypted, email_encrypted, room_type, room_number
        FROM active_guests
        WHERE LOWER(name) = LOWER(?)
    """, (name,)) #Executes a SQL query similar to the above function. LOWER() function is used to invalid case sensitivity.
    guests = cursor.fetchall()

    conn.close() #Closes the connection
    return guests #Returns the fetched list


def display_active_guest(guest: Tuple): #Function to display the information of an active guest. Private information is encrypted and requires a decryption key.
    customer_id, name, phone_encrypted, email_encrypted, room_type, room_number = guest

    # Show non-private info without decryption key
    print("\n--- Customer Found ---")
    print(f"Customer ID : {customer_id}")
    print(f"Name        : {name}")
    print(f"Room Type   : {room_type}")
    print(f"Room Number : {room_number}")
    print("To view full customer info, decryption is required.")

    entered_key = input("Enter decryption key to view private data: ").strip()

    entered_key = verify_decryption_key()
    if entered_key is None:
        return

    decrypted_phone = decrypt_cipher(phone_encrypted, entered_key) #Decrypts the customers phone number and email using the decrypt_cipher function
    decrypted_email = decrypt_cipher(email_encrypted, entered_key)

    print("\n--- Full Active Customer Details ---")
    print(f"Customer ID : {customer_id}")
    print(f"Name        : {name}")
    print(f"Phone       : {decrypted_phone}")
    print(f"Email       : {decrypted_email}")
    print(f"Room Type   : {room_type}")
    print(f"Room Number : {room_number}") #Lists the customers full information after successful decryption.


def view_history_by_name(name: str): #Function to view the historical record of a customer by their name. It searches the checkout_history table for records matching the provided name and displays the relevant information while indicating that private information has been deleted after checkout.
    conn = get_connection() #Establish a connection to the database
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_id, name, room_number, room_type
        FROM checkout_history
        WHERE LOWER(name) = LOWER(?)
    """, (name,))
    rows = cursor.fetchall() #Fetches all the records from the checkout_history table that matches the provided name. LOWER() function invalidates case sensitivity

    conn.close() #Closes the connection to the database

    if not rows:
        print("No active or historical customer found with that name.")
        return #If no records are found with the provided name, it prints a message and returns from the function

    if len(rows) > 1:
        print("\nMultiple historical customers found with that name.") #If multiple records are found with the provided name, it prints a message and lists the matching customers with their names and customer IDs for further identification
        for row in rows:
            print(f"Name: {row[1]}, Customer ID: {row[0]}")
        return

    row = rows[0]
    print("\n--- Historical Customer Record ---") #If exactly one record is found, it displays the historical customer record with the customer ID, name, room number, and room type. It also indicates that private information has been deleted after checkout.
    print(f"Customer ID : {row[0]}")
    print(f"Name        : {row[1]}")
    print(f"Room Number : {row[2]}")
    print(f"Room Type   : {row[3]}")
    print("Private information has been deleted after checkout.")


def view_history_by_id(customer_id: str): #Same as the above function, but searches the database using the unique customer ID instead of the name.
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_id, name, room_number, room_type
        FROM checkout_history
        WHERE customer_id = ?
    """, (customer_id,))
    row = cursor.fetchone() #Fetches the record from the checkout_history table that matches the customer ID.
#The query uses a parameterized statement to prevent SQL injection. 
    conn.close()

    if not row:
        print("No active or historical customer found with that ID.") #If no record is found with the provided ID, it prints a message and returns from the function
        return

    print("\n--- Historical Customer Record ---") #If a record is found, it displays the historical customer record with the customer ID, name, room number, and room type.
    print(f"Customer ID : {row[0]}")
    print(f"Name        : {row[1]}")
    print(f"Room Number : {row[2]}")
    print(f"Room Type   : {row[3]}")
    print("Private information has been deleted after checkout.") #Private information has been deleted after checkout


def view_customer(): #Function to view an active customer's information, either using thei name or their assigned customer ID.
    print("\n--- View Customer ---")
    search_choice = input("Search by (1) Name or (2) Unique ID: ").strip() #Prompts the user to choose to either search by a name or by assigned customer ID.

    guest = None #Initialize a variable to hold the guest information that will be retrieved based on the user's search choice. It starts as None and will be assigned the guest's information if a matching record is found in the database.

    if search_choice == "1":
        name = input("Enter customer name: ").strip()
        matches = find_active_guests_by_name(name) #Calls the find_active_guests_by_name function to search for active guests matching the provided name. The function returns a list of matching guests, which is stored in the matches variable.

        if not matches:
            view_history_by_name(name)
            return

        if len(matches) == 1:
            guest = matches[0]
        else:
            print("\nMultiple active customers found with that name.")
            print("Matching customers:")
            for match in matches:
                print(f"Name: {match[1]} | Customer ID: {match[0]}")

            entered_id = input("Please enter the unique customer ID: ").strip() #If multiple active customers are found with the provided name, it prompts the user to enter the unique customer ID to identify the specific customer they want to view. The entered ID is then used to find the corresponding guest information from the list of matches.
            guest = next((g for g in matches if g[0] == entered_id), None) #Searches through the list of matching guests to find the one with the entered customer ID. If a match is found, it assigns the guest's information to the guest variable; otherwise, it remains None.

            if guest is None:
                print("No matching active customer found with that ID.") #If no match is found, it prints a message indicating that no matching active customer was found with the entered ID and returns from the function.
                return

    elif search_choice == "2": #If the user chooses to search by unique ID, it prompts them to enter the customer ID and calls the find_active_guest_by_id function to retrieve the guest information based on the provided ID. If no active guest is found with that ID, it calls the view_history_by_id function to check if there is a historical record of a customer with that ID.
        customer_id = input("Enter unique customer ID: ").strip()
        guest = find_active_guest_by_id(customer_id) #Calls the find_active_guest_by_id function to search for an active guest matching the provided customer ID. The function returns the guest's information as a tuple if found, or None if no active guest is found with that ID.

        if guest is None:
            view_history_by_id(customer_id) #If no active guest is found with the provided customer ID, it calls the view_history_by_id function to check if there is a historical record of a customer with that ID. 
            return
    else:
        print("Invalid option.")
        return

    display_active_guest(guest) #If a guest is found, calls the display_active_guest function to show the guest's information.


def checkout_guest(): #Function to handle the process of checking out a guest. It prompts the user for the customer's unique ID, verifies if the guest is currently active, moves their information to the checkout_history table, and deletes their record from the active_guests table while retaining a historical record of their stay.
    print("\n--- Check Out Guest ---")
    customer_id = input("Enter the unique customer ID for checkout: ").strip() #Asks the user to enter the unique customer ID of the guest that is checking out. This ID is used to identify the specific guest in the database for the checkout process.

    guest = find_active_guest_by_id(customer_id) #Calls the find_active_guest_by_id function to search for an active guest matching the provided customer ID. The function returns the guest's information as a tuple if found, or None if no active guest is found with that ID.
    if guest is None:
        print("No active guest found with that ID.")
        return

    customer_id, name, _, _, room_type, room_number = guest

    conn = get_connection() #Establish a connection to the database
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO checkout_history (customer_id, name, room_number, room_type)
        VALUES (?, ?, ?, ?)
    """, (customer_id, name, room_number, room_type)) #Execute a SQL command to insert the guest's information into the checkout_history table. The private information (phone and email) is not included in the checkout history to ensure that it is deleted after checkout, while still retaining a historical record of the customer's stay with their ID, name, room number, and room type.

    cursor.execute("DELETE FROM active_guests WHERE customer_id = ?", (customer_id,)) #Execute a SQL command to delete the guests record from the active_guests table based on the customer ID, effectively checking them out of the hotel.

    conn.commit() #Commit the changes to the database to save the checkout history and remove the guest from the active_guests table
    conn.close() #Close the connection to the database

    print(f"Guest '{name}' with Customer ID {customer_id} has been checked out.") #Prints a message confirming that the guest has been checked out, including their name and customer ID for reference.
    print("Private information deleted. Historical record retained.") #Confirms that the guest's private information has been deleted from the active_guests table.


def list_active_guests(): #Function to list all currently active guests in the hotel. It retrieves the guest information from the active_guests table and displays it in a readable format, showing the customer ID, name, room type, and room number for each active guest.
    conn = get_connection() #Establish a connection to the database
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_id, name, room_type, room_number
        FROM active_guests
        ORDER BY room_number
    """)
    rows = cursor.fetchall() #Fetches all records from the active_guests table

    conn.close() #Closes the connection to the database

    print("\n--- Active Guests ---")
    if not rows:
        print("No active guests.") #If no active guests are found in the database, it prints a message indicating that there are no active guests and
        return

    for row in rows:
        print(
            f"Customer ID: {row[0]} | Name: {row[1]} | Room Type: {row[2]} | Room Number: {row[3]}" #Prints the customer ID, name, room type, and room number for each active guest in a formatted string for easy reading.
        )


def main_menu(): #Function to display the main menu of the hotel customer management system
    setup_database()

    while True:
        print("\n========== HOTEL CUSTOMER MANAGEMENT ==========")
        print("1. Check in / assign guest to room")
        print("2. Check out guest")
        print("3. View customer")
        print("4. List active guests")
        print("5. Exit")

        choice = input("Choose an option: ").strip() #Asks the user to choose an option from the main menu by entering a number corresponding to the desired action. The input is stripped of leading and trailing whitespace for cleaner processing.

        if choice == "1":
            assign_guest()
        elif choice == "2":
            checkout_guest()
        elif choice == "3":
            view_customer()
        elif choice == "4":
            list_active_guests()
        elif choice == "5":
            print("Exiting system.")
            break
        else:
            print("Invalid option. Please try again.") 


if __name__ == "__main__":
    main_menu() #This line checks if the script is being run directly (as the main program) and if so, it calls the main_menu function to start the hotel customer management system.
