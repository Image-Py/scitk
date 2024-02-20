# import wx, wx.lib.agw.aui as aui
from .mcanvas import MCanvas
from ..widgets import ToolBar, MenuBar, ParaDialog
from sciapp import App

import tkinter as tk
import ttkbootstrap as ttk

class CanvasFrame(ttk.Toplevel): # 继承自 tk.Tk 而不是 tk.Frame
    def __init__(self, parent, autofit=False):
        super().__init__(parent)
        self.title('CanvasFrame')
        self.geometry('800x600') # 设置窗口大小
        
        self.canvas = MCanvas(self, autofit=autofit)
        self.canvas.pack(fill='both', expand=True)

        ttk.Separator(self).pack(side='top', fill='x')
        self.status = ttk.Label(self, anchor="e")
        self.status.pack(side='bottom', fill='x')
        
        self.set_rg = self.canvas.set_rg
        self.set_lut = self.canvas.set_rg
        self.set_log = self.canvas.set_log
        self.set_mode = self.canvas.set_mode
        self.set_tool = self.canvas.set_tool
        self.set_imgs = self.canvas.set_imgs
        self.set_img = self.canvas.set_img
        self.set_cn = self.canvas.set_cn
        
        # self.bind('<Idle>', self.on_idle)
        self.bind('<Activate>', self.on_valid)
        # self.protocol("WM_DELETE_WINDOW", self.on_close) # 在TKinter中处理窗口关闭事件
        self.after(100, self.idle_loop)

    def get_img(self): return self.canvas.image
    
    def idle_loop(self):
        self.on_idle(self)
        self.after(100, self.idle_loop)
        
    def on_idle(self, event):
        if self.title() != self.canvas.image.title:
            self.title(self.canvas.image.title)
    
    def set_title(self, ips):
        self.title(ips.title)
    
    def on_close(self, event):
        # Close event handling
        pass

    def on_valid(self, event):
        print('valid')
        
    def add_toolbar(self):
        toolbar = ToolBar(self)
        toolbar.pack(side="top", fill="x", befor=self.canvas)
        return toolbar

    def add_menubar(self):
        menubar = MenuBar(self)
        self.configure(menu=menubar)
        return menubar

    def info(self, info):
        self.status.config(text=info)
    
    def show_para(self, title, para, view, on_handle=None, on_ok=None, on_cancel=None, preview=False, modal=True):
        dialog = ParaDialog(self, title)
        dialog.init_view(view, para, preview, modal=modal, app=self)
        dialog.bind('cancel', on_cancel)
        dialog.bind('parameter', on_handle)
        dialog.bind('commit', on_ok)
        return dialog.show()

class CanvasNoteBook(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.after(100, self.idle_loop)

    def idle_loop(self):
        self.on_idle(self)
        self.after(100, self.idle_loop)
        
    def on_idle(self, event):
        for i in range(self.index('end')):
            title = self.nametowidget(self.tabs()[i]).image.title
            if self.tab(i, "text") != title:
                self.tab(i, text=title)

    def canvas(self, i=None):
        if i is not None:
            return self.nametowidget(self.tabs()[i])
        else:
            return self.nametowidget(self.select())

    def set_background(self, img):
        self.configure(style='TNotebook', s='lefttab.TNotebook')
  
    def add_canvas(self, mcanvas=None):
        if mcanvas is None:
            mcanvas = MCanvas(self)
            mcanvas.pack(side='top', fill='both', expand=True)
        self.add(mcanvas, text='Image')
        return mcanvas

    def set_title(self, panel, title):
        i = self.index(panel)
        self.tab(i, text=title)

    def on_valid(self): 
        pass

    def on_close(self):
        pass

class CanvasNoteFrame(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('CanvasNoteFrame')
        self.geometry('800x600')

        self.notebook = CanvasNoteBook(self)
        self.canvas = self.notebook.canvas()

        self.notebook.pack(fill="both", expand=True)
        self.add_canvas = self.notebook.add_canvas

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_toolbar(self):
        toolbar = ToolBar(self)
        toolbar.pack(fill="x")
        return toolbar

    def add_menubar(self):
        menubar = MenuBar(self)
        self.config(menu=menubar)
        return menubar

    def on_close(self):
        self.destroy()

if __name__=='__main__':
    from skimage.data import camera, astronaut
    from skimage.io import imread

    
    app = wx.App()
    cf = CanvasFrame(None, autofit=False)
    cf.set_imgs([astronaut(), 255-astronaut()])
    cf.set_cn(0)
    cf.Show()
    app.MainLoop()
    
    '''
    app = wx.App()
    cnf = CanvasNoteFrame(None)
    canvas = cnf.add_img()
    canvas.set_img(camera())

    canvas = cnf.add_img()
    canvas.set_img(camera())
    canvas.set_cn(0)
    
    cnf.Show()
    app.MainLoop()
    '''
