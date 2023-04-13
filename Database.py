import sqlite3 as sql

# Create database
conn = sql.connect("Bank.db")

# Create cursor
c = conn.cursor()

# CREATE TABLE Customer
c.execute("""
              CREATE TABLE Customer (
                CustomerID text NOT NULL PRIMARY KEY,
                CustomerName text,
                DateOfBirth text,
                Address text,
                Phone text,
                Sex text,
                SignatureFolder text
            )
          """)
          
#  CREATE TABLE Employee
c.execute("""
              CREATE TABLE Employee (
                EmployeeID text NOT NULL PRIMARY KEY,
                EmployeeName text,
                Address text,
                Phone text,
                DateOfBirth text,
            	Sex text,
            	Email text
            )
          """)

# CREATE TABLE EmployeeAccount
c.execute("""
              CREATE TABLE EmployeeAccount (
                EmployeeAccountID text NOT NULL PRIMARY KEY,
                Username text,
            	Password text,
            	AccountType text,
            	EmployeeID text NOT NULL,
            	FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
            )
          """)
          
# CREATE TABLE CustomerAccount
c.execute("""
              CREATE TABLE CustomerAccount (
                CustomerAccountID text NOT NULL PRIMARY KEY,
                Balance integer,
                AccountOpenDate text,
            	AccountType text,
                CustomerID text NOT NULL,
            	EmployeeManageID text NOT NULL,
            	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
            	FOREIGN KEY (EmployeeManageID) REFERENCES EmployeeAccount(EmployeeAccountID)
            )
          """)
         
# CREATE TABLE Exchange
c.execute("""
              CREATE TABLE Exchange (
            	TransactionID text NOT NULL PRIMARY KEY,
            	CustomerTransferID text NOT NULL,
                CustomerReceiveID text,
                TransactionDate text,
            	MoneySend integer,
            	EmployeeAccountID text NOT NULL,
            	FOREIGN KEY (CustomerTransferID) REFERENCES CustomerAccount(CustomerAccountID),
            	FOREIGN KEY (CustomerReceiveID) REFERENCES CustomerAccount(CustomerAccountID),
            	FOREIGN KEY (EmployeeAccountID) REFERENCES EmployeeAccount(EmployeeAccountID)
            )
          """)
          
# Insert Into Customer
c.execute("""
              INSERT INTO Customer
                VALUES
                ('KH01', 'Nguyễn Thị Ánh', '01/03/1975', '123 Nguyễn Văn Cừ, Quận 1, TP.HCM', '0901234567', 'Nữ', 'SignatureImg/KH01'),
                ('KH02', 'Lê Văn Đức', '20/05/1998', '456 Trần Hưng Đạo, Quận 5, TP.HCM', '0909876543', 'Nam', 'SignatureImg/KH02'),
                ('KH03', 'Phạm Thị Mai', '17/03/2000', '789 Nguyễn Thị Minh Khai, Quận 3, TP.HCM', '0902223333', 'Nữ', 'SignatureImg/KH03'),
                ('KH04', 'Nguyễn Văn Hưng', '29/12/1980', '555 Lê Lợi, Quận 1, TP.HCM', '0904445555', 'Nam', 'SignatureImg/KH04'),
                ('KH05', 'Trần Thị Thanh', '01/12/1975', '888 Phạm Ngọc Thạch, Quận 3, TP.HCM', '0906667777', 'Nữ', 'SignatureImg/KH05');
          """)
          
# INSERT INTO Employee
c.execute("""
          INSERT INTO Employee
            VALUES
            ('NV01', 'Huỳnh Thị Ánh Ngọc', '12 Lý Tự Trọng, Quận 1', '0901234567', '01/01/1990', 'Nữ', 'abccoop@gmail.com'),
            ('NV02', 'Nguyễn Thị Huyền Trang', '54 Trần Hưng Đạo, Quận 5', '0902345678', '05/05/1995', 'Nữ', 'xyzcoop@gmail.com'),
            ('NV03', 'Lê Văn Thắng', '234 Lê Văn Sỹ, Quận 3', '0903456789', '10/08/1992', 'Nam', 'xyzcoop@gmail.com'),
            ('NV04', 'Phạm Thị Hoài', '111 Lê Lợi, Quận 1', '0904567891', '21/03/1993', 'Nữ', 'xyzcoop@gmail.com'),
            ('NV05', 'Trần Minh Hiếu', '77 Nguyễn Trãi, Quận 5', '0905678912', '31/12/1994', 'Nam', 'xyzcoop@gmail.com');
          """)
          
# INSERT INTO EmployeeAccount
c.execute("""
          INSERT INTO EmployeeAccount
            VALUES 
            ('TK01', 'Employee', '123456', 'normal', 'NV01'),
            ('TK02', 'Employee', '123456', 'normal', 'NV02'),
            ('TK03', 'Employee', '123456', 'normal', 'NV03'),
            ('TK04', 'Employee', '123456', 'normal', 'NV04'),
            ('TK05', 'Employee', '123456', 'normal', 'NV05');
          """)
          
# INSERT INTO CustomerAccount
c.execute("""
          INSERT INTO CustomerAccount
            VALUES
            ('TKKH01', 2000000, '28/12/2020', 'normal', 'KH01', 'TK01'),
            ('TKKH02', 6000000, '03/05/2021', 'normal', 'KH02', 'TK01'),
            ('TKKH03', 10000000, '30/05/2021', 'normal', 'KH03', 'TK03'),
            ('TKKH04', 5000000, '02/10/2021', 'normal', 'KH04', 'TK02'),
            ('TKKH05', 3000000, '08/07/2018', 'normal', 'KH05', 'TK02');
          """)

# INSERT INTO Exchange
c.execute("""
          INSERT INTO Exchange
            VALUES
            ('T01', 'TKKH01', 'TKKH03', '2022-01-01 08:00:00', 500000, 'TK02'),
            ('T02', 'TKKH04', 'TKKH01', '2022-01-05 10:00:00', 300000, 'TK02'),
            ('T03', 'TKKH04', 'TKKH02', '2022-01-10 14:00:00', 200000, 'TK01'),
            ('T04', 'TKKH02', 'TKKH05', '2022-02-02 09:00:00', 100000, 'TK05'),
            ('T05', 'TKKH03', 'TKKH01', '2022-02-05 11:00:00', 400000, 'TK03'),
            ('T06', 'TKKH02', 'TKKH03', '2022-02-08 13:00:00', 300000, 'TK04'),
            ('T07', 'TKKH01', 'TKKH03', '2022-03-03 07:00:00', 700000, 'TK01'),
            ('T08', 'TKKH01', NULL, '2022-03-05 11:00:00', 200000, 'TK01');
          """)
          
# Execute query
conn.commit()
# Close connection
conn.close()