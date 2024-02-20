import numpy as np
import tkinter as tk
import ttkbootstrap as ttk
# from tkinter import ttk
from numpy import ndarray
from .canvas import Canvas
from sciapp.object.image import Image
from sciapp.action import Tool, ImageTool, ShapeTool

class ICanvas(Canvas):
    def __init__(self, parent, autofit=False, within=False, ingrade=False, up=False):
        Canvas.__init__(self, parent, autofit, within, ingrade, up)
        self.images.append(Image())
        #self.images[0].back = Image()
        #self.Bind(wx.EVT_IDLE, self.on_idle)
        #self.idle_loop()

    def get_obj_tol(self):
        return self.image, ImageTool.default
        
    def set_img(self, img, b=False):
        isarr = isinstance(img, ndarray)
        if b and not isarr: self.images[0].back = img
        if not b and not isarr: self.images[0] = img
        if b and isarr: self.images[0].back = Image([img])
        if not b and isarr: self.images[0].img = img
        if not b: self.images[0].reset()
        if b and self.images[0].back: 
            self.images[0].back.reset()
        self.update_box()
        self.update()

    def set_log(self, log, b=False):
        if b: self.back.log = log
        else: self.image.log = log
        
    def set_rg(self, rg, b=False):
        if b: self.back.rg = rg
        else: self.image.rg = rg
        
    def set_lut(self, lut, b=False):
        if b: self.back.lut = lut
        else: self.image.lut = lut

    def set_cn(self, cn, b=False):
        if b: self.back.cn = cn
        else: self.image.cn = cn

    def set_mode(self, mode):
        self.image.mode = mode

    def set_tool(self, tool):
        self.image.tool = self.tool = tool

    @property
    def image(self): return self.images[0]

    @property
    def name(self): return self.image.title

    @property
    def back(self): return self.images[0].back

    def draw_ruler(self, dc, f, **key):
        dc.SetPen(wx.Pen((255,255,255), width=2, style=wx.SOLID))
        conbox, winbox, oribox = key['conbox'], key['winbox'], key['oribox']
        x1 = max(conbox[0], winbox[0])+5
        x2 = min(conbox[2], winbox[2])-5
        pixs = (x2-x1+10)*(oribox[2]-oribox[0])/10.0/(conbox[2]-conbox[0])
        h = min(conbox[3], winbox[3])-5
        dc.DrawLineList([(x1,h,x2,h)])
        dc.DrawLineList([(i,h,i,h-5) for i in np.linspace(x1, x2, 11)])
        dc.SetTextForeground((255,255,255))
        k, unit = self.image.unit
        text = 'Unit = %.1f %s'%(k*pixs, unit)
        dw, dh = dc.GetTextExtent(text)
        dc.DrawText(text, (x2-dw, h-10-dh))

    def on_idle(self, event):
        if self.image.unit == (1, 'pix'):
            if 'unit' in self.marks: del self.marks['unit']
        else: self.marks['unit'] = self.draw_ruler
        if self.image.roi is None:
            if 'roi' in self.marks: del self.marks['roi']
        else: self.marks['roi'] = self.image.roi
        if self.image.mark is None:
            if 'mark' in self.marks: del self.marks['mark']
        elif self.image.mark.dtype=='layers':
            if self.image.cur in self.image.mark.body:
                self.marks['mark'] = self.image.mark.body[self.image.cur]
            elif 'mark' in self.marks: del self.marks['mark']
        else: self.marks['mark'] = self.image.mark
        self.tool = self.image.tool
        Canvas.on_idle(self, event)

class VCanvas(Canvas):
    def __init__(self, parent, autofit=False, within=False, ingrade=True, up=True):
        Canvas.__init__(self, parent, autofit, within, ingrade, up)

    def get_obj_tol(self):
        return self.shape, ShapeTool.default

    def set_shp(self, shp):
        self.marks['shape'] = shp
        self.update()

    def set_tool(self, tool): self.tool = tool

    @property
    def shape(self): 
        if not 'shape' in self.marks: return None
        return self.marks['shape']


class SCanvas(ttk.Frame):
    def __init__(self, parent, autofit=False):
        super().__init__(parent)
        
        self.lab_info = ttk.Label(self, text="information", background="white")
        self.lab_info.pack(side="top", fill="x", padx=0, pady=0)
        
        self.canvas = VCanvas(self, autofit=autofit)
        self.canvas.pack(side="top", fill="both", expand=True)
        
        self.set_shp = self.canvas.set_shp

        self.after(100, self.idle_loop)

    def idle_loop(self):
        self.on_idle()
        self.after(100, self.idle_loop)
        
    def on_idle(self):
        if self.shape.dirty: self.update()
        self.shape.dirty = False

    def update(self):
        if self.shape is None: return
        self.canvas.update()
        if self.lab_info.cget("text") != self.shape.info:
            self.lab_info.config(text=self.shape.info)

    @property
    def shape(self):
        return self.canvas.shape

    @property
    def name(self):
        return self.canvas.shape.name
        

class Scrollbar(ttk.Scrollbar):
    def __init__(self, parent, span=100, *p, **key):
        ttk.Scrollbar.__init__(self, parent, *p, **key)
        self.config(command=self.onscroll)
        self.bind('<ButtonRelease-1>', lambda e: self.set(self.cur))
        self.span, self.cur = span, 0
        self.command = key.get('command', print)
        self.set(0)

    def set_span(self, lim):
        self.span = lim
        self.set(self.cur)
        
    def set(self, value):
        newv = max(min(value, self.span-1), 0)
        ivalue = int(round(newv))
        changed, self.cur = self.cur!=ivalue, ivalue
        super().set(newv/self.span, (newv+1)/self.span)
        if changed: self.command(self.cur)
        
    def get(self): return self.cur
    
    def onscroll(self, *cmds):
        if cmds[0]=='moveto':
            value = min(max(float(cmds[1]), 0), 1)
            self.set(value * self.span)
        if cmds[0]=='scroll' and cmds[2]=='units':
            self.set(self.cur + (int(cmds[1])>0)*2-1)
        if cmds[0]=='scroll' and cmds[2]=='pages':
            step = max(1, self.span/10)
            self.set(self.cur + int(cmds[1])*step)

class MCanvas(ttk.Frame):
    def __init__(self, parent=None, autofit=False):
        tk.Frame.__init__(self, parent)
        
        self.configure(bg="white")
        
        self.lab_info = ttk.Label(self, text="information", anchor="w")
        self.lab_info.pack(side='top', fill='x', anchor='w')

        ttk.Separator(self).pack(side='top', fill='x')
        
        self.canvas = ICanvas(self, autofit=autofit)
        self.canvas.pack(side='top', expand=True, fill="both")
        
        self.sli_chan = ttk.Scale(self, from_=0, to=100, orient="horizontal",
            command=self.on_scroll )
        self.sli_chan.bind('<ButtonRelease-1>',
            lambda e: self.sli_chan.set(int(round(self.sli_chan.get()))))
        # self.sli_chan.pack(fill="x")
        
        self.sli_page = Scrollbar(self, bootstyle='round', orient="horizontal",
            command=self.on_scroll ) #, from_=0, to=100, orient="horizontal")
        # self.sli_page.pack(fill="x")
        
        # self.sli_page.bind("<Motion>", self.on_scroll)
        # self.sli_chan.bind("<Motion>", self.on_scroll)
        # self.bind("<ButtonRelease-1>", self.on_idle)
        
        self.set_rg = self.canvas.set_rg
        self.set_lut = self.canvas.set_rg
        self.set_log = self.canvas.set_log
        self.set_mode = self.canvas.set_mode
        self.set_tool = self.canvas.set_tool

        self.chans, self.pages, self.cn, self.cur = -1, -1, -1, -1
        self.after(100, self.idle_loop)
        print('start loop')
        
    def set_img(self, img, b=False):
        self.canvas.set_img(img, b)
        self.canvas.update_box()
        self.update()
    
    def set_cn(self, cn, b=False):
        self.canvas.set_cn(cn, b)
        self.update()
    
    @property
    def image(self): return self.canvas.image

    @property
    def back(self): return self.canvas.back

    @property
    def name(self): return self.canvas.image.name

    def set_imgs(self, imgs, b=False):
        if b: self.canvas.back.set_imgs(imgs)
        else: self.canvas.image.set_imgs(imgs)
        self.canvas.update_box()
        self.update()

    def Fit(self):
        wx.Panel.Fit(self)
        self.GetParent().Fit()
        
    def slider(self):
        slices = self.image.slices
        channels = self.image.channels
        
        if channels != self.chans or self.cn != self.image.cn:
            print('set channels')
            if not isinstance(self.image.cn, int) and self.sli_chan.winfo_ismapped():
                self.sli_chan.pack_forget()
            if isinstance(self.image.cn, int) and channels > 1:
                if not self.sli_chan.winfo_ismapped():
                    self.sli_chan.pack(fill="x")
                self.sli_chan.set(self.image.cn)
            self.sli_chan.configure(from_=0, to=channels-1)
            self.chans, self.cn = channels, self.image.cn
        if slices != self.pages or self.image.cur != self.cur:
            print('set slices')
            if slices == 1 and self.sli_page.winfo_ismapped():
                self.sli_page.pack_forget()
            if slices > 1 and not self.sli_page.winfo_ismapped():
                self.sli_page.pack(side='bottom', fill="x")
            self.sli_page.set_span(slices)
            self.sli_page.set(self.image.cur)
            self.pages, self.cur = slices, self.image.cur

    def update(self):
        if self.image.img is None: return
        self.slider()
        if self.lab_info.cget("text") != self.image.info:
            self.lab_info.config(text=self.image.info)
        # self.canvas.update()
        # self.update_idletasks()

    def on_scroll(self, event):
        self.image.cur = int(self.sli_page.get())
        self.image.dirty = True
        
        if isinstance(self.image.cn, int):
            self.image.cn = int(round(self.sli_chan.get()))
        self.canvas.on_idle(event)

    def idle_loop(self):
        self.on_idle(self)
        self.after(100, self.idle_loop)
        
    def on_idle(self, event):
        if self.image.img is None: return
        image = self.image
        info = self.lab_info.cget("text")
        imgs = (image.slices, image.channels, image.cn, image.cur)
        selfs = (self.pages, self.chans, self.cn, self.cur)
        if imgs != selfs or info != self.image.info:
            self.update()

    def __del__(self):
        print('canvas panel del')

if __name__=='__main__':
    from skimage.data import camera, astronaut
    from skimage.io import imread
    
    app = wx.App()
    frame = wx.Frame(None, title='MCanvas')
    mc = MCanvas(frame, autofit=False)
    mc.set_img(astronaut())
    mc.set_cn(0)
    frame.Show()
    app.MainLoop()
