import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

def make_logo_(obj):
    bmp = None
    if isinstance(obj, str) and len(obj)>1:
        bmp = wx.Bitmap(obj)
    if isinstance(obj, str) and len(obj)==1:
        bmp = wx.Bitmap(16, 16)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush((255,255,255)))
        dc.Clear()
        dc.SetTextForeground((0,0,150))
        font = dc.GetFont()
        font.SetPointSize(12)
        dc.SetFont(font)
        w, h = dc.GetTextExtent(obj)
        dc.DrawText(obj, 8-w//2, 8-h//2)
        rgb = bytes(768)
        dc.SelectObject(wx.NullBitmap)
        bmp.CopyToBuffer(rgb)
        a = memoryview(rgb[::3]).tolist()
        a = bytes([255-i for i in a])
        bmp = wx.Bitmap.FromBufferAndAlpha(16, 16, rgb, a)
    # img = bmp.ConvertToImage()
    # img.Resize((20,20), (2,2))
    # return img.ConvertToBitmap()
    return bmp

class ToolBar(ttk.Frame):
    def __init__(self, parent, orient='x', width=0, *p, **key):
        super().__init__(parent)
        
        self.orient = orient
        self.app = parent
        self.width = width
        self.toolset = []
        self.curbtn = None
        self.add_border()

    def add_border(self):
        ttk.Separator(self).pack(
            side={'x':'bottom', 'y':'right'}[self.orient], fill=self.orient)
        ttk.Separator(self).pack(
            side={'x':'top', 'y':'left'}[self.orient], fill=self.orient)
        
    def on_tool(self, tol):
        print('on tool')
        return tol.start(self.app)
        if self.curbtn:
            self.curbtn.config(background=self.cget("background"))
        self.curbtn = event.widget
        event.widget.config(background="light blue")

    def on_config(self, tol):
        if not hasattr(tol, 'view'):
            return
        self.app.show_para(tol.title, tol.para, tol.view)
        tol.config()

    def on_help(self, tol):
        pass

    def on_info(self, tol):
        if hasattr(self.app, 'info'):
            self.app.info(tol.title)

    def bind(self, btn, tol):
        obj = tol()
        # btn.config(background=self.cget("background"))
        btn.bind("<Button-1>", lambda e, obj=obj: self.on_tool(obj))
        btn.bind("<Button-3>", lambda e, obj=obj: self.on_help(obj))
        btn.bind("<Enter>", lambda e, obj=obj: self.on_info(obj))
        btn.bind("<Double-Button-1>", lambda e, obj=obj: self.on_config(obj))

    def clear(self):
        for child in self.winfo_children():
            child.destroy()
            self.toolset.clear()

    def add_tool(self, logo, tool, imgdic={}):
        side = {'x':'left', 'y':'top'}[self.orient]
        if '.' in logo:
            if not logo in imgdic:
                imgdic[logo] = tk.PhotoImage(file=logo)
            text, img = '', imgdic[logo]
        else: text, img = logo, None
        btn = ttk.Button(self, bootstyle='outline-info',
            width=self.width, text=text, image=img,
            compound='center', padding=5)
        self.bind(btn, tool)
        btn.pack(side=side, padx=2, pady=5)

    def add_tools(self, name, tools, fixed=True, imgdic={}):
        side = {'x':'left', 'y':'top'}[self.orient]
        if not fixed:
            self.toolset.append((name, []))
        for logo, tool in tools:
            if '.' in logo:
                if not logo in imgdic:
                    imgdic[logo] = tk.PhotoImage(file=logo)
                text, img = '', imgdic[logo]
            else: text, img = logo, None
            btn = ttk.Button(self, bootstyle='outline-info',
                width=self.width, text=text, image=img,
                compound='center', padding=5)
            self.bind(btn, tool)
            btn.pack(side=side, padx=2, pady=5)
            if not fixed:
                self.toolset[-1][1].append(btn)
        if fixed:
            orient = {'x':'vertical', 'y':'horizontal'}[self.orient]
            line = ttk.Separator(self, orient=orient)
            line.pack(side=side, fill={'x':'y', 'y':'x'}[self.orient])

    def active_set(self, name):
        for n, tools in self.toolset:
            for btn in tools:
                if n == name:
                    btn.pack(side={'x':'left', 'y':'top'}[self.orient],
                     padx=2, pady=5)
                else:
                    btn.pack_forget()

    def add_pop(self, logo, default):
        side = {'x':'right', 'y':'bottom'}[self.orient]
        btn = ttk.Button(self, bootstyle='outline-info',
            text=logo, padding=5, width=self.width)
        btn.config(command=lambda: self.menu_drop(btn))
        btn.pack(side=side, padx=2, pady=5)
        self.active_set(default)

    def menu_drop(self, btn):
        menu = tk.Menu(self, tearoff=0)
        for name, item in self.toolset:
            menu.add_command(label=name, command=lambda n=name: self.active_set(n))
        menu.post(btn.winfo_rootx()+btn.winfo_width()//2,
                  btn.winfo_rooty()+btn.winfo_height()//2)

if __name__ == '__main__':
    path = '../floodfill.gif'
    app = ttk.Window('ToolBar')
    frame = app
    tool = ToolBar(frame, orient='x', width=0)
    # path = 'C:/Users/54631/Documents/projects/imagepy2/fucai/imgs/_help.png'
    tool.add_tools('A', [(path, print)] * 3, True)
    tool.add_tools('B', [('Basic', print)] * 3, False)
    tool.add_tools('C', [('Come', print)] * 3, False)
    tool.add_pop('P', 'C')
    tool.pack(fill='x', side='top')
    app.mainloop()
