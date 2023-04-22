from tkinter import *
from SignatureValid import SignatureValid_GUI as sn
from Employee import Employee as emp
from Employee import EmployeeAccount as empacc
from Customer import Manager
from Transaction import bang
from TrainModel import CreateNPY as crNPY
from TrainModel import CreateModel as crModel

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
        
        dataBtn = Button(frameFeature, text="Tạo dataset", font=10)
        dataBtn.grid(row=5, column=0, pady = 2, sticky=W)
        
        modelBtn = Button(frameFeature, text="Tạo model", font=10)
        modelBtn.grid(row=6, column=0, pady = 2, sticky=W)
        
        dataBtn.config(command=lambda: crNPY.createNPY())
        modelBtn.config(command=lambda: crModel.CreateModel())
    
    transactionBtn = Button(frameFeature, text="Giao dịch", font=10)
    transactionBtn.grid(row=4, column=0, pady = 2, sticky=W)
    
    # Add click event for customerManageBtn
    customerManageBtn.config(command=lambda: Manager.mainframe(accId, permission, root))
    
    # Add click event for transactionBtn
    transactionBtn.config(command=lambda: bang.bangGUI(accId, root))
    
    root.mainloop()