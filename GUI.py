import tkinter as tk 

from tkinter import *

#import Check_In_Out, Guest_Info, Guest_List


def check_in_out_window():
    window1 = tk.Toplevel(root)
    window1.title("Hotel System")
    window1.geometry("500x250")
    window1.configure(bg="pink")

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

btn1 = tk.Button(root, text="Check In / Out", width=25, highlightbackground="pink", command=check_in_out_window)
btn1.pack (pady=10)

btn2 = tk.Button (root, text = "Guest info", width = 25, highlightbackground="pink", command=guest_info_window)
btn2.pack (pady=10)


btn3 = tk.Button(root, text="Guest List", width=25, highlightbackground="pink", command=guest_list_window)
btn3.pack(pady=10)


root.mainloop()


