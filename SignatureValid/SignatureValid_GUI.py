import cv2
from skimage.metrics import structural_similarity as ssim
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from SignatureValid import SignatureValid_DAO as snDao

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
def checkSimilarity(window, path1, paths):
    # check if path1 is empty
    if path1.strip() == '':
        messagebox.showerror("Error",
                             "Chưa chọn hình cần xác nhận")
        return
    
    # check if get paths is available
    if paths == -1:
        messagebox.showerror("Error",
                             "Không kết nối được database")
        return
        
    # check paths is empty
    if len(paths) == 0:
        messagebox.showerror("Error",
                             "Khách hàng chưa có chữ ký mẫu")
        return
    
    for path in paths:
        path = path[0]
        
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
    ent.delete(0, END)
    ent.insert(0, txt)

# Main#############################################################################
def SignatureValid_GUI(CustomerId):
    root = Tk()
    root.title("Xác nhận chữ ký")
    root.geometry("800x300")

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
    
    # get data from customer then show it to entry
    customerInfo = snDao.getCustomerById(CustomerId)
    
    if customerInfo == -1:
        messagebox.showerror("Error",
                             "Không kết nối được database")
    # if customer is not existed
    elif customerInfo == None:
        Na = 'N/A'
        cusIdTxt.config(text = Na)
        cusNameTxt.config(text = Na)
        cusBdTxt.config(text = Na)
        cusAddTxt.config(text = Na)
        cusPhoneTxt.config(text = Na)
        cusSexTxt.config(text = Na)
    else:
        cusIdTxt.config(text = customerInfo[0])
        cusNameTxt.config(text = customerInfo[1])
        cusBdTxt.config(text = customerInfo[2])
        cusAddTxt.config(text = customerInfo[3])
        cusPhoneTxt.config(text = customerInfo[4])
        cusSexTxt.config(text = customerInfo[5])
# End Frame Thong Tin Chung
    
# Frame Xac Nhan Chu Ky
    # Create frame xac nhan chu ky
    frameChuKy = Frame(root)
    frameChuKy.grid(row=0, column=1, padx = 40, pady = 20)
    
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
    
    # Get customer's signature image paths
    paths = snDao.getImgPathById(CustomerId)

    # Create check signature button
    compare_button = Button(
        frameChuKy, text="Kiểm tra", font=10, command=lambda: checkSimilarity(window=root,
                                                                       path1=imageEntry.get(),
                                                                       paths=paths))
    compare_button.grid(row=2, column=0, columnspan=2, pady = 2)
    
    # Add empty rows
    label2 = Label(frameChuKy, text="", font=10)
    label2.grid(row=3, column=0, pady = 2)
    
    label3 = Label(frameChuKy, text="", font=10)
    label3.grid(row=4, column=0, pady = 2)
    
    label4 = Label(frameChuKy, text="", font=10)
    label4.grid(row=5, column=0, pady = 2)
    # End Add empty rows
# End Frame Xac Nhan Chu Ky
    
    root.mainloop()
    