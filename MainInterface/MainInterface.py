from tkinter import *
from SignatureValid import SignatureValid_GUI as sn
from Employee import Employee as emp
from Employee import EmployeeAccount as empacc
from Customer import Manager
from Transaction import bang

def MainInterface(accId, permission, parentForm):
    parentForm.withdraw()
    
    
    root = Tk()
    root.title("Quản lý thông tin khách hàng")
    root.geometry("500x500")
    
    def on_closing():
        parentForm.deiconify()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Create frame feature
    frameFeature = Frame(root)
    frameFeature.grid(row=0, column=0, padx = 20, pady = 20, sticky=N)
    
    # Create title for frame feature
    title = Label(frameFeature, text="Chức năng", font=("Arial", 15))
    title.grid(row=0, column=0, columnspan=2, pady = 2)
    
    # Create feature button
    customerManageBtn = Button(frameFeature, text="Quản lý khách hàng", font=10)
    customerManageBtn.grid(row=1, column=0, pady = 2, sticky=W)
    
    if (permission == 'admin'):
        employeeManageBtn = Button(frameFeature, text="Quản lý nhân viên", font=10)
        employeeManageBtn.grid(row=2, column=0, pady = 2, sticky=W)
        
        employeeAccBtn = Button(frameFeature, text="Quản lý tài khoản nhân viên", font=10)
        employeeAccBtn.grid(row=3, column=0, pady = 2, sticky=W)
        
        # Add click event for employeeManageBtn
        employeeManageBtn.config(command=lambda: emp.Employee(root))
        
        # Add click event for employeeAccBtn
        employeeAccBtn.config(command=lambda: empacc.EmployeeAccount(root))
    
    transactionBtn = Button(frameFeature, text="Giao dịch", font=10)
    transactionBtn.grid(row=4, column=0, pady = 2, sticky=W)
    
    # Create frame to perform feature
    framePerform = Frame(root, highlightbackground='black', highlightthickness=1)
    framePerform.grid(row=0, column=1, padx = 20, pady = 20)
    
    # Add click event for customerManageBtn
    customerManageBtn.config(command=lambda: Manager.mainframe(accId, permission, root))
    
    # Add click event for transactionBtn
    transactionBtn.config(command=lambda: bang.bangGUI(accId, root))
    
    root.mainloop()