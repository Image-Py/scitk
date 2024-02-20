from .mcanvas import SCanvas
from ..widgets import ToolBar, MenuBar, ParaDialog
from sciapp import App
import tkinter as tk
import ttkbootstrap as ttk

class VectorFrame(ttk.Toplevel):
    def __init__(self, parent, autofit=False):
        super().__init__(parent)
        self.title('CanvasFrame')
        self.geometry('800x600') # 设置窗口大小
        
        self.canvas = SCanvas(self, autofit=autofit)
        self.canvas.pack(fill='both', expand=True)

        ttk.Separator(self).pack(side='top', fill='x')
        self.status = ttk.Label(self, anchor="e")
        self.status.pack(side='bottom', fill='x')
        
        self.set_shp = self.canvas.set_shp
        # self.Bind(wx.EVT_IDLE, self.on_idle)

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


class VectorNoteBook(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.after(100, self.idle_loop)

    def idle_loop(self):
        self.on_idle(self)
        self.after(100, self.idle_loop)
        
    def on_idle(self, event):
        for i in range(self.index('end')):
            name = self.nametowidget(self.tabs()[i]).shape.name
            if self.tab(i, "text") != name:
                self.tab(i, text=name)

    def canvas(self, i=None):
        if i is not None:
            return self.nametowidget(self.tabs()[i])
        else:
            return self.nametowidget(self.select())

    def set_background(self, img):
        self.configure(style='TNotebook', s='lefttab.TNotebook')
  
    def add_canvas(self, scanvas=None):
        if scanvas is None:
            scanvas = SCanvas(self)
            scanvas.pack(side='top', fill='both', expand=True)
        self.add(scanvas, text='Image')
        return scanvas

    def set_title(self, panel, title):
        i = self.index(panel)
        self.tab(i, text=title)

    def on_valid(self): 
        pass

    def on_close(self):
        pass

class VectorNoteFrame(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('CanvasNoteFrame')
        self.geometry('800x600')

        self.notebook = VectorNoteBook(self)
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
