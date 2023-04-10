from tkinter import *
from Customer import customer as ctm
from tkinter import messagebox
from Customer import Manager as Mg
from tkinter.filedialog import askopenfilename
# file hu
def Editframe(ID,Name,Date,Address,Phone,Sex,Signature):
    
    def get_Sex():
        if (var.get() == 1):
            return "Nam"
        else :
            return "Nữ"
            
    def EditO():
        cus = ctm.Customer(Name_field.get(),Date_field.get(),Address_field.get(),Phone_field.get(),get_Sex(),Signature_field.get())
        cus.EditCustomer(ID)
        messagebox.showinfo("","Sửa thành công!")
        
    def DeleteO():
        cus = ctm.Customer(Name_field.get(),Date_field.get(), Address_field.get(), Phone_field.get(), get_Sex(), Signature_field.get())
        cus.DeleteCustomer(ID)
        messagebox.showinfo("","Xoá thành công!")
        
            
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
        Mg.mainframe()
        
    
    root = Tk()
    root.minsize(height = 400,width = 500)
    #root.geometry("500x400")
    
        
    root.title("Thêm khách hàng")
        
    Label(root, text="Sửa khách hàng (ID = "+ID+" )",fg='red',font=('cambria',20)).place(relwidth = .7, relheight = .08, relx =.1, rely =.05)
        
    # Label 
        
    Label_CustomerName = Label(root, text="Customer name: ")
    Label_CustomerName.place(relwidth = .3, relheight = .1, relx =.01, rely =.17)
        
    Label_DateOfBirth = Label(root, text="Date of birth: ")
    Label_DateOfBirth.place(relwidth = .3, relheight = .1, relx =.01, rely =.275)
        
    Label_Address = Label(root, text="Address: ")
    Label_Address.place(relwidth = .3, relheight = .1, relx =.01, rely =.38)
    
    Label_Phone = Label(root, text="Phone: ")
    Label_Phone.place(relwidth = .3, relheight = .1, relx =.01, rely =.485)
        
    Label_Sex = Label(root, text="Sex: ")
    Label_Sex.place(relwidth = .3, relheight = .1, relx =.01, rely =.59)
        
    Label_Signature = Label(root, text="Signature: ")
    Label_Signature.place(relwidth = .3, relheight = .1, relx =.01, rely =.695)
        
    #Entry
        
    
    Name_field = Entry(root,font="Times 12")
    Name_field.place(relwidth = .6, relheight = .08, relx =.35, rely =.17)
    Name_field.delete(0,END)
    Name_field.insert(0, Name)
    
    Date_field = Entry(root,font="Times 12")
    Date_field.place(relwidth = .6, relheight = .08, relx =.35, rely =.275)
    Date_field.delete(0,END)
    Date_field.insert(0, Date)
        
    Address_field = Entry(root,font="Times 12")
    Address_field.place(relwidth = .6, relheight = .08, relx =.35, rely =.38)
    Address_field.delete(0,END)
    Address_field.insert(0, Address)
        
    Phone_field = Entry(root,font="Times 12")
    Phone_field.place(relwidth = .6, relheight = .08, relx =.35, rely =.485)
    Phone_field.delete(0,END)
    Phone_field.insert(0, Phone)
        
    Signature_field = Entry(root,font="Times 12")
    Signature_field.place(relwidth = .49, relheight = .08, relx =.35, rely =.695)
    Signature_field.delete(0,END)
    Signature_field.insert(0, Signature)
        
    var = IntVar()
    R1 = Radiobutton(root, text="Nam",variable=var,value=1,tristatevalue=0).place(relwidth = .1, relheight = .1, relx =.5, rely =.59)
    R2 = Radiobutton(root, text="Nữ",variable=var,value=2,tristatevalue=0).place(relwidth = .1, relheight = .1, relx =.75, rely =.59)
    
    
    Button(root,text="QUIT",command=Quit).place(relwidth = .3,relheight = .1,relx = .03, rely = .85)
    Button(root,text="EDIT",command=EditO).place(relwidth = .3, relheight = .1, relx =.36, rely =.85)
    Button(root,text="DELETE",command=DeleteO).place(relwidth = .3,relheight = .1,relx = .69,rely = .85)
    Button(root,text="...",command=lambda : browsefunc(ent=Signature_field)).place(relwidth = .1, relheight = .08, relx =.85, rely =.695)
    
    root.mainloop()