from tkinter import *
import sqlite3 as sql
from tkinter import ttk
from Customer import AddCustomerAccount as Add
from Customer import Manager as Mg
from Customer import CustomerAccount as ctmAcc
from tkinter import messagebox

def mainframeAcc(ID, parentForm):
    parentForm.withdraw()
    conn = sql.connect("Bank.db")
    
    def AddO():
        root.destroy()
        Add.AddAccount(ID, parentForm)
    
    def EditO():
        cusAcc = ctmAcc.CustomerAccount(Balance_field.get(),Date_field.get(), Type_field.get(),ID,employeechoosen.get())
        a = messagebox.askquestion("Question",message="Bạn có chắc chắn muốn sửa thông tin tài khoản "+ID_field.get()+" không?")
        if (ID_field.get() == ""):
            messagebox.showerror("Error","Bạn chưa chọn tài khoản muốn sửa thông tin!")
        else:
            if (Balance_field.get() == ""):
                messagebox.showerror("Error","Chưa nhập số tiền!")
            elif (Type_field.get() == ""):
                messagebox.showerror("Error","Chưa nhập loại tài khoảng!")
            else:
                if (a == 'yes'):
                    cusAcc.EditAccountCustomer(ID_field.get())
                    messagebox.showinfo("","Sửa thành công!")
                    Reload()
    
    def DeleteO():
        cusAcc = ctmAcc.CustomerAccount(Balance_field.get(),Date_field.get(), Type_field.get(),ID,employeechoosen.get())
        if (ID_field.get() == ""):
            messagebox.showerror("Error","Bạn chưa chọn tài khoản muốn xoá!")
        else:
            a = messagebox.askquestion("Question",message="Bạn có chắc chắn muốn xoá tài khoản "+ID_field.get()+" không?")
            if (a == 'yes'):
                cusAcc.DeleteAccountCustomer(ID_field.get())
                messagebox.showinfo("","Xoá thành công!")
                Reload()
       
    def Clear():
         ID_field.config(state="normal")
         ID_field.delete(0,END)
         Balance_field.delete(0,END)
         Date_field.config(state="normal")
         Date_field.delete(0,END)
         Type_field.delete(0,END)
         employeechoosen.current(0)
    
    def Quit():
        root.destroy()
        Mg.mainframe()
        
    
    def Reload():
        root.destroy()
        mainframeAcc(ID)
        
    def displaySelectedItem(a):
         ID_field.config(state="normal")
         ID_field.delete(0,END)
         Balance_field.delete(0,END)
         Date_field.config(state="normal")
         Date_field.delete(0,END)
         Type_field.delete(0,END)
         employeechoosen.delete(0,END)
         
         current_item = table.focus()
         ID = table.item(current_item)['values'][0]
         Balance = table.item(current_item)['values'][1]
         Date = table.item(current_item)['values'][2]
         Type = table.item(current_item)['values'][3]
         EmployeeID = table.item(current_item)['values'][4]
         
         ID_field.insert(0, ID)
         ID_field.config(state="disabled")
         Balance_field.insert(0, Balance)
         Date_field.insert(0, Date)
         Date_field.config(state="disabled")
         Type_field.insert(0, Type)
         employeechoosen.set(EmployeeID)
         
         
    
    def ShowO():
        for item in table.get_children():
            table.delete(item)
        c = conn.cursor()
        sql_show = """
        SELECT CustomerAccountID,Balance,AccountOpenDate,AccountType,EmployeeManageID
        FROM CustomerAccount
        WHERE CustomerID = '{0}'
        """.format(ID)
        c.execute(sql_show)
        rows = c.fetchall()
        for row in rows:
            data = []
            for i in row:
                data.append(i)
            table.insert( parent = '', index = 'end', values = data)
    
    root = Tk()
    root.minsize(height=500,width=800)
    def on_closing():
        parentForm.deiconify()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Title
    
    root.title("Quản lý tài khoản khách hàng")
    Label(root, text="Quản lý tài khoản khách hàng "+ID,fg='red',font=('cambria',20)).place(relwidth = .6, relheight = .07, relx =.1, rely =.01)
    
    #menu bar
    menubar = Menu(root)
    fileMenu = Menu(menubar,tearoff=0)
    fileMenu.add_command(label = "Reload",command=Reload)
    fileMenu.add_command(label = "Quit",command=Quit)
    fileMenu.add_separator()
    menubar.add_cascade(label="menu",menu = fileMenu)
    root.config(menu=menubar)
    
    #table
    table = ttk.Treeview(root, columns = ('AccountID','Balance','DateOpen','Type','EmployeeManageID'), show = 'headings')
    table.heading('AccountID', text='Account ID')
    table.heading('Balance', text='Balance')
    table.heading('DateOpen', text='Date Open')
    table.heading('Type', text='Type')
    table.heading('EmployeeManageID', text="EmployeeManagerID")
    
    table.column('AccountID',width =20,anchor=CENTER)
    table.column('Balance',width=20,anchor=CENTER)
    table.column('DateOpen',width=20,anchor=CENTER)
    table.column('Type',width=20,anchor=CENTER)
    table.column('EmployeeManageID',width=20,anchor=CENTER)

    
    scrolly = Scrollbar(table)
    scrolly.pack(side = RIGHT,fill=Y)
    
    
    table.bind("<<TreeviewSelect>>",displaySelectedItem)
    table.place(relwidth = .98,relheight= .55,relx=.01,rely=.08)
    ShowO()
    
    # label items
    Label(root, text="Customer Account ID: ").place(relwidth = .19, relheight = .06, relx =.01, rely =.65)
    
    Label(root, text="Balance: ").place(relwidth = .19, relheight = .06, relx =.01, rely =.72)
        
    Label(root, text="Account Open Date: ").place(relwidth = .19, relheight = .06, relx =.01, rely =.79)
        
    Label(root, text="Type: ").place(relwidth = .19, relheight = .06, relx =.01, rely =.86)
    
    Label(root, text="Employee Manage ID: ").place(relwidth = .19, relheight = .06, relx =.01, rely =.93)
    
    # entry items
    ID_field = Entry(root, font="Times 12")
    ID_field.place(relwidth = .4, relheight = .06, relx =.2, rely =.65)
    
    Balance_field = Entry(root,font="Times 12")
    Balance_field.place(relwidth = .4, relheight = .06, relx =.2, rely =.72)
        
    Date_field = Entry(root,font="Times 12")
    Date_field.place(relwidth = .4, relheight = .06, relx =.2, rely =.79)
        
    Type_field = Entry(root,font="Times 12")
    Type_field.place(relwidth = .4, relheight = .06, relx =.2, rely =.86)
    
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
    employeechoosen.place(relwidth = .4, relheight = .06, relx =.2, rely =.93)
    
    # Button
    Button(root,text="ADD",command=AddO).place(relwidth = .3, relheight = .06, relx =.65, rely =.65)
    Button(root,text="EDIT",command=EditO).place(relwidth = .3, relheight = .06, relx =.65, rely =.74)
    Button(root,text="DELETE",command=DeleteO).place(relwidth = .3,relheight = .06,relx = .65,rely = .83)
    Button(root,text="CLEAR",command=Clear).place(relwidth = .3, relheight = .06, relx= .65, rely=.92)
    
    root.mainloop()
