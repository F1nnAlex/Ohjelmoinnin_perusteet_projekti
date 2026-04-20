import tkinter as tk 
import Functions
from tkinter import *
from tkinter import ttk, simpledialog # Nämä tarvitaan taulukkoon ja admin-ikkunaan
import Check_In_Out, Guest_Info, Guest_List

#laajennus napille checkin/out

def check_in_out_window():
    window1 = tk.Toplevel(root)
    window1.title("Hotel System")
    window1.geometry("500x600")
    window1.configure(bg="pink")

#tektboxit
    tk.Label(window1, text="----------------------------------", bg="pink").pack(pady=10)
    tk.Label(window1, text="Check In", font=("Arial", 12, "bold"), bg="pink").pack()

    tk.Label(window1, text="Name:", bg="pink").pack(pady=(10, 0))
    name_entry = tk.Entry(window1)
    name_entry.pack()

    tk.Label(window1, text="Phone:", bg="pink").pack(pady=(10, 0))
    phone_entry = tk.Entry(window1)
    phone_entry.pack()

    tk.Label(window1, text="Email:", bg="pink").pack(pady=(10, 0))
    email_entry = tk.Entry(window1)
    email_entry.pack()

    tk.Label(window1, text="Room Type:", bg="pink").pack(pady=(10, 0))
    room_type_entry = tk.Entry(window1)
    room_type_entry.pack()

    # Label to show success or error messages
    result_label = tk.Label(window1, text="", bg="pink", font=("Arial", 10, "bold"))

    def submit_check_in():
        # Get all the text from the entry boxes
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        room_type = room_type_entry.get()


        if name == "" or phone == "" or email == "" or room_type == "":
            # Show an error and stop the function right here using 'return'
            result_label.config(text="Error: All fields must be filled!", fg="red")
            return 
        
        #saves the customer's check in to our system
        result_message = Check_In_Out.check_in(name, phone, email, room_type)

        if "Success" in result_message:
            result_label.config(text=result_message,fg="green")

            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            room_type_entry.delete(0, tk.END)

        else:
            result_label.config(text=result_message, fg="red")

        


    #CHECK IN: The Submit Button

    submit_btn = tk.Button(window1, text="Submit Check-In", command=submit_check_in)
    submit_btn.pack(pady=20)

    result_label.pack(pady=5)

    #CHECK OUT: button 

    tk.Label(window1, text="----------------------------------", bg="pink").pack(pady=10)
    tk.Label(window1, text="Check Out", font=("Arial", 12, "bold"), bg="pink").pack()

    tk.Label(window1, text="Customer ID:", bg="pink").pack(pady=(5, 0))
    checkout_id_entry = tk.Entry(window1)
    checkout_id_entry.pack()

    checkout_result_label = tk.Label(window1, text="", bg="pink", font=("Arial", 10, "bold"))

    def submit_check_out():
        c_id = checkout_id_entry.get().strip()
        if c_id == "":
            checkout_result_label.config(text="Error: Enter ID!", fg="red")
            return

        # Kutsutaan Check_In_Out.py:n funktiota
        viesti = Check_In_Out.check_out(c_id)

        if "Successfully" in viesti:
            checkout_result_label.config(text=viesti, fg="green")
            checkout_id_entry.delete(0, tk.END) # Tyhjennetään laatikko
        else:
            checkout_result_label.config(text=viesti, fg="red")

    tk.Button(window1, text="Submit Check-Out", command=submit_check_out).pack(pady=20)
    checkout_result_label.pack()


#extension for guest info button  

def guest_info_window():
    window2 = tk.Toplevel(root)
    window2.title("Hotel System")
    window2.geometry("500x300")
    window2.configure(bg="pink")

#guest info extension window content

    tk.Label(window2, text="----------------------------------", bg="pink").pack(pady=1)
    tk.Label(window2, text="Guest Info", font=("Arial", 12, "bold"), bg="pink").pack()
    tk.Label(window2, text="----------------------------------", bg="pink").pack(pady=1)


    search_mode = tk.StringVar(value="Name")
    mode_frame = tk.Frame(window2, bg="pink")
    mode_frame.pack(pady=5)
    tk.Radiobutton(mode_frame, text="Name", variable=search_mode, value="Name", bg="pink").pack(side=LEFT, padx=10)
    tk.Radiobutton(mode_frame, text="ID", variable=search_mode, value="ID", bg="pink").pack(side=LEFT, padx=10)

    tk.Label(window2, text="Enter name or ID number:", bg="pink").pack(pady=(10, 0))
    search_entry = tk.Entry(window2, width=30)
    search_entry.pack(pady=5)

    result_display = tk.Label(window2, text="", bg="pink", justify=LEFT, font=("Arial", 10))
    
    def perform_search():
        term = search_entry.get().strip()
        if not term:
            result_display.config(text="Enter valid search!", fg="red")
            return
        
        # KUTSU NYT GUEST_INFO TIEDOSTOA:
        info = Guest_Info.get_guest_details(term, search_mode.get())
        
        if "Virhe" in info:
            result_display.config(text=info, fg="red")
        else:
            result_display.config(text=info, fg="black")

    tk.Button(window2, text="Hae tiedot", command=perform_search).pack(pady=15)
    result_display.pack(pady=10)



#extension for guest list button 

def guest_list_window():
    window3 = tk.Toplevel(root)
    window3.title("Hotel System")
    window3.geometry("850x500")
    window3.configure(bg="pink")

#guest list extension window content

    tk.Label(window3, text="----------------------------------", bg="pink").pack(pady=1)
    tk.Label(window3, text="Guest List", font=("Arial", 12, "bold"), bg="pink").pack()
    tk.Label(window3, text="----------------------------------", bg="pink").pack(pady=1)

    # --- Yläpalkki Admin-napille ---
    top_bar = tk.Frame(window3, bg="pink")
    top_bar.pack(fill=X, padx=10, pady=5)

    def open_admin_mode():
        # Kysytään salasanaa (WALLEYE)
        key = simpledialog.askstring("Admin Login", "Anna salauksen purkuavain:", parent=window3)
        if key == "WALLEYE":
            refresh_table(key)
        elif key is not None:
            status_label.config(text="Väärä avain!", fg="red")

    admin_btn = tk.Button(top_bar, text="Admin Login", command=open_admin_mode)
    admin_btn.pack(side=LEFT)

    tk.Label(window3, text="Kaikki aktiiviset vieraat", font=("Arial", 14, "bold"), bg="pink").pack(pady=5)
    
    # --- Taulukko (Treeview) ---
    columns = ("id", "name", "phone", "email", "type", "room")
    tree = ttk.Treeview(window3, columns=columns, show="headings")

    # Sarakkeiden nimet
    tree.heading("id", text="Asiakas ID")
    tree.heading("name", text="Nimi")
    tree.heading("phone", text="Puhelin")
    tree.heading("email", text="Sähköposti")
    tree.heading("type", text="Huonetyyppi")
    tree.heading("room", text="Huone #")

    # Sarakkeiden leveydet
    tree.column("id", width=100)
    tree.column("name", width=150)
    tree.column("phone", width=120)
    tree.column("email", width=200)
    tree.column("type", width=100)
    tree.column("room", width=70)

    tree.pack(expand=True, fill=BOTH, padx=20, pady=10)

    status_label = tk.Label(window3, text="Kirjaudu sisään nähdäksesi yhteystiedot", bg="pink", font=("Arial", 9))
    status_label.pack(pady=5)

    # --- Funktion taulukon päivittämiseen ---
    def refresh_table(key=None):
        # Tyhjennetään vanha sisältö
        for item in tree.get_children():
            tree.delete(item)
        
        # Haetaan uusi lista Guest_List tiedostosta
        vieraat = Guest_List.fetch_guest_list_data(key)
        
        for v in vieraat:
            tree.insert("", tk.END, values=v)
        
        if key:
            status_label.config(text="Admin-tila aktiivinen: Tiedot purettu", fg="green")

    # Täytetään taulukko ensimmäisen kerran (salattuna)
    refresh_table()


# GUI window:

root = tk.Tk()
root.title("Hotel System")
root.geometry("500x250")
root.configure(bg="pink")

title = tk.Label(root, text="Hotel System", font=("Arial", 18))
title.pack(pady=20)
title.configure(bg="pink")

btn1 = tk.Button(root, text= "Check In / Out", width=25, highlightbackground="pink", command=check_in_out_window)
btn1.pack (pady=10)

btn2 = tk.Button (root, text = "Guest info", width = 25, highlightbackground="pink", command=guest_info_window)
btn2.pack (pady=10)


btn3 = tk.Button(root, text= "Guest List", width=25, highlightbackground="pink", command=guest_list_window)
btn3.pack(pady=10)



Functions.setup_database()
root.mainloop()




