import cv2
from skimage.metrics import structural_similarity as ssim
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from SignatureValid import SignatureValid_DAO as snDao
import os
import shutil
import numpy as np

class SignatureValid:
    def __init__(self):
        self.matchValueLs = []
        
    def Gui(self, CustomerId, parentForm, deposit_button, transfer_button, withdraw_button):
        self.matchValueLs = []
        
        def average(lst):
            return sum(lst) / len(lst)

        # Mach Threshold
        THRESHOLD = 85

        # Matching signature
        def match(path1, path2):
            # read the images
            img1 = cv2.imread(path1)
            img2 = cv2.imread(path2)
            
            # Convert to HSV format
            hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
            hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

            # Define lower and upper color threshold
            lower = np.array([90, 38, 0])
            upper = np.array([145, 255, 255])

            # Generate mask
            mask1 = cv2.inRange(hsv1, lower, upper)
            mask2 = cv2.inRange(hsv2, lower, upper)

            # Detect signature for img1
            contours, hierarchy = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                x,y,w,h = cv2.boundingRect(cnt)
                if w > 50 and h > 50:
                    imgTemp1 = img1[y:y+h,x:x+w]
                    
            # Detect signature for img2
            contours2, hierarchy2 = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours2:
                x,y,w,h = cv2.boundingRect(cnt)
                if w > 50 and h > 50:
                    imgTemp2 = img2[y:y+h,x:x+w]

            # Create new image
            signature1 = np.zeros((512,512,3), np.uint8)
            signature2 = np.zeros((512,512,3), np.uint8)

            # Copy signature to new image
            signature1[100:100+imgTemp1.shape[0], 100:100+imgTemp1.shape[1]] = imgTemp1
            signature2[100:100+imgTemp2.shape[0], 100:100+imgTemp2.shape[1]] = imgTemp2
            
            # turn images to grayscale
            signature1 = cv2.cvtColor(signature1, cv2.COLOR_BGR2GRAY)
            signature2 = cv2.cvtColor(signature2, cv2.COLOR_BGR2GRAY)
            
            # resize images for comparison
            # signature1 = cv2.resize(signature1, (300, 300))
            # signature2 = cv2.resize(signature2, (300, 300))
            
            similarity_value = "{:.2f}".format(ssim(signature1, signature2)*100)
            
            return (float(similarity_value), signature1, signature2)

        # Check similarity
        def checkSimilarity(path1, treeview):
            self.matchValueLs = []
            
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
                    matchValue, signature1, signature2 = match(path1, path)
                    self.matchValueLs.append(matchValue)
                except Exception:
                    messagebox.showerror("Error",
                                         "Không đọc được chữ ký mẫu. Xin kiểm tra lại đường dẫn của khách hàng")
                    return
                
                # read the images
                # img1 = cv2.imread(path1)
                # img2 = cv2.imread(path)
                # img1 = cv2.resize(img1, (300, 300))
                # img2 = cv2.resize(img2, (300, 300))
                
                # turn images to color
                signature1 = cv2.cvtColor(signature1, cv2.COLOR_GRAY2BGR)
                signature2 = cv2.cvtColor(signature2, cv2.COLOR_GRAY2BGR)
                
                textPosition = (10, 50)
                
                if matchValue >= THRESHOLD:
                    # green color
                    color = (0,255,0)
                    # write checking value on image
                    cv2.putText(signature2, f'Matched: {matchValue}', textPosition, cv2.FONT_HERSHEY_SIMPLEX, 
                                1, color, 2, cv2.LINE_AA)
                else:
                    # red color
                    color = (0,0,255)
                    # write checking value on image
                    cv2.putText(signature2, f'Matched: {matchValue}', textPosition, cv2.FONT_HERSHEY_SIMPLEX, 
                                1, color, 2, cv2.LINE_AA)
                    
                # display both images
                # cv2.imshow("Hinh can kiem tra da duoc nhan dang", signature1)
                # cv2.imshow("Hinh goc da duoc nhan dang", signature2)
                cv2.imshow("Hinh can kiem tra", signature1)
                cv2.imshow("Hinh goc", signature2)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        # Browse file function
        def browsefunc(ent):
            filename = askopenfilename(filetypes=([
                ("image", ".jpeg"),
                ("image", ".png"),
                ("image", ".jpg"),
            ]))
            setTextEnt(ent, filename)        

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
        parentForm.withdraw()
        root = Tk()
        
        def on_closing():
            try:
                if (average(self.matchValueLs) >= THRESHOLD):
                    deposit_button.config(state="normal")
                    transfer_button.config(state="normal")
                    withdraw_button.config(state="normal")
                else:
                    deposit_button.config(state="disabled")
                    transfer_button.config(state="disabled")
                    withdraw_button.config(state="disabled")
            except Exception:
                deposit_button.config(state="disabled")
                transfer_button.config(state="disabled")
                withdraw_button.config(state="disabled")
            finally:
                parentForm.deiconify()
                root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

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
            # Get how many file then increment to have a file name and then create destination for copy
            numFiles = len(os.listdir(cusPathTxt.cget("text")))
            desFile = f'{cusPathTxt.cget("text")}/{numFiles + 1}.{srcFile.split(".")[-1]}'
            
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
        root.mainloop()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    