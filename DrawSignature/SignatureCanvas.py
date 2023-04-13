from tkinter import *
from PIL import Image, ImageDraw
import os

class SignatureCanvas:
    
    def __init__(self):
        self._mousePressed = False
        self._last = None
        
    def CaptureSignature(self, path, parentForm, treeview=None):
        self._mousePressed = False
        self._last = None
        
        parentForm.withdraw()
        
        tk = Tk()
        
        # Remove all tree view
        def rmAllTreeView(treeview):
            for record in treeview.get_children():
                treeview.delete(record)
        
        # Load data from DB to tree view
        def loadTreeView(treeview):
            SignaturePath = path[:path.rfind('/')]
            # Get file in customer signature folder
            fileImg = []
            for root, dirs, files in os.walk(SignaturePath):
                for file in files:
                    if file.endswith('png') or file.endswith('jpg') or file.endswith('jpeg'):
                        fileImg.append(f'{SignaturePath}/{file}')
                    
            # Show files on tree view
            for item in fileImg:
                treeview.insert('', 'end', value=item)
        
        
        def on_closing():
            parentForm.deiconify()
            tk.destroy()

        tk.protocol("WM_DELETE_WINDOW", on_closing)
        
        cvs = Canvas(tk, width=300, height=300)
        cvs.pack()

        img = Image.new('RGB', (300, 300), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        def press(evt):
            self._mousePressed = True

        def release(evt):
            self._mousePressed = False

        cvs.bind_all('<ButtonPress-1>', press)
        cvs.bind_all('<ButtonRelease-1>', release)

        def finish():
            img.save(path)
            
            # If treeview is not null, load treeview file
            if treeview:
                rmAllTreeView(treeview)
                loadTreeView(treeview)
            parentForm.deiconify()
            tk.destroy()

        Button(tk, text='done', command=finish).pack()

        def move(evt):
            x, y = evt.x, evt.y
            if self._mousePressed:
                if self._last is None:
                    self._last = (x, y)
                    return
                draw.line(((x, y), self._last), (0, 0, 0))
                cvs.create_line(x, y, self._last[0], self._last[1])
                self._last = (x, y)
            else:
                self._last = (x, y)

        cvs.bind_all('<Motion>', move)

        tk.mainloop()