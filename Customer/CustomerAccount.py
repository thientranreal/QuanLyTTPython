import sqlite3 as sql

conn = sql.connect('Bank.db')

class CustomerAccount:
    count = 1
    
    def __init__(self,Balance,AccountOpenDate,AccountType,CustomerID,EmployeeManageID):
        #self.CustomerAccountID = CustomerAccountID 
        self.Balance = Balance
        self.AccountOpenDate =AccountOpenDate
        self.AccountType = AccountType
        self.CustomerID = CustomerID
        self.EmployeeManageID = EmployeeManageID
    
    def create_ID_Acc(self):
        if CustomerAccount.count < 10 and CustomerAccount.count > 0:
            IDAcc = "TKKH"+"0"+str(CustomerAccount.count)
        else :
            IDAcc = "TKKH"+str(CustomerAccount.count)
        return IDAcc
    
    def get_CustomerID_Acc(self):
        c = conn.cursor()
        sql_ID = """
        SELECT CustomerAccountID FROM CustomerAccount
        """
        c.execute(sql_ID)
        data = ""
        rows = c.fetchall()
        for row in rows:
            data = str(row[0])
        Id = ""
        while True:
            Id = self.create_ID_Acc()
            if Id == data:
                CustomerAccount.count+=1
                if CustomerAccount.count < 10 and CustomerAccount.count > 0:
                    IDAcc = "TKKH"+"0"+str(CustomerAccount.count)
                    break
                else :
                    IDAcc = "TKKH"+str(CustomerAccount.count)
                    break
            CustomerAccount.count+=1
        return IDAcc
    
    def set_Balance(self,Balance):
        self.Balance = Balance
        
    def get_Balance(self):
        return self.Balance
    
    def set_AccountOpenDate(self,AccountOpenDate):
        self.AccountOpenDate =AccountOpenDate
        
    def get_AccountOpenDate(self):
        return self.AccountOpenDate
    
    def set_AccountType(self,AccountType):
        self.AccountType = AccountType
        
    def get_AccountType(self):
        return self.AccountType
    
    def set_CustomerID(self,CustomerID):
        self.CustomerID = CustomerID
        
    def get_CustomerID(self):
        return self.CustomerID
    
    def set_EmployeeManagerID(self,EmployeeManageID):
        self.EmployeeManageID = EmployeeManageID
        
    def get_EmployeeManageID(self):
        return self.EmployeeManageID
    
    def AddAccountCustomer(self):
        c = conn.cursor()
        sql_add_acc = """
            INSERT INTO CustomerAccount(CustomerAccountID,Balance,AccountOpenDate,AccountType,CustomerID,EmployeeManageID)
            VALUES ("{0}","{1}","{2}","{3}","{4}","{5}")
        """.format(self.get_CustomerID_Acc(),self.Balance,self.AccountOpenDate,self.AccountType,self.CustomerID,self.EmployeeManageID)
        c.execute(sql_add_acc)
        conn.commit()
        
    def DeleteAccountCustomer(self,deleteID):
        c = conn.cursor()
        sql_delete_Acc ="""
            DELETE FROM CustomerAccount WHERE CustomerAccountID = '{0}'
        """.format(deleteID)
        c.execute(sql_delete_Acc)
        conn.commit()
        
    def EditAccountCustomer(self,EditID):
        c = conn.cursor()
        sql_edit_Acc = """
            UPDATE CustomerAccount SET Balance = '{0}', AccountOpenDate = '{1}',AccountType = '{2}' , CustomerID = '{3}', EmployeeManageID = '{4}'
            WHERE CustomerAccountID = '{5}'
        """.format(self.Balance,self.AccountOpenDate,self.AccountType,self.CustomerID,self.EmployeeManageID,EditID)
        c.execute(sql_edit_Acc)
        conn.commit()