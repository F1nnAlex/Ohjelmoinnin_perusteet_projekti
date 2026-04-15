import tkinter as tk 

from tkinter import *

#import Check_In_Out, Guest_Info, Guest_List





# GUI window:

root = tk.Tk()
root.title("Hotel System")
root.geometry("500x250")
root.configure(bg="pink")

title = tk.Label(root, text="Hotel System", font=("Arial", 18))
title.pack(pady=20)
title.configure(bg="pink")

btn1 = tk.Button(root, text="Check In / Out", width=25) #command=Check_In_Out)
btn1.pack (pady=10)

btn2 = tk.Button (root, text = "Guest info", width = 25) #command=Guest_Info)
btn2.pack (pady=10)


btn3 = tk.Button(root, text="Guest List", width=25) #command=Guest_List)
btn3.pack(pady=10)

root.mainloop()


