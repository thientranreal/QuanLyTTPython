from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3 as sql
import os
from tkinter import colorchooser
from configparser import ConfigParser

def EmployeeAccount(parentForm):
    parentForm.withdraw()
    root = Tk()
    root.title('Quan li tai khoan nhan vien')
    root.geometry("800x500")


    #Read our config file and grt colors
    parser = ConfigParser()
    path = os.path.dirname(__file__) + "\\treebase.ini"
    parser.read(path)
    # parser.read("treebase.ini")
    saved_primary_color = parser.get('colors', 'primary_color')
    saved_secondary_color = parser.get('colors', 'secondary_color')
    saved_highlight_color = parser.get('colors', 'highlight_color')

    def on_closing():
        parentForm.deiconify()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)



    def query_database():
        #Clear the Treeview
        for record in tree.get_children():
            tree.delete(record)

        #Create a database or connect to on that exists
        path = "Bank.db"
        conn = sql.connect(path)

        #Create a cursor instance
        c = conn.cursor()

        # c.execute('SELECT rowid, * FROM Employee')
        c.execute('SELECT * FROM EmployeeAccount')
        records = c.fetchall()
        
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                tree.insert(parent='', index='end', iid= count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow'))
            else:
                tree.insert(parent='', index='end', iid= count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow'))
            count += 1

        #Commit changes
        conn.commit()

        #Close our connection
        conn.close()




    def search_records():
        lookup_records = search_entry.get()

        #Close the search box
        search.destroy()

        #Clear the Treeview
        for record in tree.get_children():
            tree.delete(record)

        #Create a database or connect to on that exists
        path = "Bank.db"
        conn = sql.connect(path)

        #Create a cursor instance
        c = conn.cursor()

        c.execute('SELECT * FROM EmployeeAccount WHERE EmployeeID like ?', (lookup_records, ))
        records = c.fetchall()
        
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                tree.insert(parent='', index='end', iid= count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('evenrow'))
            else:
                tree.insert(parent='', index='end', iid= count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('oddrow'))
            count += 1

        #Commit changes
        conn.commit()

        #Close our connection
        conn.close()



    def lookup_records():
        global search_entry, search
        search = Toplevel(root)
        search.title("Lookup records")
        search.geometry("400x200")

        #Create label frame 
        search_frame = LabelFrame(search, text="ID")
        search_frame.pack(padx=10, pady=10)

        #Add entry box
        search_entry = Entry(search_frame, font=("Helvetica", 18))
        search_entry.pack(padx=20, pady=20)

        #Add button
        search_button = Button(search, text="Search records", command=search_records)
        search_button.pack(padx=20, pady=20)
        
        

    def primary_color():
        primary_color = colorchooser.askcolor()[1]
        if primary_color:
            tree.tag_configure("evenrow", background=primary_color)

            parser = ConfigParser()
            path = os.path.dirname(__file__) + "\\treebase.ini"
            parser.read(path)

            #Set the color change
            parser.set('colors', 'primary_color', primary_color)
            #Save the config file 
            with open(path, 'w') as configfile:
                parser.write(configfile)


    def secondary_color():
        secondary_color = colorchooser.askcolor()[1]
        if secondary_color:
            tree.tag_configure("oddrow", background=secondary_color)

            parser = ConfigParser()
            path = os.path.dirname(__file__) + "\\treebase.ini"
            parser.read(path)

            #Set the color change
            parser.set('colors', 'secondary_color', secondary_color)
            #Save the config file 
            with open(path, 'w') as configfile:
                parser.write(configfile)



    def highlight_color():
        highlight_color = colorchooser.askcolor()[1]
        if highlight_color:
            style.map('Treeview', background=[('selected', highlight_color)])

            parser = ConfigParser()
            path = os.path.dirname(__file__) + "\\treebase.ini"
            parser.read(path)

            #Set the color change
            parser.set('colors', 'highlight_color', highlight_color)
            #Save the config file 
            with open(path, 'w') as configfile:
                parser.write(configfile)


    def reset_colors():
        #Save original colors to config file
        parser = ConfigParser()
        path = os.path.dirname(__file__) + "\\treebase.ini"
        parser.read(path)
        parser.set('colors', 'primary_color', 'lightblue')
        parser.set('colors', 'secondary_color', 'white')
        parser.set('colors', 'highlight_color', '#347083')
        with open(path, 'w') as configfile:
            parser.write(configfile)

        #Reset colors
        tree.tag_configure("oddrow", background='white')
        tree.tag_configure("evenrow", background='lightblue')
        style.map('Treeview', background=[('selected', '#347083')])

    #Add menu
    menu = Menu(root)
    root.config(menu=menu)

    #Configure our menu
    option_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Options", menu=option_menu)

    #Drop down menu 
    option_menu.add_command(label="Primary color", command=primary_color)
    option_menu.add_command(label="Secondary color", command=secondary_color)
    option_menu.add_command(label="Highlight color", command=highlight_color)
    option_menu.add_separator()
    option_menu.add_command(label="Reset colors", command=reset_colors)
    option_menu.add_command(label="Exit", command=root.quit)


    #Search our menu
    search_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Search", menu=search_menu)

    #Drop down menu 
    search_menu.add_command(label="Search", command=lookup_records)
    search_menu.add_separator()
    search_menu.add_command(label="Reset", command=query_database)




    #Create a database or connect to on that exists
    path = "Bank.db"
    conn = sql.connect(path)

    #Create a cursor instance
    c = conn.cursor()

    #Create tabel
    c.execute('''CREATE TABLE if not exists EmployeeAccount(
            EmployeeAccountID text,
            Username text,
            Password text,
            AccountType text,
            EmployeeID text
            )
            ''')


    #Commit changes
    conn.commit()

    #Close our connection
    conn.close()


    

    #Add some style
    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview",
        background="lightgray",
        foreground="black",
        rowheight=25,  
        fieldbackground="lightgray"   
        )

    #Change selected color #347083
    style.map("Treeview", 
        background=[('selected', saved_highlight_color)]
        )


    #Create Treeview Frame
    tree_frame = Frame(root)
    tree_frame.pack(pady=10)


    #Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y, ipadx=3)

    # tree = ttk.Treeview(root)
    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    tree.pack()


    #Configure the Scrollbar
    tree_scroll.config(command=tree.yview)

    tree['columns'] = ("AccountID", "UserName", "Password", "Type", "EmployeeID")

    tree.column("#0", width=0, stretch=NO)
    tree.column("AccountID", anchor=CENTER, width=150)
    tree.column("UserName", anchor=CENTER, width=150)
    tree.column("Password", anchor=CENTER, width=150)
    tree.column("Type", anchor=CENTER, width=120, minwidth=100)
    tree.column("EmployeeID",anchor=CENTER, width=150, minwidth=100)


    tree.heading("#0", text="", anchor=CENTER)
    tree.heading("AccountID", text="AccountID", anchor=CENTER)
    tree.heading("UserName", text="UserName", anchor=CENTER)
    tree.heading("Password", text="Password", anchor=CENTER)
    tree.heading("Type", text="Type", anchor=CENTER)
    tree.heading("EmployeeID", text="EmployeeID", anchor=CENTER)




    #Create striped row tags
    tree.tag_configure("oddrow", background=saved_secondary_color)
    tree.tag_configure("evenrow", background=saved_primary_color)




    #Add record entry boxes
    data_frame = LabelFrame(root, text="Record")
    data_frame.pack(expand=YES)

    aid_label = Label(data_frame, text="AccountID")
    aid_label.grid(row=0, column=0, padx=10, pady=10)
    aid_entry = Entry(data_frame)
    aid_entry.grid(row=0, column=1, padx=10, pady=10)

    un_label = Label(data_frame, text="UserName")
    un_label.grid(row=0, column=2, padx=10, pady=10)
    un_entry = Entry(data_frame)
    un_entry.grid(row=0, column=3, padx=10, pady=10)

    p_label = Label(data_frame, text="Password")
    p_label.grid(row=1, column=0, padx=10, pady=10)
    p_entry = Entry(data_frame)
    p_entry.grid(row=1, column=1, padx=10, pady=10)

    t_label = Label(data_frame, text="Type")
    t_label.grid(row=1, column=2, padx=10, pady=10)
    t_entry = Entry(data_frame)
    t_entry.grid(row=1, column=3, padx=10, pady=10)

    eid_label = Label(data_frame, text="EmployeeID")
    eid_label.grid(row=1, column=4, padx=10, pady=10)
    eid_entry = Entry(data_frame)
    eid_entry.grid(row=1, column=5, padx=10, pady=10)





    #Add record
    def add_record():

        #Create a database or connect to on that exists
        path = "Bank.db"
        conn = sql.connect(path)

        #Create a cursor instance
        c = conn.cursor()

        # Get the value of the input field
        account_id = aid_entry.get()
        employee_id = eid_entry.get()

        # Prepare the SQL query with the parameter placeholder
        query = 'SELECT COUNT(*) FROM EmployeeAccount WHERE EmployeeAccountID = ? OR EmployeeID = ?'

        # Execute the query with the parameter value
        c.execute(query, (account_id, employee_id,))

        # Get the count value from the query result
        counter = c.fetchone()[0]

        # Check if the count is greater than zero
        if counter > 0:
            messagebox.showerror("ERROR", " The ID was exist in table EmployeeAccount.")
        else:
            #Add new record
            c.execute("INSERT into EmployeeAccount VALUES (:AID, :Username, :Password, :Type, :EID)",    
                {
                    'AID': aid_entry.get(),  
                    'Username': un_entry.get(),
                    'Password': p_entry.get(),
                    'Type': t_entry.get(),
                    'EID': eid_entry.get(),
                }           
                        )
            messagebox.showinfo('Congratulation', 'Add Successfull !')
            


        #Commit changes
        conn.commit()

        #Close our connection
        conn.close()

        global count
        if count % 2 == 0:
            tree.insert(parent='', index='end', iid= count, text='', values=(aid_entry.get(), un_entry.get(), p_entry.get(), t_entry.get(), eid_entry.get()), tags=('evenrow'))
        else:
            tree.insert(parent='', index='end', iid= count, text='', values=(aid_entry.get(), un_entry.get(), p_entry.get(), t_entry.get(), eid_entry.get()), tags=('oddrow'))

        count += 1

        #Clear the boxes
        aid_entry.delete(0, END)
        un_entry.delete(0, END)
        p_entry.delete(0, END)
        t_entry.delete(0, END)
        eid_entry.delete(0, END)


        #Clear the treeview table
        tree.delete(*tree.get_children())
        query_database()


    #Remove all records
    def remove_all():
        #Add a little message box 
        respone = messagebox.askyesno("Delete all ?", "This will delete everything from the table! \n Are you sure ?")

        #Add logic for message box
        if respone == 1:
            for record in tree.get_children():
                tree.delete(record)

            #Create a database or connect to on that exists
            path = "Bank.db"
            conn = sql.connect(path)

            #Create a cursor instance
            c = conn.cursor()

            #Delete everything from database
            c.execute("DROP TABLE EmployeeAccount")
        

            #Commit changes
            conn.commit()

            #Close our connection
            conn.close()

            #Clear the boxes
            clear_entries()

            #Recreate the table
            create_table_again()



    #Remove one record
    '''
    def remove_one():
        x = tree.selection()[0]
        tree.delete(x)

        #Create a database or connect to on that exists
        path = "Bank.db"
        conn = sql.connect(path)

        #Create a cursor instance
        c = conn.cursor()

        #Delete from database
        c.execute("DELETE from EmployeeAccount WHERE EmployeeID = " + aid_entry.get())
        

        #Commit changes
        conn.commit()

        #Close our connection
        conn.close()

        #Clear the boxes
        clear_entries()

        #Add a little message box 
        messagebox.showinfo("Delete", "Delete Sucessful!")
    '''
        

    #Remove many record
    def remove_many():
        #Add a little message box 
        respone = messagebox.askyesno("Delete selected ?", "This will delete everything selected from the table! \n Are you sure ?")

        #Add logic for message boxes
        if respone == 1: 
            #Designate selections
            x = tree.selection()

            #Create list of ID's
            ids_to_delete = []

            #Add selections to ids_to_delete list
            for record in x:
                ids_to_delete.append(tree.item(record, 'values')[0])


            #Delete from the treeview    
            for record in x:
                tree.delete(record)

            
            #Create a database or connect to on that exists
            path = "Bank.db"
            conn = sql.connect(path)

            #Create a cursor instance
            c = conn.cursor()

            #Delete everything selected from database
            c.executemany("DELETE FROM EmployeeAccount WHERE EmployeeAccountID = ?", [(a,) for a in ids_to_delete])
        

            #Commit changes
            conn.commit()

            #Close our connection
            conn.close()

            #Clear the boxes
            clear_entries()


    #Clear entry boxes
    def clear_entries():
        aid_entry.delete(0, END)
        un_entry.delete(0, END)
        p_entry.delete(0, END)
        t_entry.delete(0, END)
        eid_entry.delete(0, END)

    #Select record
    def select_record():

        #Clear entry boxes
        aid_entry.delete(0, END)
        un_entry.delete(0, END)
        p_entry.delete(0, END)
        t_entry.delete(0, END)
        eid_entry.delete(0, END)

        #Grab record number
        selected = tree.focus()

        #Grab record values
        values = tree.item(selected, "values")
        
        
        #Output to entry boxes
        aid_entry.insert(0, values[0])
        un_entry.insert(0, values[1])
        p_entry.insert(0, values[2])
        t_entry.insert(0, values[3])
        eid_entry.insert(0, values[4])



    #Update record
    def update_record():
        selected = tree.focus()
        tree.item(selected, text="", values=(aid_entry.get(), un_entry.get(), p_entry.get(), t_entry.get(), eid_entry.get()))
        

        #Update the database
        #Create a database or connect to on that exists
        path = "Bank.db"
        conn = sql.connect(path)

        #Create a cursor instance
        c = conn.cursor()

        # Get the value of the input field
        account_id = aid_entry.get()
        employee_id = eid_entry.get()

        # Prepare the SQL query with the parameter placeholder
        query = 'SELECT COUNT(*) FROM EmployeeAccount WHERE EmployeeAccountID = ? OR EmployeeID = ?'

        # Execute the query with the parameter value
        c.execute(query, (account_id, employee_id,))

        # Get the count value from the query result
        counter = c.fetchone()[0]

        # Check if the count is greater than zero
        if counter > 0:
            query_database()
            messagebox.showerror("ERROR", " The ID was exist in table EmployeeAccount.")
        else:
            c.execute('''UPDATE EmployeeAccount SET 

                Username = :Name,
                Password = :Password,
                AccountType = :Type,
                EmployeeID = :EID,  

                WHERE EmployeeAccountID = :AID''',  
                {
                    'AID': aid_entry.get(),  
                    'Name': un_entry.get(),
                    'Password': p_entry.get(),
                    'Type': t_entry.get(),
                    'EID': eid_entry.get(),
                }           
                        )
            messagebox.showinfo('Congratulation', 'Update Successfull !')



        #Commit changes
        conn.commit()

        #Close our connection
        conn.close()

        #Clear entry boxes
        aid_entry.delete(0, END)
        un_entry.delete(0, END)
        p_entry.delete(0, END)
        t_entry.delete(0, END)
        eid_entry.delete(0, END)


    #Create binding click function
    def clicker(e):
        select_record()


    #Move row up
    # def up():
    #     rows = tree.selection()
    #     for row in rows:
    #         tree.move(row, tree.parent(row), tree.index(row)-1) 


    #Move row up
    # def down():
    #     rows = tree.selection()
    #     for row in reversed(rows):
    #         tree.move(row, tree.parent(row), tree.index(row)+1) 


    def create_table_again():
        #Create a database or connect to on that exists
        path = "Bank.db"
        conn = sql.connect(path)

        #Create a cursor instance
        c = conn.cursor()

        #Create tabel
        c.execute('''CREATE TABLE if not exists EmployeeAccount (
            EmployeeAccountID text,
            Username text,
            Password text,
            AccountType text,
            EmployeeID text
            )
            ''')

        #Commit changes
        conn.commit()

        #Close our connection
        conn.close()


    #Add buttons
    button_frame = LabelFrame(root, text="Commands")
    button_frame.pack(expand=YES)

    update_button = Button(button_frame, text="Update record", command=update_record)
    update_button.grid(row=0, column=0, padx=20, pady=20)

    add_button = Button(button_frame, text="Add record", command=add_record)
    add_button.grid(row=0, column=1, padx=20, pady=20)

    remove_all_button = Button(button_frame, text="Remove all record", command=remove_all)
    remove_all_button.grid(row=0, column=2, padx=20, pady=20)

    # remove_one_button = Button(button_frame, text="Remove one selected", command=remove_one)
    # remove_one_button.grid(row=0, column=3, padx=20, pady=20)

    remove_many_button = Button(button_frame, text="Remove many selected", command=remove_many)
    remove_many_button.grid(row=0, column=4, padx=20, pady=20)

    # move_up_button = Button(button_frame, text="Move up", command=up)
    # move_up_button.grid(row=0, column=5, padx=20, pady=20)

    # move_down_button = Button(button_frame, text="Move down", command=down)
    # move_down_button.grid(row=0, column=6, padx=20, pady=20)

    selected_record_button = Button(button_frame, text="Clear entry boxes", command=clear_entries)
    selected_record_button.grid(row=0, column=7, padx=20, pady=20)


    #Bindings
    # tree.bind("<Double-1>", clicker)
    tree.bind("<ButtonRelease-1>", clicker)


    query_database()


    root.mainloop()