from tkinter import *
from SignatureValid import SignatureValid_GUI as sn

def MainInterface():
    root = Tk()
    root.title("Quản lý thông tin khách hàng")
    root.geometry("2000x700")
    
    # Create frame feature
    frameFeature = Frame(root)
    frameFeature.grid(row=0, column=0, padx = 20, pady = 20, sticky=N)
    
    # Create title for frame feature
    title = Label(frameFeature, text="Chức năng", font=("Arial", 15))
    title.grid(row=0, column=0, columnspan=2, pady = 2)
    
    # Create feature button
    customerManageBtn = Button(frameFeature, text="Quản lý khách hàng", font=10)
    customerManageBtn.grid(row=1, column=0, pady = 2, sticky=W)
    
    employeeManageBtn = Button(frameFeature, text="Quản lý nhân viên", font=10)
    employeeManageBtn.grid(row=2, column=0, pady = 2, sticky=W)
    
    transactionBtn = Button(frameFeature, text="Giao dịch", font=10)
    transactionBtn.grid(row=3, column=0, pady = 2, sticky=W)
    
    # Create frame to perform feature
    framePerform = Frame(root, highlightbackground='black', highlightthickness=1)
    framePerform.grid(row=0, column=1, padx = 20, pady = 20)
    
    # Add click event for customerManageBtn
    def customerManageBtnHandle():
        pass

    customerManageBtn.config(command=lambda: customerManageBtnHandle())
    
    # Add click event for employeeManageBtn
    def employeeManageBtnHandle():
        pass

    employeeManageBtn.config(command=lambda: employeeManageBtnHandle())
    
    # Add click event for transactionBtn
    def transactionBtnHandle():
        sn.SignatureValid_GUI('KH01', framePerform)

    transactionBtn.config(command=lambda: transactionBtnHandle())
    
    root.mainloop()