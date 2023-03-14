import cv2
from skimage.metrics import structural_similarity as ssim
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from SignatureValid import SignatureValid_DAO as snDao
import os
import shutil

# Get absolute base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mach Threshold
THRESHOLD = 85

# Matching signature
def match(path1, path2):
    # read the images
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    
    # turn images to grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # resize images for comparison
    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))
    similarity_value = "{:.2f}".format(ssim(img1, img2)*100)
    
    return float(similarity_value)

# Browse file function
def browsefunc(ent):
    filename = askopenfilename(filetypes=([
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ]))
    setTextEnt(ent, filename)

# Check similarity
def checkSimilarity(path1, treeview):
    # check if path1 is empty
    if path1.strip() == '':
        messagebox.showerror("Error",
                             "Chưa chọn hình cần xác nhận")
        return
    
    # Get imgage file from tree view
    fileImg = []
    for record in treeview.get_children():
        fileName = treeview.item(record)['values'][0]
        fileImg.append(fileName)
        
    # check paths is empty
    if len(fileImg) == 0:
        messagebox.showerror("Error",
                             "Khách hàng chưa có chữ ký mẫu")
        return
    
    for path in fileImg:
        
        # Match signature
        try:
            matchValue = match(path1, path)
        except Exception:
            messagebox.showerror("Error",
                                 "Không đọc được chữ ký mẫu. Xin kiểm tra lại đường dẫn của khách hàng")
            return
        
        # read the images
        img1 = cv2.imread(path1)
        img2 = cv2.imread(path)
        img1 = cv2.resize(img1, (300, 300))
        img2 = cv2.resize(img2, (300, 300))
        
        textPosition = (10, 50)
        
        if matchValue >= THRESHOLD:
            # green color
            color = (0,255,0)
            # write checking value on image
            cv2.putText(img2, f'Matched: {matchValue}', textPosition, cv2.FONT_HERSHEY_SIMPLEX, 
                        1, color, 2, cv2.LINE_AA)
        else:
            # red color
            color = (0,0,255)
            # write checking value on image
            cv2.putText(img2, f'Matched: {matchValue}', textPosition, cv2.FONT_HERSHEY_SIMPLEX, 
                        1, color, 2, cv2.LINE_AA)
            
        # display both images
        cv2.imshow("Hinh can kiem tra", img1)
        cv2.imshow("Hinh goc", img2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        

# Set text entry
def setTextEnt(ent, txt):
    ent.delete(0, 'end')
    ent.insert(0, txt)

# Load data from DB to tree view
def loadTreeView(SignaturePath, treeview):
    # Get file in customer signature folder
    fileImg = []
    for root, dirs, files in os.walk(SignaturePath):
        for file in files:
            if file.endswith('png') or file.endswith('jpg') or file.endswith('jpeg'):
                fileImg.append(f'{SignaturePath}/{file}')
                
    # Show files on tree view
    for item in fileImg:
        treeview.insert('', 'end', value=item)

# Remove all tree view
def rmAllTreeView(treeview):
    for record in treeview.get_children():
        treeview.delete(record)
    
# Main#############################################################################
def SignatureValid_GUI(CustomerId, root):

    # get data from customer
    customerInfo = snDao.getCustomerById(CustomerId)
    
    if customerInfo == -1:
        print("Không kết được database")
        return
    if customerInfo == None:
        print("Khách hàng không tồn tại")
        return

# Frame Thong Tin Chung
    # Create frame thong tin chung
    frameTTChung = Frame(root)
    frameTTChung.grid(row=0, column=0, padx = 20, pady = 20)
    
    # Title thong tin chung
    ttChungLb = Label(frameTTChung, text="Thông tin chung", font=("Arial", 15))
    ttChungLb.grid(row=0, column=0, columnspan=2, pady = 2)
    
    # Input for customer id
    cusIdLb = Label(frameTTChung, text="Khách hàng Id:", font=10)
    cusIdTxt = Label(frameTTChung, text="Khách hàng Id:", font=10)
    cusIdLb.grid(row=1, column=0, sticky=W, pady = 2)
    cusIdTxt.grid(row=1, column=1, sticky=W, pady = 2)
    
    # Input for customer name
    cusNameLb = Label(frameTTChung, text="Tên khách hàng:", font=10)
    cusNameTxt = Label(frameTTChung, text="Tên khách hàng:", font=10)
    cusNameLb.grid(row=2, column=0, sticky=W, pady = 2)
    cusNameTxt.grid(row=2, column=1, sticky=W, pady = 2)
    
    # Input for customer birthday
    cusBdLb = Label(frameTTChung, text="Ngày sinh:", font=10)
    cusBdTxt = Label(frameTTChung, text="Ngày sinh:", font=10)
    cusBdLb.grid(row=3, column=0, sticky=W, pady = 2)
    cusBdTxt.grid(row=3, column=1, sticky=W, pady = 2)
    
    # Input for customer address
    cusAddLb = Label(frameTTChung, text="Địa chỉ:", font=10)
    cusAddTxt = Label(frameTTChung, text="Địa chỉ:", font=10)
    cusAddLb.grid(row=4, column=0, sticky=W, pady = 2)
    cusAddTxt.grid(row=4, column=1, sticky=W, pady = 2)
    
    # Input for customer phone
    cusPhoneLb = Label(frameTTChung, text="Điện thoại:", font=10)
    cusPhoneTxt = Label(frameTTChung, text="Điện thoại:", font=10)
    cusPhoneLb.grid(row=5, column=0, sticky=W, pady = 2)
    cusPhoneTxt.grid(row=5, column=1, sticky=W, pady = 2)
    
    # Input for customer sex
    cusSexLb = Label(frameTTChung, text="Giới tính:", font=10)
    cusSexTxt = Label(frameTTChung, text="Giới tính:", font=10)
    cusSexLb.grid(row=6, column=0, sticky=W, pady = 2)
    cusSexTxt.grid(row=6, column=1, sticky=W, pady = 2)
    
    # Input for customer signature path
    cusPathLb = Label(frameTTChung, text="Thư mục chữ ký:", font=10)
    cusPathTxt = Label(frameTTChung, text="Thư mục chữ ký:", font=10)
    cusPathLb.grid(row=7, column=0, sticky=W, pady = 2)
    cusPathTxt.grid(row=7, column=1, sticky=W, pady = 2)
    
    # Show data to thong tin chung
    cusIdTxt.config(text = customerInfo[0])
    cusNameTxt.config(text = customerInfo[1])
    cusBdTxt.config(text = customerInfo[2])
    cusAddTxt.config(text = customerInfo[3])
    cusPhoneTxt.config(text = customerInfo[4])
    cusSexTxt.config(text = customerInfo[5])
    cusPathTxt.config(text = customerInfo[6])
        
    # Create folder for signature customer
    if not os.path.exists(cusPathTxt.cget("text")):
        os.mkdir(cusPathTxt.cget("text"))
        messagebox.showinfo("Created",
                            f"Đã tạo thành công thư mục {cusPathTxt.cget('text')}")
        
# End Frame Thong Tin Chung
    
# Frame Xac Nhan Chu Ky
    # Create frame xac nhan chu ky
    frameChuKy = Frame(root)
    frameChuKy.grid(row=0, column=1, padx = 20, pady = 20, sticky=N)
    
    # Create title Xac nhan chu ky
    titleIdLb = Label(frameChuKy, text="Xác nhận chữ ký", font=("Arial", 15))
    titleIdLb.grid(row=0, column=0, columnspan=2, pady = 2)
    
    # Create image entry
    imageEntry = Entry(frameChuKy, font=10)
    imageEntry.grid(row=1, column=0, pady = 2, padx = 2)
    
    # Browse image button
    imageBrowse = Button(
        frameChuKy, text="Browse", font=10, command=lambda : browsefunc(ent=imageEntry))
    imageBrowse.grid(row=1, column=1, pady = 2, padx=5)

    # Create check signature button
    compare_button = Button(frameChuKy, text="Kiểm tra", font=10)
    compare_button.grid(row=2, column=0, columnspan=2, pady = 2)
# End Frame Xac Nhan Chu Ky

# Frame Tree View For Customers' Signature
    frameTreeView = Frame(root)
    frameTreeView.grid(row=1, column=1, padx = 20, pady = 20)
    
    # Title Thêm chữ ký
    modSignLb = Label(frameTreeView, text="Thêm xóa chữ ký", font=("Arial", 15))
    modSignLb.grid(row=0, column=0, columnspan=2, pady = 2)
    
    # Create entry and buttons
    signFileImg = Label(frameTreeView, text="", font=10)
    signFileImg.grid(row=1, column=0, pady = 2)
    frameBtn = Frame(frameTreeView)
    frameBtn.grid(row=1, column=1)
    
    add_button = Button(frameBtn, text="Thêm", font=5)
    add_button.grid(row=0, column=0, pady = 2)
    
    del_button = Button(frameBtn, text="Xóa", font=5)
    del_button.grid(row=0, column=1, pady = 2)
    
    # Create tree view
    tv = ttk.Treeview(frameTreeView, columns=(1,), show="headings", height="5")
    tv.grid(row=2, column=0, pady = 2)
    tv.heading(1, text='Image Path')
    
    # Get customer signature from database show to tree view
    loadTreeView(cusPathTxt.cget("text"), tv)
        
    # Event listener ###################################################
    
    # Tree view select handler
    def treeViewHandler(event):
        for sel in tv.selection():
            fileName = tv.item(sel)['values'][0]
            signFileImg.config(text=fileName)
            
    # Add selection event for tree view
    tv.bind('<<TreeviewSelect>>', treeViewHandler)
    
    # Event listener for add button
    def addCustomerSignature():
        srcFile = askopenfilename(filetypes=([
            ("image", ".jpeg"),
            ("image", ".png"),
            ("image", ".jpg"),
        ]))
        if srcFile == '':
            return
        # Get file name and then create destination for copy
        desFile = f'{cusPathTxt.cget("text")}/{srcFile.split("/")[-1]}'
        
        # Copy file from source to customer's signature folder
        shutil.copyfile(srcFile, desFile)
        messagebox.showinfo("Created",
                            f"Đã thêm thành công {desFile}")
        
        rmAllTreeView(tv)
        loadTreeView(cusPathTxt.cget("text"), tv)
        
    add_button.config(command=lambda: addCustomerSignature())
    
    # Event listener for delete button
    def delCustomerSignature():
        imgFile = signFileImg.cget("text")
        if imgFile == '':
            messagebox.showinfo("Info",
                                "Xin chọn file cần xóa")
            return
        
        # Delete image file
        if os.path.exists(imgFile):
            os.remove(imgFile)
            messagebox.showinfo("Deleted",
                                f"Đã xóa {imgFile}")
        else:
            messagebox.showerror("Error",
                                 "File không tồn tại")
            return
        
        rmAllTreeView(tv)
        loadTreeView(cusPathTxt.cget("text"), tv)
        
    del_button.config(command=lambda: delCustomerSignature())
    
    # Add event listener for check signature button
    compare_button.config(command=lambda: checkSimilarity(imageEntry.get(), tv))
    
    # End Event listener ###################################################
    
# End Frame Tree View For Customers' Signature

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    