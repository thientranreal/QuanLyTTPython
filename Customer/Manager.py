from Customer import customer as ctm
from tkinter import *
from tkinter import ttk
import sqlite3 as sql
from tkinter import messagebox
from Customer import ManagerAcc as formAcc
from unidecode import unidecode

def mainframe(EmployeeID, permission, parentForm):
    parentForm.withdraw()
    
        
    def AddO():
        if (ID_field.get() != ""):
            messagebox.showerror("Error","Phải để trống ID khi thêm! Vui lòng nhấn CLEAR.")
        else:
            Ngay = daychoosen.get()+"/"+monthchoosen.get()+"/"+yearchoosen.get()
            if (permission == 'admin'):
                cus = ctm.Customer(Name_field.get(),Ngay,Address_field.get(),Phone_field.get(),Sexchoosen.get(),employeechoosen.get())
                if (Name_field.get() == ""):
                    messagebox.showerror("Error","Không được để trống tên!")
                elif (Address_field.get() == ""):
                    messagebox.showerror("Error","Không được để trống địa chỉ!")
                elif (Phone_field.get() == ""):
                    messagebox.showerror("Error","Không được để trống số điện thoại!")
                elif (Sexchoosen.get() == ""):
                    messagebox.showerror("Error","Chưa chọn giới tính!")
                elif (daychoosen.get() == "" or monthchoosen.get() == "" or yearchoosen.get() == ""):
                    messagebox.showerror("Error","Chưa chọn ngày tháng năm sinh!")
                elif (employeechoosen.get() == ""):
                    messagebox.showerror("Error","Chưa chọn tài khoản nhân viên quản lý!")
                else:
                    if (check_Date() == False):
                        messagebox.showerror("Error","Lỗi ngày tháng năm sinh!")
                    elif (check_Phone() == False):
                        messagebox.showerror("Error","Lỗi số điện thoại!")
                    else:
                        a = messagebox.askquestion("Question",message="Bạn có chắc chắn muốn thêm khách hàng không?")
                        if (a == 'yes'):
                            cus.AddCustomer()
                            Reload()
            else:
                cus = ctm.Customer(Name_field.get(),Ngay,Address_field.get(),Phone_field.get(),Sexchoosen.get(),EmployeeID)
                if (Name_field.get() == ""):
                    messagebox.showerror("Error","Không được để trống tên!")
                elif (Address_field.get() == ""):
                    messagebox.showerror("Error","Không được để trống địa chỉ!")
                elif (Phone_field.get() == ""):
                    messagebox.showerror("Error","Không được để trống số điện thoại!")
                elif (Sexchoosen.get() == ""):
                    messagebox.showerror("Error","Chưa chọn giới tính!")
                elif (daychoosen.get() == "" or monthchoosen.get() == "" or yearchoosen.get() == ""):
                    messagebox.showerror("Error","Chưa chọn ngày tháng năm sinh!")
                else:
                    if (check_Date() == False):
                        messagebox.showerror("Error","Lỗi ngày tháng năm sinh!")
                    elif (check_Phone() == False):
                        messagebox.showerror("Error","Lỗi số điện thoại!")
                    else:
                        a = messagebox.askquestion("Question",message="Bạn có chắc chắn muốn thêm khách hàng không?")
                        if (a == 'yes'):
                            cus.AddCustomer()
                            Reload()
        
    def ShowO():
        for item in table.get_children():
            table.delete(item)
        if permission == "admin":
            conn = sql.connect("Bank.db")
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
            conn.close()
        else:
            conn = sql.connect("Bank.db")
            c = conn.cursor()
            sql_show = """
                SELECT *
                FROM Customer
                WHERE EmployeeManageID = '{0}'
            """.format(EmployeeID)
            c.execute(sql_show)
            rows = c.fetchall()
            for row in rows:
                data = []
                for i in row:
                    data.append(i)
                table.insert( parent = '', index = 'end', values = data)
            conn.close()
            
    def check_Date():
        year_check = int(yearchoosen.get())
        if (monthchoosen.get() == "02"):
            if ((year_check%400 == 0) or ((year_check%4 == 0) and (year_check%100 == 0))):
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
        parentForm.deiconify()
        root.destroy()
        
    def Reload():
        root.destroy()
        mainframe(EmployeeID,permission,parentForm)
    
    def EditO():
        Ngay = daychoosen.get()+"/"+monthchoosen.get()+"/"+yearchoosen.get()
        if permission == 'admin':
            cus = ctm.Customer(Name_field.get(),Ngay,Address_field.get(),Phone_field.get(),Sexchoosen.get(),employeechoosen.get())
            if (ID_field.get() == ""):
                messagebox.showerror("Error","Bạn chưa chọn thông tin người sửa!")
            else:
                if (Name_field.get() == ""):
                    messagebox.showerror("Error","Không được để trống tên!")
                elif (Address_field.get() == ""):
                    messagebox.showerror("Error","Không được để trống địa chỉ!")
                elif (Phone_field.get() == ""):
                    messagebox.showerror("Error","Không được để trống số điện thoại!")
                elif (daychoosen.get() == "" or monthchoosen.get() == "" or yearchoosen.get() == ""):
                    messagebox.showerror("Error","Chưa chọn ngày tháng năm sinh!")
                elif (employeechoosen.get() == ""):
                    messagebox.showerror("Error","Chưa chọn tài khoản nhân viên quản lý!")
                else:
                    if (check_Date() == False):
                        messagebox.showerror("Error","Lỗi ngày tháng năm sinh!")
                    elif (check_Phone() == False):
                        messagebox.showerror("Error","Lỗi số điện thoại!")
                    else:
                        a = messagebox.askquestion("Question",message="Bạn có chắc chắn muốn sửa thông tin khách hàng"+ID_field.get()+" không?")
                        if (a == 'yes'):
                            cus.EditCustomer(ID_field.get())
                            Reload()
        else:
            cus = ctm.Customer(Name_field.get(),Ngay,Address_field.get(),Phone_field.get(),Sexchoosen.get(),EmployeeID)
            if (ID_field.get() == ""):
                messagebox.showerror("Error","Bạn chưa chọn thông tin người sửa!")
            else:
                if (Name_field.get() == ""):
                    messagebox.showerror("Error","Không được để trống tên!")
                elif (Address_field.get() == ""):
                    messagebox.showerror("Error","Không được để trống địa chỉ!")
                elif (Phone_field.get() == ""):
                    messagebox.showerror("Error","Không được để trống số điện thoại!")
                elif (daychoosen.get() == "" or monthchoosen.get() == "" or yearchoosen.get() == ""):
                    messagebox.showerror("Error","Chưa chọn ngày tháng năm sinh!")
                else:
                    if (check_Date() == False):
                        messagebox.showerror("Error","Lỗi ngày tháng năm sinh!")
                    elif (check_Phone() == False):
                        messagebox.showerror("Error","Lỗi số điện thoại!")
                    else:
                        a = messagebox.askquestion("Question",message="Bạn có chắc chắn muốn sửa thông tin khách hàng"+ID_field.get()+" không?")
                        if (a == 'yes'):
                            cus.EditCustomer(ID_field.get())
                            Reload()
            
    
    def DeleteO():
        Ngay = daychoosen.get()+"/"+monthchoosen.get()+"/"+yearchoosen.get()
        cus = ctm.Customer(Name_field.get(),Ngay, Address_field.get(), Phone_field.get(),Sexchoosen.get(),"Delete")
        if (ID_field.get() == ""):
            messagebox.showerror("Error","Bạn chưa chọn thông tin người muốn xoá!")
        else:
            a = messagebox.askquestion("Question",message="Bạn có chắc chắn muốn xoá khách hàng "+ID_field.get()+" không?")
            if (a == 'yes'):
                cus.DeleteCustomer(ID_field.get())
                Reload()

    def CheckAcc():
        if (ID_field.get()==""):
            messagebox.showerror("Error","Bạn chưa chọn khách hàng bạn muốn xem thông tin tài khoản!")
        else:
            ID = ID_field.get()
            if (permission=="admin"):
                formAcc.mainframeAcc(ID,permission, root)
            else:
                formAcc.mainframeAcc(ID,permission, root)
    
    def Clear():
        Search_Field.delete(0,END)
        ID_field.config(state="normal")
        ID_field.delete(0,END)
        ID_field.config(state="readonly")
        Name_field.delete(0,END)
        daychoosen.set("")
        monthchoosen.set("")
        yearchoosen.set("")
        Address_field.delete(0,END)
        Phone_field.delete(0,END)
        Sexchoosen.set("")
        Signature_field.config(state="normal")
        Signature_field.delete(0,END)
        Signature_field.config(state="readonly")
        if permission == 'admin':
            employeechoosen.set("")
            
    def Search():
        if (Search_Field.get() == ""):
            for item in table.get_children():
                table.delete(item)
            ShowO()
        else:
            string_search = str(Search_Field.get())
            if permission == "admin":
                conn = sql.connect("Bank.db")
                c = conn.cursor()
                sql_name = """
                    SELECT CustomerName FROM Customer 
                """
                c.execute(sql_name)
                rows = c.fetchall()
                data = []
                for row in rows:
                    data.append(row[0])
                conn.close()
                search_data = []
                for i in data:
                    try:
                        name = str(i)
                        i = str(i).lower()
                        i = unidecode(str(i))
                        string_search = string_search.lower()
                        string_search = unidecode(string_search)
                        if (str(i).index(string_search) >= 0 ):
                            search_data.append(name)
                    except:
                        pass
                if (not search_data):
                    messagebox.showerror("Error","Không tìm thấy tên!")
                else:
                    for item in table.get_children():
                        table.delete(item)
                    for name in search_data:
                        search_rows = []
                        conn = sql.connect("Bank.db")
                        c = conn.cursor()
                        sql_show = """
                            SELECT *
                            FROM Customer
                            WHERE CustomerName = '{0}'
                        """.format(name)
                        c.execute(sql_show)
                        search_rows = c.fetchall()
                        for row in search_rows:
                            data_find = row 
                        table.insert( parent = '', index = 'end', values = data_find)
                        conn.close()
            else:
                conn = sql.connect("Bank.db")
                c = conn.cursor()
                sql_name = """
                    SELECT CustomerName
                    FROM Customer
                    WHERE EmployeeManageID = '{0}'
                """.format(EmployeeID)
                c.execute(sql_name) # sql_show
                rows = c.fetchall()
                data = []
                for row in rows:
                    data.append(row[0])
                conn.close()
                search_data = []
                for i in data:
                    try:
                        name = str(i)
                        i = str(i).lower()
                        i = unidecode(str(i))
                        string_search = string_search.lower()
                        string_search = unidecode(string_search)
                        if (str(i).index(string_search) >= 0 ):
                            search_data.append(name)
                    except:
                        pass
                if (not search_data):
                    messagebox.showerror("Error","Không tìm thấy tên!")
                else:
                    for item in table.get_children():
                        table.delete(item)
                    for name in search_data:
                        search_rows = []
                        conn = sql.connect("Bank.db")
                        c = conn.cursor()
                        sql_show = """
                            SELECT *
                            FROM Customer
                            WHERE CustomerName = '{0}'
                        """.format(name)
                        c.execute(sql_show)
                        search_rows = c.fetchall()
                        for row in search_rows:
                            data_find = row 
                        table.insert( parent = '', index = 'end', values = data_find)
                        conn.close()
                        
        
    
    def displaySelectedItem(a):
        ID_field.config(state="normal")
        ID_field.delete(0,END)
        Name_field.delete(0,END)
        Address_field.delete(0,END)
        Phone_field.delete(0,END)
        Signature_field.config(state="normal")
        Signature_field.delete(0,END)
        
        current_item = table.focus()
        ID = table.item(current_item)['values'][0]
        Name = table.item(current_item)['values'][1]
        Date = table.item(current_item)['values'][2]
        Address = table.item(current_item)['values'][3]
        Phone = table.item(current_item)['values'][4]
        Sex = table.item(current_item)['values'][5]
        Signature = table.item(current_item)['values'][6]
        EmployeeAccountID = table.item(current_item)['values'][7]
        
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
        Sexchoosen.set(Sex)
        Signature_field.insert(0, Signature)
        Signature_field.config(state="readonly")
        if permission == 'admin':
            employeechoosen.set(EmployeeAccountID)
        
    def on_closing():
        parentForm.deiconify()
        root.destroy()
        
        
    root = Tk()
    root.minsize(height = 500,width = 800)
    

    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    menubar = Menu(root)
    fileMenu = Menu(menubar,tearoff=0)
    fileMenu.add_command(label = "Reload",command=Reload)
    fileMenu.add_command(label = "Quit",command=Quit)
    fileMenu.add_separator()
    menubar.add_cascade(label="menu",menu = fileMenu)
    root.config(menu=menubar)
    
    root.title("Quản lý khách hàng")
    
    Label(root, text="Quản lý khách hàng",fg='red',font=('cambria',20)).place(relwidth = .5, relheight = .06, relx =.1, rely =.0)
    
    # thanh tìm kiếm
    Label(root,text="Tìm kiếm theo tên: ").place(relwidth = .2, relheight = .04, relx =.1, rely =.07)
    
    Search_Field = Entry(root, font="Times 12")
    Search_Field.place(relwidth = .4, relheight = .04, relx =.3, rely =.07)
    
    Button(root,text="SEARCH",command=Search).place(relwidth = .1, relheight = .04, relx =.71, rely =.07)
    
    # Button chức năng
    Button(root,text="ADD",command=AddO).place(relwidth = .3, relheight = .06, relx =.1, rely =.68)
    Button(root,text="EDIT",command=EditO).place(relwidth = .3, relheight = .06, relx =.1, rely =.79)
    Button(root,text="DELETE",command=DeleteO).place(relwidth = .3,relheight = .06,relx = .1,rely = .9)
    Button(root,text="CHECK ACCOUNT",command=CheckAcc).place(relwidth = .3, relheight = .06, relx= .55, rely=.68)
    Button(root, text="CLEAR",command=Clear).place(relwidth = .3, relheight = .06, relx = .55, rely = .79)
    
    table = ttk.Treeview(root, columns = ('ID','Name','Birth','Address','Phone','Sex','Signature','EmployeeAccountID'), show = 'headings')
    table.heading('ID', text='ID')
    table.heading('Name', text='Name')
    table.heading('Birth', text='Birth')
    table.heading('Address', text='Address')
    table.heading('Phone', text='Phone')
    table.heading('Sex', text='Sex')
    table.heading('Signature', text = 'Signature')
    table.heading('EmployeeAccountID', text = 'Employee Account ID')
    
    table.column('ID',width =45,stretch=NO)
    table.column('Name',minwidth = 50,width=150)
    table.column('Birth',width=75,stretch=NO)
    table.column('Address',minwidth=10,width=100,stretch=NO)
    table.column('Phone',width=75,stretch=NO)
    table.column('Sex',width=40,stretch=NO)
    table.column('Signature',width=100,stretch=NO)
    table.column('EmployeeAccountID',width=100)
    
    scrolly = Scrollbar(table)
    scrolly.pack(side = RIGHT,fill=Y)
    
    
    table.bind("<<TreeviewSelect>>",displaySelectedItem)
    table.place(relwidth = .98,relheight= .35,relx=.01,rely=.12)
    ShowO()
    
    # Label
    Label(root, text="Customer ID: ").place(relwidth = .12, relheight = .04, relx =.01, rely =.48)
    
    Label(root, text="Customer name: ").place(relwidth = .12, relheight = .04, relx =.01, rely =.53)
        
    Label(root, text="Date of birth: ").place(relwidth = .12, relheight = .04, relx =.01, rely =.58)
        
    Label(root, text="Address: ").place(relwidth = .12, relheight = .04, relx =.01, rely =.63)

    Label(root, text="Phone: ").place(relwidth = .16, relheight = .04, relx =.5, rely =.48)
        
    Label(root, text="Sex: ").place(relwidth = .16, relheight = .04, relx =.5, rely =.53)
        
    Label(root, text="Signature: ").place(relwidth = .16, relheight = .04, relx =.5, rely =.58)
    if permission =="admin": 
        Label(root, text="Employee Account ID: ").place(relwidth = .16, relheight = .04, relx =.5, rely =.63)
    
    #Entry
    
    ID_field = Entry(root, font="Times 12",state='readonly')
    ID_field.place(relwidth = .25, relheight = .04, relx =.13, rely =.48)
    
    Name_field = Entry(root,font="Times 12")
    Name_field.place(relwidth = .25, relheight = .04, relx =.13, rely =.53)
        
    Address_field = Entry(root,font="Times 12")
    Address_field.place(relwidth = .35, relheight = .04, relx =.13, rely =.63)
        
    Phone_field = Entry(root,font="Times 12")
    Phone_field.place(relwidth = .3, relheight = .04, relx =.67, rely =.48)
        
    Signature_field = Entry(root,font="Times 12",state="readonly")
    Signature_field.place(relwidth = .3, relheight = .04, relx =.67, rely =.58)
        
    nday = StringVar()
    daychoosen = ttk.Combobox(root,textvariable = nday,state="readonly")
    daychoosen['values'] = ("01","02","03","04","05","06","07","08","09",10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
    daychoosen.place(relwidth = .07, relheight =.04, relx = .13, rely = .58)
    
    nmonth = StringVar()
    monthchoosen = ttk.Combobox(root,textvariable = nmonth,state="readonly")
    monthchoosen['values'] = ("01", "02","03","04","05","06","07","08","09","10","11","12")
    monthchoosen.place(relwidth = .07, relheight =.04, relx = .2, rely = .58)
        
    nyear = IntVar()
    yearchoosen = ttk.Combobox(root,textvariable = nyear,state="readonly")
    year = []
    for i in range(1950,2022):
        year.append(i)
    yearchoosen['values'] = (year)
    yearchoosen.place(relwidth = .1, relheight =.04, relx = .27, rely = .58)
    
    nSex = StringVar()
    Sexchoosen = ttk.Combobox(root,textvariable = nSex, state='readonly')
    Sexchoosen['values'] = ("Nam","Nữ")
    Sexchoosen.place(relwidth = .12, relheight = .04, relx =.67, rely =.53)  
    
    if permission == 'admin':
        nEmployeeID = StringVar()
        employeechoosen = ttk.Combobox(root,textvariable= nEmployeeID,state='readonly')
        conn = sql.connect("Bank.db")
        c = conn.cursor()
        sql_ID = """
        SELECT EmployeeAccountID FROM EmployeeAccount
        """
        c.execute(sql_ID)
        rows = c.fetchall()
        data = []
        for row in rows:
            for i in row:
                data.append(i)
        employeechoosen['values'] = (data)
        employeechoosen.place(relwidth = .25, relheight = .04, relx =.67, rely =.63)
        conn.close()
    
    root.mainloop()