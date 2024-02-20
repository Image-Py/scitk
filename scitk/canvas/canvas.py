import numpy as np
import tkinter as tk
from sciapp.util.imgutil import mix_img, cross, multiply, merge, lay, mat, like
from scitk.canvas.mark import drawmark
from sciapp.object import Image, Shape, mark2shp, Layer, json2shp
from sciapp.action import Tool, ImageTool, ShapeTool
from time import time

class Canvas (tk.Canvas):
    scales = [0.03125, 0.0625, 0.125, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 8, 10, 15, 20, 30, 50]
    
    def __init__(self, parent, autofit=False, within=False, ingrade=False, up=False):
        tk.Canvas.__init__ ( self, parent)

        self.winbox = None
        self.within = within
        self.conbox = [0,0,1,1]
        self.oribox = [0,0,1,1]
        
        self.outbak = None
        self.outimg = None
        self.outrgb = None
        self.outbmp = None
        self.outint = None
        self.buffer = None

        self.first = True

        self.images = []
        self.marks = {}
        self.tool = None
        
        self.scaidx = 6
        self.autofit = autofit
        self.ingrade = ingrade
        self.up = up
        self.scrbox = (self.winfo_screenwidth(),
                       self.winfo_screenheight())
        self.bindEvents()
        self.after(100, self.idle_loop)

    def get_obj_tol(self): return self, Tool.default

    def bindEvents(self):
        self.bind("<Configure>", self.on_size)
        mouse_evts = ['<Button-1>', '<Button-2>', '<Button-3>', '<Motion>', '<MouseWheel>',
                     '<ButtonRelease-1>', '<ButtonRelease-2>', '<ButtonRelease-3>']
        for evt in mouse_evts: self.bind(evt, self.on_mouse)

    def on_mouse(self, me):
        # print(bin(me.state), me.num)
        px, py = me.x, me.y
        x, y = self.to_data_coor(px, py)
        obj, tol = self.get_obj_tol()
        btn, tool = me.num, self.tool or tol
        ld, rd, md = me.state&0x100>0, me.state&0x200>0, me.state&0x400>0
        # print(ld, rd, md)
        sta = [me.state&0x20000>0, me.state&0x0004>0, me.state&0x0001>0]
        others = {'alt':sta[0], 'ctrl':sta[1],
            'shift':sta[2], 'px':px, 'py':py, 'canvas':self}
        if me.num=='??' and not (ld or md or rd): 
            for i in (ImageTool, ShapeTool):
                if isinstance(tool, i):
                    i.mouse_move(tool, obj, x, y, btn, **others)
        if (ld+rd+md)==0 and btn!='??':
            tool.mouse_down(obj, x, y, btn, **others)
        if (ld+rd+md)>0 and btn!='??':
            tool.mouse_up(obj, x, y, btn, **others)
        if btn == '??':
            tool.mouse_move(obj, x, y, btn, **others)

        wheel = np.sign(me.delta)
        
        if wheel!=0:
            tool.mouse_wheel(obj, x, y, wheel, **others)
        ckey = {'arrow':'arrow','cross':'cross','hand':'hand2'}
        self.configure(cursor=ckey[tool.cursor])
            
    def initBuffer(self):
        box = self.winfo_width(), self.winfo_height()
        self.buffer = []
        self.winbox = [0, 0, *box]
        lay(self.winbox, self.conbox)

    def fit(self):
        self.update_box()
        oriw = self.oribox[2]-self.oribox[0]
        orih = self.oribox[3]-self.oribox[1]
        if not self.autofit: a,b,c,d = self.winbox
        else: 
            (a,b),(c,d) = (0,0), self.scrbox
            c, d = c*0.9, d*0.9
        if not self.ingrade:
            for i in self.scales[6::-1]:
                if oriw*i<c-a and orih*i<d-b: break
            self.scaidx = self.scales.index(i)
        else: i = min((c-a)*0.9/oriw, (d-b)*0.9/orih)
        self.zoom(i, 0, 0)
        lay(self.winbox, self.conbox)
        self.update()

    def update_box(self):
        box = [1e10, 1e10, -1e10, -1e10]
        for i in self.images: box = merge(box, i.box)
        shapes = [i for i in self.marks.values() if isinstance(i, Shape)]
        shapes = [i for i in shapes if not i.box is None]
        for i in shapes: box = merge(box, i.box)
        if box[2]<=box[0]: box[0], box[2] = box[0]-1e-3, box[2]+1e-3
        if box[1]<=box[3]: box[1], box[3] = box[1]-1e-3, box[3]+1e-3
        if self.winbox and self.oribox == box: return
        self.conbox = self.oribox = box

    def draw_image(self, dc, img, back, mode):
        out, bak, rgb = self.outimg, self.outbak, self.outrgb
        ori, cont = self.oribox, self.conbox
        cellbox = like(ori, cont, img.box)
        csbox = cross(self.winbox, cellbox)
        
        if min(csbox[2]-csbox[0], csbox[3]-csbox[1])<5: return
        shp = csbox[3]-csbox[1], csbox[2]-csbox[0]
        o, m = mat(self.oribox, self.conbox, cellbox, csbox)
        shp = tuple(np.array(shp).round().astype(np.int32))
        if out is None or (out.shape, out.dtype) != (shp, img.dtype):
            self.outimg = np.zeros(shp, dtype=img.dtype)
        if not back is None and not back.img is None and (
            bak is None or (bak.shape, bak.dtype) != (shp, back.dtype)):
            self.outbak = np.zeros(shp, dtype=back.dtype)
        if rgb is None or rgb.shape[:2] != shp:
            self.outrgb = np.zeros(shp+(3,), dtype=np.uint8)
            self.outint = np.zeros(shp, dtype=np.uint8)
            buf = memoryview(self.outrgb)
            # self.outbmp = wx.Bitmap.FromBuffer(*shp[::-1], buf)
        if not back is None:
            mix_img(back.imgs[img.cur], m, o, shp, self.outbak, 
                self.outrgb, self.outint, back.rg, back.lut,
                back.log, cns=back.cn, mode='set')
        mix_img(img.img, m, o, shp, self.outimg,
            self.outrgb, self.outint, img.rg, img.lut,
            img.log, cns=img.cn, mode=img.mode)
        
        # self.outbmp.CopyFromBuffer(memoryview(self.outrgb))
        # dc.DrawBitmap(self.outbmp, int(csbox[0]), int(csbox[1]))

        # image = ImageTk.PhotoImage(PILImage.fromarray(self.outrgb))
        height, width = self.outrgb.shape[:2]
        data = f'P6 {width} {height} 255 '.encode() + self.outrgb.tobytes()
        image = tk.PhotoImage(width=width, height=height, data=data, format='PPM')

        self.buffer.append(image)
        dc.create_image(int(csbox[0]), int(csbox[1]), image=image, anchor=tk.NW)

        
    def update(self, counter = [0,0]):
        #self.update_box()
        #if self.conbox[2] - self.conbox[0]>1: self.update_box()

        if None in [self.winbox, self.conbox]: return
        if self.within :lay(self.winbox, self.conbox)
        
        if self.first and self.conbox[2] - self.conbox[0]>1:
            self.first = False
            return self.fit()
        
        counter[0] += 1
        start = time()
        # lay(self.winbox, self.conbox)
        dc = self # wx.BufferedDC(wx.ClientDC(self), self.buffer)
        #dc.SetBackground(wx.Brush((255,255,255)))
        
        self.delete('all') # dc.Clear()
        del self.buffer[:]
        
        for i in self.images: 
            if i.img is None: continue
            self.draw_image(dc, i, i.back, 0)
        
        for i in self.marks.values():
            if i is None: continue
            if callable(i):
                i(dc, self.to_panel_coor, k=self.scale, cur=0,
                    winbox=self.winbox, oribox=self.oribox, conbox=self.conbox)
            else:
                drawmark(dc, self.to_panel_coor, i, k=self.scale, cur=0,
                    winbox=self.winbox, oribox=self.oribox, conbox=self.conbox)
        # dc.UnMask()
        
        
        # print('update')

        counter[1] += time()-start
        if counter[0] == 50:
            print('frame rate:',int(50/max(0.001,counter[1])))
            counter[0] = counter[1] = 0

    def set_tool(self, tool): self.tool = tool

    @property
    def scale(self):
        conw = self.conbox[2]-self.conbox[0]
        oriw = self.oribox[2]-self.oribox[0]
        conh = self.conbox[3]-self.conbox[1]
        orih = self.oribox[3]-self.oribox[1]
        l1, l2 = conw**2+conh**2, oriw**2+orih**2
        return l1**0.5 / l2**0.5

    def move(self, dx, dy, coord='win'):
        if coord=='data':
            dx,dy = dx*self.scale, dy*self.scale
        arr = np.array(self.conbox)
        arr = arr.reshape((2,2))+(dx, dy)
        self.conbox = arr.ravel().tolist()
        self.update()

    def idle_loop(self):
        self.on_idle(self)
        self.after(100, self.idle_loop)

    def on_size(self, event):
        print('size')
        size = self.winfo_width(), self.winfo_height()
        print(size)
        if max(size)>20: # and self.images[0].img is not None:
            self.initBuffer()
        return self.update()
        # if len(self.images)+len(self.marks)==0: return
        # if self.conbox[2] - self.conbox[0] > 1: self.update()

    def on_idle(self, event=None):
        need = sum([i.dirty for i in self.images])
        shapes = [i for i in self.marks.values() if isinstance(i, Shape)]
        need += sum([i.dirty for i in shapes])
        if need==0: return
        else:
            for i in self.images: i.dirty = False
            for i in shapes: i.dirty = False
            self.update()
        
    def center(self, x, y, coord='win'):
        if coord=='data':
            x,y = self.to_panel_coor(x, y)
        dx = (self.winbox[2]-self.winbox[0])/2 - x
        dy = (self.winbox[3]-self.winbox[1])/2 - y
        for i,j in zip((0,1,2,3),(dx,dy,dx,dy)):
            self.conbox[i] += j
        lay(self.winbox, self.conbox)
        
    def zoom(self, k, x, y, coord='win'):
        if coord=='data':
            x,y = self.to_panel_coor(x, y)
            if self.up: y = (self.winbox[3]-self.winbox[1]) - y
        box = np.array(self.conbox).reshape((2,2))
        box = (box - (x,y)) / self.scale * k + (x, y)
        self.conbox = box.ravel().tolist()
        if not self.autofit: return
        a,b,c,d = self.conbox
        if c-a<self.scrbox[0]*0.9 and d-b<self.scrbox[1]*0.9:
            self.config(width=c-a+4, height=d-b+4)
        lay(self.winbox, self.conbox)
        top_level = self.winfo_toplevel()
        self.pack()
        # top_level.geometry('') 
        # op_level.pack()
        
    def zoomout(self, x, y, coord='win', grade=True):
        if not self.ingrade:
            self.scaidx = min(self.scaidx + 1, len(self.scales)-1)
            i = self.scales[self.scaidx]
        else: i = self.scale * 1.5
        self.zoom(i, x, y, coord)
        self.update()

    def zoomin(self, x, y, coord='win'):
        if not self.ingrade:
            self.scaidx = max(self.scaidx - 1, 0)
            i = self.scales[self.scaidx]
        else: i = self.scale / 1.5
        self.zoom(i, x, y, coord)
        self.update()

    def to_data_coor(self, x, y):
        if self.up: y = (self.winbox[3]-self.winbox[1]) - y
        x, y = x / self.scale, y / self.scale
        x += -self.conbox[0]/self.scale+self.oribox[0]
        y += -self.conbox[1]/self.scale+self.oribox[1]
        return x-0.5, y-0.5

    def to_panel_coor(self, x, y):
        x, y = (x+0.5) * self.scale, (y+0.5) * self.scale
        x += -self.oribox[0] * self.scale + self.conbox[0]
        y += -self.oribox[1] * self.scale + self.conbox[1]
        if self.up: y = (self.winbox[3]-self.winbox[1]) - y
        return x, y

    def save_buffer(self, path):
        dcSource = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        # based largely on code posted to wxpython-users by Andrea Gavana 2006-11-08
        size = dcSource.Size

        # Create a Bitmap that will later on hold the screenshot image
        # Note that the Bitmap must have a size big enough to hold the screenshot
        # -1 means using the current default colour depth
        bmp = wx.Bitmap(size.width, size.height)

        # Create a memory DC that will be used for actually taking the screenshot
        memDC = wx.MemoryDC()

        # Tell the memory DC to use our Bitmap
        # all drawing action on the memory DC will go to the Bitmap now
        memDC.SelectObject(bmp)

        # Blit (in this case copy) the actual screen on the memory DC
        # and thus the Bitmap
        memDC.Blit( 0, # Copy to this X coordinate
            0, # Copy to this Y coordinate
            size.width, # Copy this width
            size.height, # Copy this height
            dcSource, # From where do we copy?
            0, # What's the X offset in the original DC?
            0  # What's the Y offset in the original DC?
            )

        # Select the Bitmap out of the memory DC by selecting a new
        # uninitialized Bitmap
        memDC.SelectObject(wx.NullBitmap)

        img = bmp.ConvertToImage()
        img.SaveFile(path, wx.BITMAP_TYPE_PNG)

    def destroy(self):
        # self.img = self.back = None
        print('canvas deleted!')
        super().destroy()

if __name__=='__main__':
    from skimage.data import astronaut, camera
    import matplotlib.pyplot as plt

    app = tk.Tk()
    frame = app; app.title('Canvas')
    canvas = Canvas(frame, autofit=False, ingrade=True, up=False)

    image = Image()
    image.img = camera()
    image.pos = (0,0)
    canvas.images.append(image)
    canvas.pack(fill="both", expand=True)
    app.mainloop()
