import sqlite3 as sql

databasePath = "Bank.db"

def getAllCustomer():
    try:
        # Connect database
        conn = sql.connect(databasePath)

        # Create cursor
        c = conn.cursor();
        
        query = "Select * from Customer"
        c.execute(query)
        
        result = c.fetchall()
        
        # Execute query
        conn.commit()
    except Exception:
        return -1
    finally:
        # Close connection
        conn.close()

    return result

def getCustomerById(CustomerId):
    try:
        # Connect database
        conn = sql.connect(databasePath)

        # Create cursor
        c = conn.cursor();
        
        query = "Select * from Customer where CustomerID = (?)"
        c.execute(query, (CustomerId,))
        
        result = c.fetchone()

        # Execute query
        conn.commit()
    except Exception:
        return -1
    finally:
        # Close connection
        conn.close()
    
    return result

# Get customer's signature image paths
def getImgPathById(CustomerId):
    try:
        # Connect database
        conn = sql.connect(databasePath)

        # Create cursor
        c = conn.cursor();
        
        query = "Select ImgPath from CustomerSignature where CustomerID = (?)"
        c.execute(query, (CustomerId,))
        
        result = c.fetchall()

        # Execute query
        conn.commit()
    except Exception:
        return -1
    finally:
        # Close connection
        conn.close()
    
    return result

# Get customer's signature data
def getCustomerSignatureById(CustomerId):
    try:
        # Connect database
        conn = sql.connect(databasePath)

        # Create cursor
        c = conn.cursor();
        
        query = "Select * from CustomerSignature where CustomerID = (?)"
        c.execute(query, (CustomerId,))
        
        result = c.fetchall()

        # Execute query
        conn.commit()
    except Exception:
        return -1
    finally:
        # Close connection
        conn.close()
    
    return result

# Add customer's signature data
def addCustomerSignature(CustomerId, ImgPath):
    try:
        # Connect database
        conn = sql.connect(databasePath)

        # Create cursor
        c = conn.cursor();
        
        query = "INSERT INTO CustomerSignature VALUES( ?, ?)"
        c.execute(query, (CustomerId, ImgPath))

        # Execute query
        conn.commit()
    except Exception:
        return -1
    finally:
        # Close connection
        conn.close()
    
    return 1

# Delete customer's signature data
def delCustomerSignature(CustomerId, ImgPath):
    try:
        # Connect database
        conn = sql.connect(databasePath)

        # Create cursor
        c = conn.cursor();
        
        query = """DELETE FROM CustomerSignature 
                WHERE CustomerID = ? and ImgPath = ?"""
        c.execute(query, (CustomerId, ImgPath))

        # Execute query
        conn.commit()
    except Exception:
        return -1
    finally:
        # Close connection
        conn.close()
    
    return 1

# Update customer's signature data
def updateCustomerSignature(CustomerId, ImgPath, newId, newPath):
    try:
        # Connect database
        conn = sql.connect(databasePath)

        # Create cursor
        c = conn.cursor();
        
        query = """UPDATE CustomerSignature 
                SET CustomerID = ? and ImgPath = ? 
                WHERE CustomerID = ? and ImgPath = ?"""
        c.execute(query, (newId, newPath, CustomerId, ImgPath))

        # Execute query
        conn.commit()
    except Exception:
        return -1
    finally:
        # Close connection
        conn.close()
    
    return 1