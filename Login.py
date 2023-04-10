import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import os
from tkinter import messagebox
import sqlite3 as sql
from MainInterface import MainInterface as mGui


root = Tk()
path = "Bank.db"
conn = sql.connect(path)

c = conn.cursor()


#width and height

w = 450
h = 500
#---------- Background Color----------#
bgcolor = "white"

#---------- CENTER FORM ---------#
root.overrideredirect(1)
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws - w)/2
y = (hs - h)/2
root.geometry("%dx%d+%d+%d"%(w, h, x, y))
 
#---------- HEADER ---------#
headerframe = tk.Frame(root, bg="skyblue", width=w, height=60)
titleframe = tk.Frame(headerframe, bg='skyblue', padx=1, pady=1)
title_lable = tk.Label(titleframe, text="ĐĂNG NHẬP", padx=40, pady=5, bg='skyblue', font=('Segou UI', 24), fg='black', width=12)
close_button = tk.Button(headerframe, text="X", borderwidth=1, relief="solid", font=('Time New Roman', 16), bg='red', padx=3)

headerframe.pack()
titleframe.pack()
title_lable.pack()
close_button.pack()

titleframe.place(relx= 0.5, rely= 0.5, anchor=CENTER)
close_button.place(x=410, y= 7)

#close frame
def close_fr():
    root.destroy()

close_button['command'] = close_fr

#---------- END HEADER ---------#

mainframe = tk.Frame(root, width = w, height= h)

#---------- Login Page ---------#
loginframe = tk.Frame(mainframe, width = w, height= h)
login_contentframe = tk.Frame(loginframe, padx = 30, pady = 100,bg=bgcolor)

username_label = tk.Label(login_contentframe, text ="Username:  ", font=('Segou UI', 16), bg=bgcolor)
password_label = tk.Label(login_contentframe, text="Password:  ", font=('Segou UI', 16), bg=bgcolor)

username_entry = tk.Entry(login_contentframe, font=('Segou UI', 18), highlightbackground='black', highlightthickness=0.5)
password_entry = tk.Entry(login_contentframe, font=('Segou UI', 18), highlightbackground='black', highlightthickness=0.5)

login_button = tk.Button(login_contentframe, text="LOGIN", font=('bold', 18),bg='skyblue', padx= 10, pady=15, width=20, fg='white' )
login_button.place(relx= 0.5, rely= 0.5, anchor=CENTER)

go_signup_label = tk.Label(login_contentframe, text ="You don't have an root? Sign Up", font=('Segou UI', 16),bg=bgcolor, fg='darkgreen' )
go_signup_label.place(relx= 0.5, rely= 0.5, anchor=CENTER)

mainframe.pack(fill= 'both', expand=1)
loginframe.pack(fill= 'both', expand=1)
login_contentframe.pack(fill= 'both', expand=1)
username_label.grid(row = 0, column = 0, pady=10)
username_entry.grid(row = 0, column = 1)

password_label.grid(row = 1, column = 0, pady=10)
password_entry.grid(row = 1, column = 1)

login_button.grid(row = 3, column = 0, columnspan=2, pady=40)

go_signup_label.grid(row = 4, column = 0, columnspan=2, pady=20)

#-------------- Create funtion to allow the user login  ----------------------#
def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    # vals = (username, password,)
    select_query = "SELECT * FROM EmployeeAccount WHERE EmployeeaccountID = (?) and Password = (?)"
    c.execute(select_query, (username, password,))
    user = c.fetchone()
    print(user[0], user[3])
    
    mGui.MainInterface("TK01", "normal")
    conn.commit()


login_button['command'] = login

root.mainloop()
