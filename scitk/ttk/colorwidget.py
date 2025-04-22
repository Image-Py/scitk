import ttkbootstrap as ttk
from tkinter import colorchooser
from ttkbootstrap.scrolled import ScrolledFrame
import numpy as np
from PIL import Image, ImageTk

def lut2img(lut, w=256, h=10):
    idx = np.linspace(0, 255, w).astype(np.uint8)
    return np.array([lut[idx]] * h)

gray = (np.arange(256*3).reshape(-1,3)//3).astype(np.uint8)

class ColorMapBox(ttk.Frame):
    def __init__( self, parent=None, cmap=[('gray', gray)], bootstyle='primary'):
        super().__init__(parent, bootstyle=bootstyle)
        self.parent = parent
        
        self.lab = ttk.Button(self,  text=cmap[0][0], compound='bottom', image='', padding=-2,
            command=self.drop, bootstyle=bootstyle+'-outline')
        self.lab.pack(side='left')
        
        self.cmap = cmap
        self.set(self.cmap[0][0])
        # ttk.Button(self, text='v', padding=3, bootstyle='dark').pack(side='left', fill='y')

    def set(self, item, call=None):
        self.lut = item
        lut = self.cmap[[i[0] for i in self.cmap].index(item)][1]
        img = Image.fromarray(lut2img(lut, 100, 10))
        self.img = ImageTk.PhotoImage(img)
        self.lab.config(text=item, image=self.img)
        if not call is None: call()
        
    def get(self): return self.lut
        
    def drop(self, imgs={}):
        dialog = ttk.Toplevel(
            title='Color Map',
            transient=self.parent,
            resizable=(False, False),
            topmost=True,
            maxsize=(260, 256),
            #iconify=True,
        )
        sframe = ScrolledFrame(dialog)
        
        ox = self.lab.winfo_rootx()
        oy = self.lab.winfo_rooty()
        oh = self.lab.winfo_height()
        for i, lut in self.cmap:
            img = Image.fromarray(lut2img(lut, 256, 10))
            imgs[i] = ImageTk.PhotoImage(img)
            lab = ttk.Button(sframe, text=i, image=imgs[i], compound='bottom', padding=-2,
                             bootstyle='default-outline',
                             command=lambda item=i:self.set(item, dialog.destroy))
            lab.pack(side='top')
        
        sframe.pack(fill='both', expand=True)
        dialog.geometry('+%d+%d'%(ox-5, oy+oh))
        dialog.grab_set()
        dialog.wait_window()

class ColorBox(ttk.Frame):
    def __init__( self, parent=None, color=(255,255,255), bootstyle='primary'):
        super().__init__(parent, bootstyle=bootstyle)
        self.parent = parent
        
        self.lab = ttk.Button(self,  text='no color', compound='bottom', image='', padding=-2,
            command=self.drop, bootstyle=bootstyle+'-outline')
        self.lab.pack(side='left')
        self.set(color)
        # ttk.Button(self, text='v', padding=3, bootstyle='dark').pack(side='left', fill='y')

    def set(self, color, call=None):
        self.color = color
        rgb = '#%.2x%.2x%.2x'%(color)
        color = np.zeros((10, 60, 3))+color
        img = Image.fromarray(color.astype(np.uint8))
        self.img = ImageTk.PhotoImage(img)
        self.lab.config(text=rgb, image=self.img)
        if not call is None: call()
        
    def get(self): return self.color
        
    def drop(self, imgs={}):
        color = colorchooser.askcolor()
        self.set(color[0])

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    cmap = []
    for i in plt.colormaps()[::-1]:
        cm = plt.get_cmap(i)
        if i[-2:]=='_r': continue
        vs = np.linspace(0, cm.N, 256, endpoint=False)
        lut = cm(vs.astype(np.uint8), bytes=True)[:,:3]
        cmap.append((i, lut))
    
    root = ttk.Window('colormap')
    ColorMapBox(root, cmap).pack()
    root.mainloop()
