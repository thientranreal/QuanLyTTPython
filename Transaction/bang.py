import sqlite3 as sql
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
from SignatureValid import SignatureValid_GUI as sn

def bangGUI(accId,parentForm):
    # Tạo đối tượng Signature Valid
    snGui = sn.SignatureValid()
    
    parentForm.withdraw()
    # Tạo cửa sổ giao diện
    root = tk.Tk()
    root.title("Bảng giao dịch")
    
    def on_closing():
        parentForm.deiconify()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Kết nối database
    conn = sql.connect("Bank.db")
    c = conn.cursor()


    # Thiết lập kích thước cửa sổ
    canvas = tk.Canvas(root,width=500,height=300)
    canvas.grid(row=0, column=0)

    # Thiết lập khung chứa các chức năng
    frame = tk.Frame(root, borderwidth=1)
    frame.grid(row=0, column=0,padx=1,sticky="WN")

    frame_left = tk.Frame(frame, bd=5, relief="groove")
    frame_left.grid(row=0, column=0, padx=10, pady=10,rowspan=5)

    frame_right = tk.Frame(frame, bd=5, relief="groove")
    frame_right.grid(row=0, column=2, padx=10, pady=10,rowspan=5)

    frame_table = tk.Frame(frame, bd=5, relief="groove")
    frame_table.grid(row=5, column=0, padx=10, pady=10,rowspan=6,columnspan=3)

    # Thêm label và entry vào khung viền
    amount_label = tk.Label(frame_left, text="Nhập tài khoản Khách hàng:", font=15)
    amount_label.grid(row=0,column=0)
    id = tk.Entry(frame_left,width=40)
    id.grid(row=1,column=0)
    customer_id =""
    
            
            
    check_button = tk.Button(frame_left,text="Kiểm tra",font=15)
    check_button.grid(row=2,column=0)
    

    #giao diện nhập số tiền
    label = tk.Label(frame_right, font=15)
    label.grid_forget()
    money_entry = tk.Entry(frame_right)
    money_entry.grid_forget()
    receiver_label = tk.Label(frame_right, text="Nhập tài khoản nhận tiền:", font=15)
    receiver_label.grid_forget()
    receiverID_entry = tk.Entry(frame_right)
    receiverID_entry.grid_forget()
    confirm_button = tk.Button(frame_right, text="Xác nhận", font=15)
    confirm_button.grid_forget()

    def generate_code(last_code):
        # Lấy số cuối cùng trong mã hiện tại
        last_num = int(last_code[1:])
        # Tăng số đó lên 1 và chuyển thành chuỗi
        new_num = str(last_num + 1)
        # Thêm số 0 vào đầu chuỗi nếu cần thiết
        new_num_padded = new_num.zfill(2)
        # Tạo mã mới bằng cách kết hợp chữ 'T' với số đã được chuyển đổi
        new_code = 'T' + new_num_padded
        return new_code

    # Thiết lập nút Nạp tiền
    def NapTien():
        #Đóng giao diện khác
        label.grid(row=0, column=2)
        label.config(text="Nhập số tiền nạp")
        money_entry.grid(row=1, column=2)
        money_entry.delete(0,'end')
        receiver_label.grid_forget()
        receiverID_entry.grid_forget()
        conn = sql.connect("Bank.db")
        c = conn.cursor()

        # Thực hiện nạp tiền khi nhấn nút "Xác nhận"
        def NapTienConfirm():
            try:
                money = int(money_entry.get())
                if money <= 10000:
                    messagebox.showerror("Thông báo", "Vui lòng nhập số tiền lớn hơn 10000 Vnđ")
                else:
                    query = "SELECT Balance FROM CustomerAccount WHERE CustomerAccountID = ?"
                    c.execute(query, (id.get(),))
                    result = c.fetchone()
                    balance = result[0]
                    # Lấy mã giao dịch
                    c.execute('SELECT TransactionID FROM Exchange ORDER BY TransactionID DESC LIMIT 1;')
                    last_id = c.fetchone()[0]
                    new_balance = balance + money
                    a = "UPDATE CustomerAccount SET Balance = ? WHERE CustomerAccountID = ?"
                    c.execute(a, (new_balance, id.get()))
                    c.execute("INSERT INTO Exchange (TransactionID, CustomerTransferID,CustomerReceiveID,"
                             "TransactionDate,MoneySend,EmployeeAccountID) VALUES (:TransactionID, :CustomerTransferID,"
                             ":CustomerReceiveID,:TransactionDate,:MoneySend,:EmployeeAccountID)",
                             {'TransactionID': generate_code(last_id), 'CustomerTransferID': id.get(),
                              'CustomerReceiveID': None, 'TransactionDate': datetime.datetime.now(),
                              'MoneySend': money, 'EmployeeAccountID': accId})
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thông báo", "Nạp tiền thành công")
                    upDate()

            except ValueError:
                messagebox.showerror("Thông báo", "Vui lòng nhập một số nguyên.")

        # Hiển thị nút "Xác nhận" để thực hiện nạp tiền
        confirm_button.grid(row=2, column=2)
        confirm_button.config(command=lambda : NapTienConfirm())

    deposit_button = tk.Button(frame, text="Nạp tiền", font=15,state="disabled",width=10)
    deposit_button.grid(row=0, column=1)
    deposit_button.config(command=lambda : NapTien())

    # Thiết lập nút Chuyển tiền
    def ChuyenTien():
        # Hiển thị giao diện nhập số tiền chuyển
        label.grid(row=0, column=2)
        label.config(text="Nhập số tiền chuyển")
        money_entry.grid(row=1, column=2)
        money_entry.delete(0,'end')
        receiver_label.grid(row=2, column=2)
        receiverID_entry.grid(row=3, column=2)
        conn = sql.connect("Bank.db")
        c = conn.cursor()
        # Thực hiện chuyển tiền tiền khi nhấn nút "Xác nhận"
        def ChuyenTienConfirm():
            money = money_entry.get()
            # Lấy số tiền
            query = "SELECT Balance FROM CustomerAccount WHERE CustomerAccountID = ?"
            c.execute(query, (id.get(),))
            result = c.fetchone()
            balance = result[0]
            # Lấy mã giao dịch
            c.execute('SELECT TransactionID FROM Exchange ORDER BY TransactionID DESC LIMIT 1;')
            last_id = c.fetchone()[0]
            try:
                money = int(money_entry.get())
                if money <= 10000:
                    messagebox.showerror("Thông báo", "Vui lòng nhập số tiền lớn hơn 10000 Vnđ")
                elif money > balance:
                    messagebox.showerror("Thông báo", "Số tiền hiện tại không đủ")
                else:
                    #Trừ tiền người chuyển
                    new_balance = balance - money
                    a = "UPDATE CustomerAccount SET Balance = ? WHERE CustomerAccountID = ?"
                    c.execute(a, (new_balance, id.get()))
                    #Cộng tiền người nhận
                    query = "SELECT Balance FROM CustomerAccount WHERE CustomerAccountID = ?"
                    c.execute(query, (receiverID_entry.get(),))
                    result = c.fetchone()
                    balance = result[0]
                    new_balance = balance + money
                    a = "UPDATE CustomerAccount SET Balance = ? WHERE CustomerAccountID = ?"
                    c.execute(a, (new_balance, receiverID_entry.get()))
                    c.execute("INSERT INTO Exchange (TransactionID, CustomerTransferID,CustomerReceiveID,"
                              "TransactionDate,MoneySend,EmployeeAccountID) VALUES (:TransactionID, :CustomerTransferID,"
                              ":CustomerReceiveID,:TransactionDate,:MoneySend,:EmployeeAccountID)",
                                   {'TransactionID': generate_code(last_id),'CustomerTransferID': id.get(),
                                    'CustomerReceiveID': receiverID_entry.get(),'TransactionDate': datetime.datetime.now(),
                                    'MoneySend': money,'EmployeeAccountID': accId})
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thông báo", "Chuyển tiền thành công")
                    upDate()

            except ValueError:
                messagebox.showerror("Thông báo", "Vui lòng nhập một số nguyên.")

        confirm_button.grid(row=4, column=2)
        confirm_button.config(command=lambda: ChuyenTienConfirm())
    transfer_button = tk.Button(frame, text="Chuyển tiền", font=15,state="disabled",width=10)
    transfer_button.grid(row=1, column=1)
    transfer_button.config(command=lambda: ChuyenTien())

    # Thiết lập nút Rút tiền
    def RutTien():
        # Hiển thị giao diện nhập số tiền rút
        label.grid(row=0, column=2)
        label.config(text="Nhập số tiền rút")
        money_entry.grid(row=1, column=2)
        money_entry.delete(0, 'end')
        receiver_label.grid_forget()
        receiverID_entry.grid_forget()
        conn = sql.connect("Bank.db")
        c = conn.cursor()
        query = "SELECT Balance FROM CustomerAccount WHERE CustomerAccountID = ?"
        c.execute(query, (id.get(),))
        result = c.fetchone()
        balance = result[0]
        # Thực hiện nạp tiền khi nhấn nút "Xác nhận"
        def RutTienConfirm():
            try:
                money = int(money_entry.get())
                if money <= 10000:
                    messagebox.showerror("Thông báo", "Vui lòng nhập số tiền lớn hơn 10000 Vnđ")
                elif money > balance:
                    messagebox.showerror("Thông báo", "Số tiền hiện tại không đủ")
                else:                   
                    # Lấy mã giao dịch
                    c.execute('SELECT TransactionID FROM Exchange ORDER BY TransactionID DESC LIMIT 1;')
                    last_id = c.fetchone()[0]
                    new_balance = balance - money
                    a = "UPDATE CustomerAccount SET Balance = ? WHERE CustomerAccountID = ?"
                    c.execute(a, (new_balance, id.get()))
                    c.execute("INSERT INTO Exchange (TransactionID, CustomerTransferID,CustomerReceiveID,"
                              "TransactionDate,MoneySend,EmployeeAccountID) VALUES (:TransactionID, :CustomerTransferID,"
                              ":CustomerReceiveID,:TransactionDate,:MoneySend,:EmployeeAccountID)",
                              {'TransactionID': generate_code(last_id), 'CustomerTransferID': id.get(),
                               'CustomerReceiveID': None, 'TransactionDate': datetime.datetime.now(),
                               'MoneySend': -(money), 'EmployeeAccountID': accId})
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thông báo", "Rút tiền thành công")
                    upDate()

            except ValueError:
                messagebox.showerror("Thông báo", "Vui lòng nhập một số nguyên.")

        # Hiển thị nút "Xác nhận" để thực hiện nạp tiền
        confirm_button.grid(row=2, column=2)
        confirm_button.config(command=lambda: RutTienConfirm())
    withdraw_button = tk.Button(frame, text="Rút tiền", font=15,state="disabled",width=10)
    withdraw_button.grid(row=2, column=1)
    withdraw_button.config(command=lambda : RutTien())

    tilte_label = tk.Label(frame_table,text="Danh sách khách hàng", font=("Arial Bold",15))
    tilte_label.grid(row=0,column=0)
    def on_select_TK(event):
        selected_item = event.widget.selection()[0]
        # Lấy dữ liệu từ cột ID của dòng được chọn
        idAccount = event.widget.item(selected_item, 'values')[0]
        if receiverID_entry.winfo_ismapped():
            receiverID_entry.delete(0, 'end')
            receiverID_entry.insert(0, idAccount)
        else:
            id.delete(0,'end')
            id.insert(0,idAccount)
            deposit_button.config(state="disabled")
            transfer_button.config(state="disabled")
            withdraw_button.config(state="disabled")
            label.grid_forget()
            money_entry.grid_forget()
            receiver_label.grid_forget()
            receiverID_entry.grid_forget()
            confirm_button.grid_forget()

    def on_select(event):
        id.delete(0,'end')
        # Lấy chỉ mục của dòng được chọn trong treeview
        selected_item = event.widget.selection()[0]
        # Lấy dữ liệu từ cột CustomerID của dòng được chọn
        global customer_id
        customer_id = event.widget.item(selected_item, 'values')[0]
        check_button.config(command=lambda : checkId(id.get(),customer_id))
        # Kiểm tra CustomerID với thuộc tính 1 bảng khác
        conn = sql.connect("Bank.db")
        c = conn.cursor()
        c.execute("SELECT * FROM CustomerAccount WHERE CustomerID=?", (customer_id,))
        order_rows = c.fetchall()
        treeTk = ttk.Treeview(frame_table)
        treeTk.grid(row=3,column=0)
        tilte_label_2 = tk.Label(frame_table, text="Danh sách tài khoản khách hàng", font=("Arial Bold",15))
        tilte_label_2.grid(row=2, column=0)
        if order_rows:
            if hasattr(event.widget, "treeTk"):
                event.widget.treeTk.destroy()
            treeTk["columns"] = ("CustomerAccountID", "Balance", "AccountOpenDate","AccountType","EmployeeManageID")
            treeTk.configure(height=3,)
            treeTk.heading("CustomerAccountID", text="Mã tài khoản")
            treeTk.heading("Balance", text="Số dư")
            treeTk.heading("AccountOpenDate", text="Ngày tạo")
            treeTk.heading("AccountType", text="Loại KH")
            treeTk.heading("EmployeeManageID", text="Mã NV")

            for row in order_rows:
                treeTk.insert("", "end", values=row)
            treeTk.column("#0", width=0, stretch=tk.NO)
            treeTk.column("CustomerAccountID", width=150)
            treeTk.column("Balance", width=100)
            treeTk.column("AccountOpenDate", width=100)
            treeTk.column("AccountType", width=100)
            treeTk.column("EmployeeManageID", width=50)
            treeTk.column("#0", width=0, stretch=tk.NO)
            treeTk.bind("<<TreeviewSelect>>", on_select_TK)
            treeTk.grid()
            # Lưu trữ tham chiếu đến Treeview mới
            event.widget.treeTk = treeTk
            conn.close()

    tree = ttk.Treeview(frame_table)
    tree.grid(row=1,column=0)
    tree["columns"] = ("CustomerID","CustomerName","DateOfBirth","Address","Phone","Sex")
    tree.configure(height=5)

    # Thiết lập thông tin cho các cột
    tree.heading("CustomerID", text="ID")
    tree.heading("CustomerName", text="Tên khách hàng")
    tree.heading("DateOfBirth", text="Ngày sinh")
    tree.heading("Address", text="Địa chỉ")
    tree.heading("Phone", text="Số điện thoại")
    tree.heading("Sex", text="Giới tính")
    c.execute("SELECT * FROM Customer")
    rows = c.fetchall()

    for row in rows:
        tree.insert("","end", values=row)
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("CustomerID", width=50)
    tree.column("CustomerName", width=150)
    tree.column("DateOfBirth", width=100)
    tree.column("Address", width=250)
    tree.column("Phone", width=100)
    tree.column("Sex", width=60)

    tree.bind("<<TreeviewSelect>>", on_select)
    tree.grid()
    
    tilte_label_3 = tk.Label(frame_table, text="Lịch sử giao dịch", font=("Arial Bold",15))
    tilte_label_3.grid(row=4, column=0)
    c.execute("SELECT * from Exchange")
    treeExchange = ttk.Treeview(frame_table)
    treeExchange.grid(row=5, column=0)
    treeExchange["columns"] = ("TransactionID", "CustomerTransferID", "CustomerReceiveID", "TransactionDate", "MoneySend", "EmployeeAccountID")
    treeExchange.configure(height=5)
    
    # Thiết lập thông tin cho các cột
    treeExchange.heading("TransactionID", text="Mã giao dịch")
    treeExchange.heading("CustomerTransferID", text="Mã TK người chuyển")
    treeExchange.heading("CustomerReceiveID", text="Mã TK người nhận")
    treeExchange.heading("TransactionDate", text="Thời gian giao dịch")
    treeExchange.heading("MoneySend", text="Số tiền(VNĐ)")
    treeExchange.heading("EmployeeAccountID", text="Mã Nhân viên")
    conn = sql.connect("Bank.db")
    c.execute("SELECT * FROM Exchange")
    rows = c.fetchall()
    for row in rows:
        treeExchange.insert("", "end", values=row)
        treeExchange.column("#0", width=0, stretch=tk.NO)
        treeExchange.column("TransactionID", width=50)
        treeExchange.column("CustomerTransferID", width=120)
        treeExchange.column("CustomerReceiveID", width=120)
        treeExchange.column("TransactionDate", width=150)
        treeExchange.column("MoneySend", width=100)
        treeExchange.column("EmployeeAccountID", width=120)
    #Cập nhật lịch sử giao dịch
    def upDate():
        # xóa tất cả các item trong Treeview
        for item in treeExchange.get_children():
            treeExchange.delete(item)
    
        # lấy dữ liệu mới từ cơ sở dữ liệu
        conn = sql.connect("Bank.db")
        c = conn.cursor()
        c.execute("SELECT * FROM Exchange")
        rows = c.fetchall()
        conn.close()
    
        # thêm item vào Treeview cho mỗi bản ghi dữ liệu mới
        for row in rows:
            treeExchange.insert("", "end", values=row)
    print(customer_id+"1")
    #Kiểm tra id
    def checkId(AccountID,customer_id):
        print(customer_id)
        conn = sql.connect("Bank.db")
        c = conn.cursor()
        query = "SELECT * FROM CustomerAccount WHERE CustomerAccountID = ?"
        c.execute(query, (AccountID,))
        results = c.fetchall()
        
        conn.close()
        if results == []:
            messagebox.showerror("Thông báo","Không tìm thấy tài khoản khách hàng" )
            deposit_button.config(state="disabled")
            transfer_button.config(state="disabled")
            withdraw_button.config(state="disabled")
        else:
            snGui.Gui(customer_id, root, deposit_button, transfer_button, withdraw_button)

    # Đóng kết nối đến cơ sở dữ liệu
    conn.close()

    # Mở cửa sổ giao diện
    root.mainloop()
    
