from Customer import customer as ctm
from tkinter import *
from tkinter import ttk
import sqlite3 as sql
from tkinter.filedialog import askopenfilename
from Customer import AddCustomer as Add
from tkinter import messagebox
from Customer import ManagerAcc as formAcc


def mainframe(EmployeeID, permission, parentForm):
    parentForm.withdraw()
    
    conn = sql.connect("Bank.db")
    
    def get_Sex():
        if (var.get() == 1):
            return "Nam"
        else :
            return "Nữ"
        
    def AddO():
        root.destroy()
        Add.Addframe(EmployeeID, permission, parentForm)
        
    def ShowO():
        for item in table.get_children():
            table.delete(item)
        if permission == "Admin":
            c = conn.cursor()
            sql_show = """
                SELECT * FROM Customer 
            """
            c.execute(sql_show)
            rows = c.fetchall()
            for row in rows:
                data = []
                for i in row:
                    data.append(i)
                table.insert( parent = '', index = 'end', values = data)
        else:
            c = conn.cursor()
            sql_show = """
                SELECT C.CustomerID,CustomerName,DateOfBirth,Address,Phone,Sex,SignatureFolder
                FROM Customer C JOIN CustomerAccount CA ON C.CustomerID = CA.CustomerID
                WHERE EmployeeManageID = '{0}'
            """.format(EmployeeID)
            c.execute(sql_show)
            rows = c.fetchall()
            for row in rows:
                data = []
                for i in row:
                    data.append(i)
                table.insert( parent = '', index = 'end', values = data)
            
    def check_Date():
        if (monthchoosen.get() == "02"):
            if (yearchoosen.get() == "1952" or yearchoosen.get() == "19556"
                or yearchoosen.get() == "19560" or yearchoosen.get() == "1964"
                or yearchoosen.get() == "1968" or yearchoosen.get() == "1972"
                or yearchoosen.get() == "1976" or yearchoosen.get() == "1980" 
                or yearchoosen.get() == "1984" or yearchoosen.get() == "1988"
                or yearchoosen.get() == "1992" or yearchoosen.get() == "1992"
                or yearchoosen.get() == "1996" or yearchoosen.get() == "2000"
                or yearchoosen.get() == "2004" or yearchoosen.get() == "2008"
                or yearchoosen.get() == "2012" or yearchoosen.get() == "2016"
                or yearchoosen.get() == "2020"):
                if (daychoosen.get() == "31" or daychoosen.get() == "30"):
                    return False
                else : return True
            else : 
                if (daychoosen.get() == "31" or daychoosen.get() == "30" or daychoosen.get() == "29"):
                    return False
                else :
                    return True
        elif (monthchoosen.get() == "04" or monthchoosen.get() == "06" or monthchoosen.get() == "09" or monthchoosen.get() == "11"):
            if (daychoosen.get() == "31"):
                return False
            else : return True
        else:
            return True
        
    def check_Phone():
        Phone = Phone_field.get()
        if len(Phone) != 10: 
            return False
        if (Phone[0] != '0'):
            return False
        if (Phone.isdigit() == False):
            return False
        return True
        
        
    def Quit():
        root.destroy()
        
    def Reload():
        root.destroy()
        mainframe()
    
    def EditO():
        Ngay = daychoosen.get()+"/"+monthchoosen.get()+"/"+yearchoosen.get()
        cus = ctm.Customer(Name_field.get(),Ngay,Address_field.get(),Phone_field.get(),get_Sex(),Signature_field.get())
        if (ID_field.get() == ""):
            messagebox.showerror("Error","Bạn chưa chọn thông tin người sửa!")
        else:
            if (Name_field.get() == ""):
                messagebox.showerror("Error","Không được để trống tên!")
            elif (Address_field.get() == ""):
                messagebox.showerror("Error","Không được để trống địa chỉ!")
            elif (Phone_field.get() == ""):
                messagebox.showerror("Error","Không được để trống số điện thoại!")
            elif (Signature_field.get() == ""):
                messagebox.showerror("Error","Chưa chọn địa chỉ ảnh")
            else:
                if (check_Date() == False):
                    messagebox.showerror("Error","Lỗi ngày tháng năm sinh!")
                elif (check_Phone() == False):
                    messagebox.showerror("Error","Lỗi số điện thoại!")
                else:
                    a = messagebox.askquestion("Question",message="Bạn có chắc chắn muốn sửa thông tin khách hàng"+ID_field.get()+" không?")
                    if (a == 'yes'):
                        cus.EditCustomer(ID_field.get())
                        messagebox.showinfo("","Sửa thành công!")
                        Reload()
            
    
    def DeleteO():
        Ngay = daychoosen.get()+"/"+monthchoosen.get()+"/"+yearchoosen.get()
        cus = ctm.Customer(Name_field.get(),Ngay, Address_field.get(), Phone_field.get(), get_Sex(), Signature_field.get())
        if (ID_field.get() == ""):
            messagebox.showerror("Error","Bạn chưa chọn thông tin người muốn xoá!")
        else:
            a = messagebox.askquestion("Question",message="Bạn có chắc chắn muốn xoá khách hàng "+ID_field.get()+" không?")
            if (a == 'yes'):
                cus.DeleteCustomer(ID_field.get())
                messagebox.showinfo("","Xoá thành công!")
                Reload()

    def CheckAcc(root):
        if (ID_field.get()==""):
            messagebox.showerror("Error","Bạn chưa chọn khách hàng bạn muốn xem thông tin tài khoản!")
        else:
            ID = ID_field.get()
            formAcc.mainframeAcc(ID, root)
    
    def Clear():
        ID_field.config(state="normal")
        ID_field.delete(0,END)
        Name_field.delete(0,END)
        daychoosen.current(0)
        monthchoosen.current(0)
        yearchoosen.current(0)
        Address_field.delete(0,END)
        Phone_field.delete(0,END)
        var.set(0)
        Signature_field.delete(0,END)
    
    def browsefunc(ent):
        filename = askopenfilename(filetypes=([
            ("image",".jpeg"),
            ("image","png"),
            ("image",".jpg"),
            ]))
        setTextEnt(ent, filename)
        
    def setTextEnt(ent, txt):
        ent.delete(0, 'end')
        ent.insert(0, txt)
    
    def displaySelectedItem(a):
        ID_field.config(state="normal")
        ID_field.delete(0,END)
        Name_field.delete(0,END)
        Address_field.delete(0,END)
        Phone_field.delete(0,END)
        var.set(0)
        Signature_field.delete(0,END)
        daychoosen.delete(0,END)
        monthchoosen.delete(0,END)
        yearchoosen.delete(0,END)
        
        current_item = table.focus()
        ID = table.item(current_item)['values'][0]
        Name = table.item(current_item)['values'][1]
        Date = table.item(current_item)['values'][2]
        Address = table.item(current_item)['values'][3]
        Phone = table.item(current_item)['values'][4]
        Sex = table.item(current_item)['values'][5]
        Signature = table.item(current_item)['values'][6]
        
        if (len(str(Phone)) == 9):
            Phone = '0' + str(Phone)
        
        listday = Date.split("/")
        
        ID_field.insert(0, ID)
        ID_field.config(state="disabled")
        Name_field.insert(0, Name)
        daychoosen.set(listday[0])
        monthchoosen.set(listday[1])
        yearchoosen.set(listday[2])
        Address_field.insert(0, Address)
        Phone_field.insert(0, Phone)
        if (Sex == "Nam"):
            var.set(1)
        else : var.set(2)
        Signature_field.insert(0, Signature)
        
        
    root = Tk()
    root.minsize(height = 500,width = 800)
    
    def on_closing():
        parentForm.deiconify()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    menubar = Menu(root)
    fileMenu = Menu(menubar,tearoff=0)
    fileMenu.add_command(label = "Reload",command=Reload)
    fileMenu.add_command(label = "Quit",command=Quit)
    fileMenu.add_separator()
    menubar.add_cascade(label="menu",menu = fileMenu)
    root.config(menu=menubar)
    
    root.title("Quản lý khách hàng")
    
    Label(root, text="Quản lý khách hàng",fg='red',font=('cambria',20)).place(relwidth = .5, relheight = .06, relx =.1, rely =.01)
    
    Button(root,text="ADD",command=AddO).place(relwidth = .3, relheight = .06, relx =.1, rely =.68)
    Button(root,text="EDIT",command=EditO).place(relwidth = .3, relheight = .06, relx =.1, rely =.79)
    Button(root,text="DELETE",command=DeleteO).place(relwidth = .3,relheight = .06,relx = .1,rely = .9)
    Button(root,text="CHECK ACCOUNT",command=lambda: CheckAcc(root)).place(relwidth = .3, relheight = .06, relx= .55, rely=.68)
    Button(root, text="CLEAR",command=Clear).place(relwidth = .3, relheight = .06, relx = .55, rely = .79)
    
    table = ttk.Treeview(root, columns = ('ID','Name','Birth','Address','Phone','Sex','Signature'), show = 'headings')
    table.heading('ID', text='ID')
    table.heading('Name', text='Name')
    table.heading('Birth', text='Birth')
    table.heading('Address', text='Address')
    table.heading('Phone', text='Phone')
    table.heading('Sex', text='Sex')
    table.heading('Signature', text = 'Signature')
    
    table.column('ID',width =45,stretch=NO)
    table.column('Name',minwidth = 50,width=150)
    table.column('Birth',width=75,stretch=NO)
    table.column('Address',minwidth=10,width=180)
    table.column('Phone',width=75,stretch=NO)
    table.column('Sex',width=40,stretch=NO)
    table.column('Signature',width=100)
    
    scrolly = Scrollbar(table)
    scrolly.pack(side = RIGHT,fill=Y)
    
    
    table.bind("<<TreeviewSelect>>",displaySelectedItem)
    table.place(relwidth = .98,relheight= .4,relx=.01,rely=.07)
    ShowO()
    
    # Label
    Label(root, text="Customer ID: ").place(relwidth = .12, relheight = .04, relx =.01, rely =.48)
    
    Label(root, text="Customer name: ").place(relwidth = .12, relheight = .04, relx =.01, rely =.53)
        
    Label(root, text="Date of birth: ").place(relwidth = .12, relheight = .04, relx =.01, rely =.58)
        
    Label(root, text="Address: ").place(relwidth = .12, relheight = .04, relx =.01, rely =.63)

    Label(root, text="Phone: ").place(relwidth = .12, relheight = .04, relx =.4, rely =.48)
        
    Label(root, text="Sex: ").place(relwidth = .12, relheight = .04, relx =.4, rely =.53)
        
    Label(root, text="Signature: ").place(relwidth = .12, relheight = .04, relx =.4, rely =.58)
        
    #Entry
    
    ID_field = Entry(root, font="Times 12")
    ID_field.place(relwidth = .25, relheight = .04, relx =.13, rely =.48)
    
    Name_field = Entry(root,font="Times 12")
    Name_field.place(relwidth = .25, relheight = .04, relx =.13, rely =.53)
    
    #Date_field = Entry(root,font="Times 12")
    #Date_field.place(relwidth = .25, relheight = .04, relx =.13, rely =.58)
        
    Address_field = Entry(root,font="Times 12")
    Address_field.place(relwidth = .5, relheight = .04, relx =.13, rely =.63)
        
    Phone_field = Entry(root,font="Times 12")
    Phone_field.place(relwidth = .4, relheight = .04, relx =.52, rely =.48)
        
    Signature_field = Entry(root,font="Times 12")
    Signature_field.place(relwidth = .36, relheight = .04, relx =.52, rely =.58)
    Button(root,text="...",command=lambda : browsefunc(ent=Signature_field)).place(relwidth = .03, relheight = .04, relx =.89, rely =.58)
        
    var = IntVar()
    R1 = Radiobutton(root, text="Nam",variable=var,value=1).place(relwidth = .1, relheight = .04, relx =.55, rely =.53)
    R2 = Radiobutton(root, text="Nữ",variable=var,value=2).place(relwidth = .1, relheight = .04, relx =.7, rely =.53)
    
    nday = StringVar()
    daychoosen = ttk.Combobox(root,textvariable = nday,state="readonly")
    daychoosen['values'] = ("01","02","03","04","05","06","07","08","09",10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
    daychoosen.place(relwidth = .07, relheight =.04, relx = .13, rely = .58)
    
    nmonth = StringVar()
    monthchoosen = ttk.Combobox(root,textvariable = nmonth,state="readonly")
    monthchoosen['values'] = ("01", "02","03","04","05","06","07","08","09","10","11","12")
    monthchoosen.place(relwidth = .07, relheight =.04, relx = .2, rely = .58)
        
    nyear = StringVar()
    yearchoosen = ttk.Combobox(root,textvariable = nyear,state="readonly")
    year = []
    for i in range(1950,2022):
        year.append(i)
    yearchoosen['values'] = (year)
    yearchoosen.place(relwidth = .1, relheight =.04, relx = .27, rely = .58)
    
    root.mainloop()