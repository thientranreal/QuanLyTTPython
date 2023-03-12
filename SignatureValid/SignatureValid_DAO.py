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