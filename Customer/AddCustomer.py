from tkinter import *
from tkinter.filedialog import askopenfilename
from Customer import customer as ctm
from tkinter import messagebox
from Customer import Manager as Mg
from tkinter import ttk
    
    
def Addframe(EmployeeID, permission, parentForm):
    
    def get_Sex():
        if (var.get() == 1):
            return "Nam"
        else :
            return "Nữ"
        
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
        if (Phone.isdigit() ==False):
            return False
        return True
                
    def AddO():
        Ngay = daychoosen.get()+"/"+monthchoosen.get()+"/"+yearchoosen.get()
        cus = ctm.Customer(Name_field.get(),Ngay,Address_field.get(),Phone_field.get(),get_Sex(),Signature_field.get())
        if (Name_field.get() == ""):
            messagebox.showerror("Error","Không được để trống tên!")
        elif (Address_field.get() == ""):
            messagebox.showerror("Error","Không được để trống địa chỉ!")
        elif (Phone_field.get() == ""):
            messagebox.showerror("Error","Không được để trống số điện thoại!")
        elif (var.get() != 1 and var.get() != 2):
            messagebox.showerror("Error","Chưa chọn giới tính!")
        elif (Signature_field.get() == ""):
            messagebox.showerror("Error","Chưa chọn địa chỉ ảnh")
        else:
            if (check_Date() == False):
                messagebox.showerror("Error","Lỗi ngày tháng năm sinh!")
            elif (check_Phone() == False):
                messagebox.showerror("Error","Lỗi số điện thoại!")
            else:
                cus.AddCustomer()
                messagebox.showinfo("","Thêm thành công!")
                root.destroy()
                Mg.mainframe()
            
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
            
    def Quit():
        root.destroy()
        Mg.mainframe(EmployeeID, permission, parentForm)
    
    root = Tk()
    root.minsize(height = 400,width = 500)
    #root.geometry("500x400")
    
        
    root.title("Thêm khách hàng")
        
    Label(root, text="Thêm khách hàng",fg='red',font=('cambria',20)).place(relwidth = .5, relheight = .08, relx =.1, rely =.05)
        
    # Label 
        
    Label(root, text="Customer name: ").place(relwidth = .3, relheight = .1, relx =.01, rely =.17)
        
    Label(root, text="Date of birth: ").place(relwidth = .3, relheight = .1, relx =.01, rely =.275)
        
    Label(root, text="Address: ").place(relwidth = .3, relheight = .1, relx =.01, rely =.38)
    
    Label(root, text="Phone: ").place(relwidth = .3, relheight = .1, relx =.01, rely =.485)
    
    Label(root, text="Sex: ").place(relwidth = .3, relheight = .1, relx =.01, rely =.59)
        
    Label(root, text="Signature: ").place(relwidth = .3, relheight = .1, relx =.01, rely =.695)
        
    #Entry
    Name_field = Entry(root,font="Times 12")
    Name_field.place(relwidth = .6, relheight = .08, relx =.35, rely =.17)
    
    #Date_field = Entry(root,font="Times 12")
    #Date_field.place(relwidth = .6, relheight = .08, relx =.35, rely =.275)
        
    Address_field = Entry(root,font="Times 12")
    Address_field.place(relwidth = .6, relheight = .08, relx =.35, rely =.38)
        
    Phone_field = Entry(root,font="Times 12")
    Phone_field.place(relwidth = .6, relheight = .08, relx =.35, rely =.485)
        
    Signature_field = Entry(root,font="Times 12")
    Signature_field.place(relwidth = .49, relheight = .08, relx =.35, rely =.695)
        
    var = IntVar()
    R1 = Radiobutton(root, text="Nam",variable=var,value=1)
    R1.place(relwidth = .1, relheight = .1, relx =.5, rely =.59)
    R2 = Radiobutton(root, text="Nữ",variable=var,value=2)
    R2.place(relwidth = .1, relheight = .1, relx =.75, rely =.59)
        
    Button(root,text="QUIT",command=Quit).place(relwidth = .35,relheight = .1,relx = .1, rely = .85)
    Button(root,text="ADD",command=AddO).place(relwidth = .35, relheight = .1, relx =.55, rely =.85)
    Button(root,text="...",command=lambda : browsefunc(ent=Signature_field)).place(relwidth = .1, relheight = .08, relx =.85, rely =.695)
    
    nday = StringVar()
    daychoosen = ttk.Combobox(root,textvariable = nday,state="readonly")
    daychoosen['values'] = ("01","02","03","04","05","06","07","08","09",10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
    daychoosen.current(0)
    daychoosen.place(relwidth = .15, relheight =.08, relx = .35, rely = .275)
    
    nmonth = StringVar()
    monthchoosen = ttk.Combobox(root,textvariable = nmonth,state="readonly")
    monthchoosen['values'] = ("01", "02","03","04","05","06","07","08","09","10","11","12")
    monthchoosen.current(0)
    monthchoosen.place(relwidth = .15, relheight =.08, relx = .5, rely = .275)
        
    nyear = StringVar()
    yearchoosen = ttk.Combobox(root,textvariable = nyear,state="readonly")
    year = []
    for i in range(1950,2022):
        year.append(i)
    yearchoosen['values'] = (year)
    yearchoosen.current(0)
    yearchoosen.place(relwidth = .15, relheight =.08, relx = .65, rely = .275)
    
    root.mainloop()