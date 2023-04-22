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
from DrawSignature import SignatureCanvas as SC
from TrainModel import Predict as pd

class SignatureValid:
    def __init__(self):
        self.matchValueLs = []
        self.regID = ''
        
    def Gui(self, CustomerId, parentForm, deposit_button, transfer_button, withdraw_button):
        drSign = SC.SignatureCanvas()
        
        self.matchValueLs = []
        self.regID = ''
        
        def average(lst):
            return sum(lst) / len(lst)

        # Mach Threshold
        THRESHOLD = 0.2
        
        def checkSimilarity(path1):
            if path1.strip() == '':
                messagebox.showerror("Error",
                                      "Chưa chọn hình cần xác nhận")
                return
            
            dataset_path = "SignatureImg"
            cusLabel = pd.predictSignature(path1, "TrainModel/signature_model.h5")
            # print(cusLabel)
            
            if (cusLabel == -1):
                self.regID = "N/A"
                messagebox.showerror("Error", "Không nhận diện được chữ ký")
                return
            
            for label, folder in enumerate(os.listdir(dataset_path)):
                # Set the path to the subfolder
                folder_path = os.path.join(dataset_path, folder)

                # Loop over the images in the subfolder
                for filename in os.listdir(folder_path):
                    if cusLabel == label:
                        self.regID = folder
                        
                        if (CustomerId == self.regID):
                            messagebox.showinfo("Xác nhận",
                                            f"Đã nhận diện được chữ ký của {self.regID}")
                        else:
                            messagebox.showerror("Error",
                                            f"Đã nhận diện được chữ ký của {self.regID}")
                        return
        
        # def detect_signature(image_path):
        #     # Load the image
        #     image = cv2.imread(image_path, 0)
        #     image = cv2.resize(image, (200, 200))
        #     return image

        # # Matching signature
        # def match(sig1_path, sig2_path):
        #     # Load the images
        #     template = cv2.imread(sig1_path, 0)
        #     original = cv2.imread(sig2_path, 0)
            
        #     # Resize the images
        #     template = cv2.resize(template, (300, 300))
        #     original = cv2.resize(original, (300, 300))
            
        #     # Create a SIFT detector
        #     sift = cv2.SIFT_create()
            
        #     # Detect and compute keypoints and descriptors
        #     kp1, desc_1 = sift.detectAndCompute(template, None)
        #     kp2, desc_2 = sift.detectAndCompute(original, None)
            
        #     # Create a matcher
        #     matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
        #     matches_1 = matcher.knnMatch(desc_1, desc_2, 2)
            
        #     # Filter matches using the Lowe's ratio test
        #     good_points = []
        #     for m,n in matches_1:
        #         if m.distance < 0.8 * n.distance:
        #             good_points.append(m)
            
        #     # Calculate the ratio of good points to total keypoints
        #     ratio = len(good_points) / len(kp1)

        #     return (ratio, template, original)
        #     # signature1 = detect_signature(sig1_path)
        #     # signature2 = detect_signature(sig2_path)
            
        #     # # Calculate structural similarity index
        #     # value = "{:.5f}".format(ssim(signature1, signature2))
            
        #     # return (float(value), signature1, signature2)

        # # Check similarity
        # def checkSimilarity(path1, treeview):
        #     self.matchValueLs = []
            
        #     # check if path1 is empty
        #     if path1.strip() == '':
        #         messagebox.showerror("Error",
        #                              "Chưa chọn hình cần xác nhận")
        #         return
            
        #     # Get imgage file from tree view
        #     fileImg = []
        #     for record in treeview.get_children():
        #         fileName = treeview.item(record)['values'][0]
        #         fileImg.append(fileName)
                
        #     # check paths is empty
        #     if len(fileImg) == 0:
        #         messagebox.showerror("Error",
        #                              "Khách hàng chưa có chữ ký mẫu")
        #         return
            
        #     for path in fileImg:
                
        #         # Match signature
        #         try:
        #             matchValue, signature1, signature2 = match(path1, path)
        #             self.matchValueLs.append(matchValue)
        #         except Exception as e:
        #             messagebox.showerror("Error",
        #                                  f"{e}")
        #             return
                
        #         # read the images
        #         # img1 = cv2.imread(path1)
        #         # img2 = cv2.imread(path)
        #         # img1 = cv2.resize(img1, (300, 300))
        #         # img2 = cv2.resize(img2, (300, 300))
                
        #         # turn images to color
        #         signature1 = cv2.cvtColor(signature1, cv2.COLOR_GRAY2BGR)
        #         signature2 = cv2.cvtColor(signature2, cv2.COLOR_GRAY2BGR)
                
        #         textPosition = (0, 50)
                
        #         if matchValue > THRESHOLD:
        #             # green color
        #             color = (0,255,0)
        #             # write checking value on image
        #             cv2.putText(signature2, f'{matchValue}', textPosition, cv2.FONT_HERSHEY_SIMPLEX, 
        #                         1, color, 2, cv2.LINE_AA)
        #         else:
        #             # red color
        #             color = (0,0,255)
        #             # write checking value on image
        #             cv2.putText(signature2, f'{matchValue}', textPosition, cv2.FONT_HERSHEY_SIMPLEX, 
        #                         1, color, 2, cv2.LINE_AA)
                    
        #         # display both images
        #         # cv2.imshow("Hinh can kiem tra da duoc nhan dang", signature1)
        #         # cv2.imshow("Hinh goc da duoc nhan dang", signature2)
        #         cv2.imshow("Hinh can kiem tra", signature1)
        #         cv2.imshow("Hinh goc", signature2)
        #         cv2.waitKey(0)
        #         cv2.destroyAllWindows()

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
                if (self.regID == CustomerId):
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
        
        # Get signature button
        getSignatureBtn = Button(
            frameChuKy, text="Ký trực tiếp", font=10, command=lambda : getSignatureBtnHandler(imageEntry, root))
        getSignatureBtn.grid(row=1, column=2, pady = 2, padx=5)

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
        
        addDirect_button = Button(frameBtn, text="Thêm trực tiếp", font=5)
        addDirect_button.grid(row=0, column=1, pady = 2)
        
        del_button = Button(frameBtn, text="Xóa", font=5)
        del_button.grid(row=0, column=2, pady = 2)
        
        # Create tree view
        tv = ttk.Treeview(frameTreeView, columns=(1,), show="headings", height="5")
        tv.grid(row=2, column=0, pady = 2)
        tv.heading(1, text='Image Path')
        
        # Get customer signature from database show to tree view
        loadTreeView(cusPathTxt.cget("text"), tv)
            
        # Event listener ###################################################
        
        # Ky truc tiep su kien
        def getSignatureBtnHandler(ent, root):
            setTextEnt(ent, 'DrawSignature/temp.png')
            drSign.CaptureSignature('DrawSignature/temp.png', root)
            
        # Them chu ky truc tiep su kien
        def addCustomerSignatureDirectly():
            # Get how many file then increment to have a file name and then create destination for copy
            numFiles = len(os.listdir(cusPathTxt.cget("text")))
            desFile = f'{cusPathTxt.cget("text")}/{numFiles + 1}.png'
            drSign.CaptureSignature(desFile, root, tv)
            
        addDirect_button.config(command=lambda: addCustomerSignatureDirectly())
        
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
        compare_button.config(command=lambda: checkSimilarity(imageEntry.get()))
        
        # End Event listener ###################################################
        
    # End Frame Tree View For Customers' Signature
        root.mainloop()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    