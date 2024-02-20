# import wx, platform
import numpy as np
import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as ttk
from tkinter import colorchooser

#style = ttk.Style()
#style.configure('design1.TEntry', foreground='green', fieldbackground='lightyellow', bordercolor='red')


# style = ttk.Style()
# style.configure('Padded.TEntry', padding=0)

class Checkbutton(ttk.Checkbutton):
    def __init__(self, frame, *p, **key):
        self.value = tk.BooleanVar()
        super().__init__(frame, var=self.value, onvalue=True, offvalue=False, *p, **key)

    def set(self, value): self.value.set(value)

    def get(self): return self.value.get()
    
class NumCtrl(ttk.Frame):
    """NumCtrl: derived from tk.Entry"""
    def __init__(self, parent, rang, accury, title, unit, app=None):
        ttk.Frame.__init__(self, parent)
        self.prefix = ttk.Label(self, text=title)
        self.prefix.pack(side="left", padx=5)
        self.ctrl = ttk.Entry(self, width=5)
        self.ctrl.bind("<KeyRelease>", self.ontext)
        self.ctrl.pack(side="left", fill='x', expand=True)
        self.postfix = ttk.Label(self, text=unit)
        self.postfix.pack(side="left", padx=5)
        
        self.min, self.max = rang
        self.accury = accury
        self.pack(pady=5, fill='x')
    
    def ontext(self, event):
        if self.get() is None:
            self.ctrl.config(bootstyle='danger')
            self.event_generate("<<ParameterEvent>>", state=0)
            # self.ctrl.config(bg="#FFFF00")  # set background color to yellow
        else:
            self.ctrl.config(bootstyle="default")  # set background color to white
            self.event_generate("<<ParameterEvent>>", state=1)
        
    def set(self, n):
        if self.accury > 0:
            self.ctrl.insert(0, str(round(n, self.accury)))
        else:
            self.ctrl.insert(0, str(int(n)))
        
    def get(self):
        sval = self.ctrl.get()
        try:
            num = float(sval) if self.accury > 0 else int(sval)
        except ValueError:
            return None
        if num < self.min or num > self.max:
            return None
        if abs(round(num, self.accury) - num) > 1E-5:
            return None
        return num

class TextCtrl(ttk.Frame):
    def __init__(self, parent, title, unit, app=None):
        ttk.Frame.__init__(self, parent)
        
        self.prefix = ttk.Label(self, text=title)
        self.prefix.pack(side="left", padx=5)
        self.ctrl = ttk.Entry(self, width=10)
        self.ctrl.pack(side="left", fill='x', expand=True)
        self.postfix = ttk.Label(self, text=unit)
        self.postfix.pack(side="left", padx=5)
        self.ctrl.bind("<KeyRelease>", self.ontext)
        self.pack(pady=5, fill='x')
        
    def ontext(self, event):
        self.event_generate("<<ParameterEvent>>", state=1)
        
    def set(self, n):
        self.ctrl.delete(0, 'end')
        self.ctrl.insert(0, n)
        
    def get(self):
        return self.ctrl.get()
    
class ColorCtrl(ttk.Frame):
    def __init__(self, parent, title, unit, app=None):
        ttk.Frame.__init__(self, parent)
        
        self.prefix = ttk.Label(self, text=title)
        self.prefix.pack(side="left", padx=5)
        self.colorbox = tk.Frame(self, width=30,
                highlightthickness=1, highlightbackground='black',
                height=30, background='red', autostyle=False)
        self.colorbox.pack(side='left')
        
        self.ctrl = ttk.Entry(self, width=10)
        self.ctrl.pack(side="left", fill='x', expand=True)
        self.postfix = ttk.Label(self, text=unit)
        self.postfix.pack(side="left", padx=5)
        self.ctrl.bind("<KeyRelease>", self.ontext)
        self.ctrl.bind("<Double-Button-1>", self.oncolor)
        self.pack(pady=5, fill='x')
        
    def ontext(self, event):
        # self.f(self)
        try:
            color = str(self.ctrl.get())
            self.colorbox.config(bg=color)
            self.ctrl.config(bootstyle='default')
            self.event_generate("<<ParameterEvent>>", state=1)
        except:
            self.ctrl.config(bootstyle='danger')
            self.event_generate("<<ParameterEvent>>", state=0)
            
    def oncolor(self, event):
        color = tk.colorchooser.askcolor()
        if color[1]:
            self.colorbox.config(bg=color[1])
            self.ctrl.delete(0, tk.END)
            self.ctrl.insert(0, color[1])
            self.event_generate("<<ParameterEvent>>", state=1)
    
    def set(self, color):
        color = "#{:02x}{:02x}{:02x}".format(*color)
        self.colorbox.config(bg=color)
        self.ctrl.delete(0, tk.END)
        self.ctrl.insert(0, color)
        
    def get(self):
        color = self.ctrl.get()[1:]
        return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
    

class Choice(ttk.Frame):
    def __init__(self, parent, choices, tp, title, unit, app=None):
        ttk.Frame.__init__(self, parent)
        self.tp, self.choices = tp, choices
        
        self.prefix = ttk.Label(self, text=title)
        self.prefix.pack(side=tk.LEFT, padx=5)
        
        self.ctrl = ttk.Combobox(self, values=choices, width=5)
        self.ctrl.pack(side=tk.LEFT, fill='x', expand=True)
        
        self.postfix = tk.Label(self, text=unit)
        self.postfix.pack(side=tk.LEFT, padx=5)
        
        self.pack(pady=5, fill='x')
        
    def on_choice(self, *args):
        if hasattr(self, 'f'):
            self.f(self)
    
    def bind(self, f):
        self.f = f
        
    def set(self, x):
        if x in self.choices:
            self.ctrl.set(x)
        
    def get(self):
        return self.tp(self.ctrl.get())

class Label(ttk.Frame):
    def __init__(self, parent, title, app=None):
        ttk.Frame.__init__(self, parent)
        self.lab_title = tk.Label(self, text=title, justify="left")
        self.lab_title.pack(side=tk.TOP, padx=5, pady=5, anchor="w")
        self.pack(pady=5, fill='x')
        
    def bind(self, z, f):
        pass
        
    def set_value(self, v):
        pass
        
    def get_value(self, v):
        pass

from ttkbootstrap.scrolled import ScrolledFrame

class Choices(ttk.Labelframe):
    def __init__(self, parent, choices, title, app=None):
        self.choices = list(choices)
        ttk.Labelframe.__init__(self, parent, text=title)
        self.ctrl = ScrolledFrame(self, width=0, height=100)
        # self.ctrl = ttk.Listbox(self.sizer, selectmode=tk.MULTIPLE)
        self.ctrls = []
        for choice in choices:
            btn = Checkbutton(self.ctrl, text=choice)
            btn.pack(side=tk.BOTTOM, fill=tk.X, pady=3)
            self.ctrls.append(btn)
            
        self.ctrl.pack(side='top', pady=5, fill='x')
        self.ctrl.bind("<ButtonRelease-1>", self.on_check)
        self.pack(pady=5, padx=5, fill='x')

    def bind(self, z, f):
        self.f = f

    def on_check(self, event):
        self.f(self)

    def get(self):
        return [i for i,j in zip(self.choices, self.ctrls) if j.get()]

    def set(self, value):
        for i in range(len(self.choices)):
            self.ctrls[i].set(self.choices[i] in value)

class Check(ttk.Frame):
    def __init__(self, parent, title, app=None):
        ttk.Frame.__init__(self, parent)
        self.value = tk.BooleanVar()    
        self.ctrl = Checkbutton(self, text=title)

        self.ctrl.pack(side=tk.TOP, padx=5, pady=5, anchor="w")
        self.ctrl.invoke()
        self.pack(pady=5, fill='x')
        self.set = self.ctrl.set
        self.get = self.ctrl.get
        
    def bind(self, z, f):
        pass

class FloatSlider(ttk.Frame):
    """NumCtrl: derived from tk.Entry"""
    def __init__(self, parent, rang, accury, title, unit, app=None):
        ttk.Frame.__init__(self, parent)
        self.scale = ttk.Scale(self, from_=rang[0], to=rang[1])
        self.scale.pack(side='top', padx=5, pady=3, fill='x')
        self.scale.config(command=self.onscale)
        self.pack(pady=5, fill='x')
        
        ttk.Label(self, text=rang[0]).pack(side="left", padx=5)
        ttk.Frame(self).pack(side='left', expand=True, fill='x')
        ttk.Label(self, text=title).pack(side="left", padx=5)
        
        self.ctrl = ttk.Entry(self, width=10)
        self.ctrl.bind("<KeyRelease>", self.ontext)
        self.ctrl.pack(side="left")

        ttk.Label(self, text=unit).pack(side="left", padx=5)
        ttk.Frame(self).pack(side='left', expand=True, fill='x')
        ttk.Label(self, text=rang[1]).pack(side="left", padx=5)
        
        self.min, self.max = rang
        self.accury = accury
        self.pack(pady=5, fill='x')

    def onscale(self, event):
        self.ctrl.delete(0, "end")  # 清空现有的文本
        self.ctrl.insert(0, round(self.scale.get(), self.accury))

    def ontext(self, event):
        if self.get() is None:
            self.ctrl.config(bootstyle='danger')
            # self.ctrl.config(bg="#FFFF00")  # set background color to yellow
        else:
            self.scale.set(self.get())
            self.ctrl.config(bootstyle="default")  # set background color to white
        
    def set(self, n):
        if self.accury > 0:
            self.ctrl.insert(0, str(round(n, self.accury)))
        else:
            self.ctrl.insert(0, str(int(n)))
        
    def get(self):
        sval = self.ctrl.get()
        try:
            num = float(sval) if self.accury > 0 else int(sval)
        except ValueError:
            return None
        if num < self.min or num > self.max:
            return None
        if abs(round(num, self.accury) - num) > 1E-5:
            return None
        return num
    
'''
class PathCtrl(wx.Panel):
    def __init__(self, parent, filt, io, title, app=None):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        self.prefix = lab_title = wx.StaticText( self, wx.ID_ANY, title,
                                   wx.DefaultPosition, wx.DefaultSize)
        self.filt, self.io = filt, io
        lab_title.Wrap( -1 )
        sizer.Add( lab_title, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.ctrl = wx.TextCtrl(self, wx.TE_RIGHT)
        sizer.Add( self.ctrl, 2, wx.ALL, 5 )
        self.SetSizer(sizer)
        
        self.ctrl.Bind(wx.EVT_KEY_UP, self.ontext)
        self.ctrl.Bind( wx.EVT_LEFT_DCLICK, self.onselect)
        
    def Bind(self, z, f): self.f = f
        
    def ontext(self, event): 
        self.f(self)
        
    def onselect(self, event):
        if isinstance(self.filt, str): self.filt = self.filt.split(',')
        filt = '|'.join(['%s files (*.%s)|*.%s'%(i.upper(),i,i) for i in self.filt])
        dic = {'open':wx.FD_OPEN, 'save':wx.FD_SAVE}
        if self.io=='folder':
            dialog = wx.DirDialog(self, 'Path Select', '', wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST | wx.FD_CHANGE_DIR)
        else: dialog = wx.FileDialog(self, 'Path Select', '', '.', filt, dic[self.io] | wx.FD_CHANGE_DIR)

        rst = dialog.ShowModal()
        if rst == wx.ID_OK:
            path = dialog.GetPath()
            self.ctrl.SetValue(path)
            self.f(self)
        dialog.Destroy()
        
    def SetValue(self, value):
        self.ctrl.SetValue(value)
        
    def GetValue(self):
        return self.ctrl.GetValue()
        
class AnyType( wx.Panel ):
    def __init__( self, parent, title, app=None):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size(-1, -1), style = wx.TAB_TRAVERSAL )
        
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        self.prefix = lab_title = wx.StaticText( self, wx.ID_ANY, title,
                                   wx.DefaultPosition, wx.DefaultSize)
        lab_title.Wrap( -1 )
        sizer.Add( lab_title, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.txt_value = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer.Add( self.txt_value, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
        com_typeChoices = ['Int', 'Float', 'Str']
        self.postfix = self.com_type = wx.ComboBox( self, wx.ID_ANY, 'Float', wx.DefaultPosition, wx.DefaultSize, com_typeChoices, 0 )
        sizer.Add( self.com_type, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        
        self.SetSizer( sizer )
        self.Layout()
        
        # Connect Events
        self.txt_value.Bind( wx.EVT_KEY_UP, self.on_text )
        self.com_type.Bind( wx.EVT_COMBOBOX, self.on_type )
    
    def Bind(self, z, f):
        self.f = f
    
    def SetValue(self, v):
        self.txt_value.SetValue(str(v))
        if isinstance(v, int):
            self.com_type.Select(0)
        if isinstance(v, float):
            self.com_type.Select(1)
        else: self.com_type.Select(2)


    def GetValue(self):
        tp = self.com_type.GetValue()
        sval = wx.TextCtrl.GetValue(self.txt_value)
        if tp == 'Float':
            try: num = float(sval)
            except ValueError: return None
        if tp == 'Int':
            try: num = int(sval)
            except ValueError: return None
        if tp == 'Str':
            try: num = str(sval)
            except ValueError: return None
        return num
    
    # Virtual event handlers, overide them in your derived class
    def on_text( self, event ):
        self.f(self)
        if self.GetValue()==None:
            self.txt_value.SetBackgroundColour((255,255,0))
        else: self.txt_value.SetBackgroundColour((255,255,255))
        self.Refresh()
    
    def on_type( self, event ):
        if self.GetValue()==None:
            self.txt_value.SetBackgroundColour((255,255,0))
        else: self.txt_value.SetBackgroundColour((255,255,255))
        self.Refresh()
'''

if __name__ == '__main__':
    app = ttk.Window()
    #style = ttk.Style.get_instance()
    #style.configure('danger.TEntry', padding=3)
    #style.configure('danger.TCombobox', padding=3)
        
    frame = app
    NumCtrl(frame, (0,10), 1, 'Age', 'int')
    TextCtrl(frame, 'Name', 'str')
    ColorCtrl(frame, 'Color', 'color')
    Choice(frame, [1,2,3], int, 'Choice', 'int')
    Choices(frame, [1,2,3,4,5,6,7], 'Choices')
    Label(frame, 'I am a lable')
    Check(frame, 'I am a check')
    FloatSlider(frame, (0,10), 1, 'Age', 'float')
    app.mainloop() 
