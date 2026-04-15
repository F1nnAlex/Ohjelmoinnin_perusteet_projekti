import tkinter as tk 

from tkinter import *

import Check_In_Out#, Guest_Info, Guest_List

#laajennus napille checkin/out

def check_in_out_window():
    window1 = tk.Toplevel(root)
    window1.title("Hotel System")
    window1.geometry("500x350")
    window1.configure(bg="pink")

#tektboxit

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
        result = Check_In_Out.check_in(name,phone, email, room_type)

        result_label.config(text= result, fg="green")



#clear boxes
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    room_type_entry.delete(0, tk.END)

    # --- 3. The Submit Button ---

    submit_btn = tk.Button(window1, text="Submit Check-In", command=submit_check_in)
    submit_btn.pack(pady=20)

    result_label.pack(pady=5)


#laajennus napille guest info  

def guest_info_window():
    window2 = tk.Toplevel(root)
    window2.title("Hotel System")
    window2.geometry("500x250")
    window2.configure(bg="pink")

def guest_list_window():
    window3 = tk.Toplevel(root)
    window3.title("Hotel System")
    window3.geometry("500x250")
    window3.configure(bg="pink")


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




root.mainloop()




