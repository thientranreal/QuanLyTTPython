from tkinter import *
from tkinter import ttk
import sqlite3 as sql
from Customer import ManagerAcc as Acc
from Customer import CustomerAccount as ctmAcc
from tkinter import messagebox
from datetime import date

def AddAccount(ID, parentForm):
    conn = sql.connect("Bank.db")
    
    def Quit():
        root.destroy()
        Acc.mainframeAcc(ID, parentForm)
        
    def get_currentDay():
        today = date.today()
        return today.strftime("%d/%m/%Y")
    
    def AddO():
        cusAcc = ctmAcc.CustomerAccount(Balance_field.get(),get_currentDay(),Type_field.get(),ID,employeechoosen.get())
        if (Balance_field.get() ==""):
            messagebox.showerror("Error","Chưa nhập số tiền!")
        elif (Balance_field.get().isdigit() == False):
            messagebox.showerror("Error","Lỗi nhập số tiền!")
        elif (Type_field.get() == ""):
            messagebox.showerror("Error","Chưa nhập loại tài khoản!")
        else:
            cusAcc.AddAccountCustomer()
            messagebox.showinfo("","Thêm thành công!")
            root.destroy()
            Acc.mainframeAcc(ID)
    
    root = Tk()
    root.minsize(height=400,width=500)
    
    # label Title
    root.title("Thêm tài khoản khách hàng")
        
    Label(root, text="Thêm tài khoản khách hàng "+ID,fg='red',font=('cambria',20)).place(relwidth = .8, relheight = .08, relx =.1, rely =.05)
    
    # label items
    Label(root, text="Balance: ").place(relwidth = .3, relheight = .1, relx =.01, rely =.17)
        
    Label(root, text="Type: ").place(relwidth = .3, relheight = .1, relx =.01, rely =.33)
    
    Label(root, text="Employee Manager ID: ").place(relwidth = .3, relheight = .1, relx =.01, rely =.49)
    
    # Entry Items
    
    Balance_field = Entry(root,font="Times 12")
    Balance_field.place(relwidth = .6, relheight = .08, relx =.35, rely =.17)
        
    Type_field = Entry(root,font="Times 12")
    Type_field.place(relwidth = .6, relheight = .08, relx =.35, rely =.33)
    
    # combobox NV ID
    nEmployeeID = StringVar()
    employeechoosen = ttk.Combobox(root,textvariable= nEmployeeID,state='readonly')
    c = conn.cursor()
    sql_ID = """
        SELECT EmployeeID FROM Employee
    """
    c.execute(sql_ID)
    rows = c.fetchall()
    data = []
    for row in rows:
        for i in row:
            data.append(i)
    employeechoosen['values'] = (data)
    employeechoosen.current(0)
    employeechoosen.place(relwidth = .4, relheight = .08, relx =.35, rely =.49)
    
    # Button 
    Button(root,text="QUIT",command=Quit).place(relwidth = .35,relheight = .1,relx = .1, rely = .85)
    Button(root,text="ADD",command=AddO).place(relwidth = .35, relheight = .1, relx =.55, rely =.85)
        
    
    root.mainloop()