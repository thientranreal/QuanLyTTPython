import sqlite3 as sql
from tkinter import messagebox
from Customer import CustomerAccount as ctmAcc
from datetime import date

#conn = sql.connect("Bank.db")
class Customer:
    count = 1
    IDSignature = ""
    def __init__(self,CustomerName,DateOfBirth,Address,Phone,Sex,EmployeeAccountID):
        self.CustomerName = CustomerName
        self.DateOfBirth = DateOfBirth
        self.Address = Address
        self.Phone = Phone
        self.Sex = Sex
        self.EmployeeAccountID = EmployeeAccountID
        
    
    def create_ID(self):
        if Customer.count < 10 and Customer.count > 0:
            ID = "KH"+"0"+str(Customer.count)
        else :
            ID = "KH"+str(Customer.count)
        return ID
    
    def get_CustomerID(self):
        conn = sql.connect("Bank.db")
        c = conn.cursor()
        sql_ID="""
        SELECT CustomerID FROM Customer
        """
        c.execute(sql_ID)
        data = ""
        rows = c.fetchall()
        for row in rows:
            data = str(row[0])
        Id = ""
        while True:
            Id = self.create_ID()
            if Id == data:
                Customer.count +=1
                if Customer.count < 10 and Customer.count > 0:
                    ID = "KH"+"0"+str(Customer.count)
                    break
                else :
                    ID = "KH"+str(Customer.count)
                    break
            Customer.count+=1
        Customer.IDSignature = ID
        conn.close()
        return ID
        
    def set_CustomerName(self,CustomerName):
        self.CustomerName = CustomerName
        
    def get_CustomerName(self):
        return self.CustomerName
    
    def set_DateOfBirth(self,DateOfBirth):
        self.DateOfBirth = DateOfBirth
        
    def get_DateOfBirth(self):
        return self.DateOfBirth
    
    def set_Address(self,Address):
        self.Address = Address
        
    def get_Address(self):
        return self.Address
    
    def set_Phone(self,Phone):
        self.Phone = Phone
        
    def get_Phone(self):
        return self.Phone
    
    def set_Sex(self,Sex):
        self.Sex = Sex
        
    def get_Sex(self):
        return self.Sex
    
    def get_Signature(self):
        s = "SignatureImg/"+str(Customer.IDSignature)
        return s
    
    def get_currentDay():
        today = date.today()
        return today.strftime("%d/%m/%Y")
    
    def AddCustomer(self):
        conn = sql.connect("Bank.db")
        c = conn.cursor()
        sql_add_ctm = """INSERT INTO Customer(CustomerID,CustomerName,DateOfBirth,Address,Phone,Sex,SignatureFolder,EmployeeManageID) 
        VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}")
        """.format(self.get_CustomerID(),self.CustomerName,self.DateOfBirth,self.Address,self.Phone,self.Sex,self.get_Signature(),self.EmployeeAccountID)
        c.execute(sql_add_ctm)
        conn.commit()
        messagebox.showinfo("","Thêm thành công!")
        conn.close()
        
    def DeleteCustomer(self,deleteID):
        conn = sql.connect("Bank.db")
        c = conn.cursor()
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            sql_delete_ctm ="""
            DELETE FROM Customer WHERE CustomerID = '{0}'
            """.format(deleteID)
            c.execute(sql_delete_ctm)
            conn.commit()
            messagebox.showinfo("","Xoá thành công!")
        except sql.IntegrityError:
            messagebox.showerror("ERROR","Không thể xoá khách hàng vì khách hàng đang tồn tại tài khoảng!")
        conn.close()
            
        
    def EditCustomer(self,editID):
        conn = sql.connect("Bank.db")
        c = conn.cursor()
        sql_edit_ctm ="""
        UPDATE Customer SET CustomerName = '{0}', DateOfBirth = '{1}', Address = '{2}', Phone = '{3}', Sex = '{4}',EmployeeManageID = '{5}'
        WHERE CustomerID = '{6}'
        """.format(self.CustomerName,self.DateOfBirth,self.Address,self.Phone,self.Sex,self.EmployeeAccountID,editID)
        c.execute(sql_edit_ctm)
        conn.commit()
        messagebox.showinfo("","Sửa thành công!")
        conn.close()
        