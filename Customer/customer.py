import sqlite3 as sql

conn = sql.connect("Bank.db")
class Customer:
    count = 1
    
    def __init__(self,CustomerName,DateOfBirth,Address,Phone,Sex,SignatureFolder):
        #self.CustomerID = self.get_CustomerID()
        self.CustomerName = CustomerName
        self.DateOfBirth = DateOfBirth
        self.Address = Address
        self.Phone = Phone
        self.Sex = Sex
        self.SignatureFolder = SignatureFolder
    
    def create_ID(self):
        if Customer.count < 10 and Customer.count > 0:
            ID = "KH"+"0"+str(Customer.count)
        else :
            ID = "KH"+str(Customer.count)
        return ID
    
    def get_CustomerID(self):
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
        return ID
    
    def ID(self,co):
        if int(co) < 10 and int(co) > 0:
            return "KH"+"0"+str(co)
        else: return "KH"+str(co)
        
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
    
    def get_SignatureFolder(self):
        return self.SignatureFolder
    
    def set_SignatureFolder(self,SignatureFolder):
        self.SignatureFolder = SignatureFolder
    
    def show(self):
        return self.CustomerID+" - "+self.CustomerName+" - "+self.DateOfBirth+" - "+self.Address+" - "+self.Phone+" - "+self.Sex+" - "+self.SignatureFolder
    
    def AddCustomer(self):
        c = conn.cursor()
        sql_add_ctm = """INSERT INTO Customer(CustomerID,CustomerName,DateOfBirth,Address,Phone,Sex,SignatureFolder) 
        VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}")
        """.format(self.get_CustomerID(),self.CustomerName,self.DateOfBirth,self.Address,self.Phone,self.Sex,self.SignatureFolder)
        c.execute(sql_add_ctm)
        conn.commit()
        
    def DeleteCustomer(self,deleteID):
        c = conn.cursor()
        sql_delete_ctm ="""
        DELETE FROM Customer WHERE CustomerID = '{0}'
        """.format(deleteID)
        c.execute(sql_delete_ctm)
        conn.commit()
        
        sql_delete_Acc = """
        DELETE FROM CustomerAccount WHERE CustomerID = '{0}'
        """.format(deleteID)
        c.execute(sql_delete_Acc)
        conn.commit()
        
    def EditCustomer(self,editID):
        c = conn.cursor()
        sql_edit_ctm ="""
        UPDATE Customer SET CustomerName = '{0}', DateOfBirth = '{1}', Address = '{2}', Phone = '{3}', Sex = '{4}', SignatureFolder = '{5}'
        WHERE CustomerID = '{6}'
        """.format(self.CustomerName,self.DateOfBirth,self.Address,self.Phone,self.Sex,self.SignatureFolder,editID)
        c.execute(sql_edit_ctm)
        conn.commit()
        