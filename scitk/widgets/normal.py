# import wx, platform
import numpy as np
import re
import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as ttk
from tkinter import colorchooser

#style = ttk.Style()
#style.configure('design1.TEntry', foreground='green', fieldbackground='lightyellow', bordercolor='red')


# style = ttk.Style()
# style.configure('Padded.TEntry', padding=0)

class ParaCtrl(ttk.Frame):
    def __init__(self, parent, command=print, **key):
        super().__init__(parent, **key)
        self.command = command
        self.prefix = self.postfix = None

    def get(self): pass
    def set(self, value): pass
    def valid(self): return True
    def config(self, **key):
        if 'command' in key: 
            self.command = key.pop('command')
        super().config(**key)

class Checkbutton(ttk.Checkbutton):
    def __init__(self, frame, *p, **key):
        self.value = tk.BooleanVar()
        super().__init__(frame, var=self.value, onvalue=True, offvalue=False, *p, **key)

    def set(self, value): self.value.set(value)

    def get(self): return self.value.get()
    
class NumCtrl(ParaCtrl):
    """NumCtrl: derived from tk.Entry"""
    def __init__(self, parent, rang, accury, title, unit, command=None, app=None):
        super().__init__(parent, command)
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
        style = ('danger', 'default')[self.valid()]
        self.ctrl.config(bootstyle=style)
        if self.command: self.command()
        
    def get(self):
        if not self.valid(): return None
        return (int, float)[self.accury>0](self.ctrl.get())

    def set(self, n):
        self.ctrl.delete(0, 'end')
        self.ctrl.insert(0, str(n))
        
    def valid(self):
        sval = self.ctrl.get()
        try:
            num = float(sval) if self.accury > 0 else int(sval)
        except ValueError:
            return False
        if num < self.min or num > self.max:
            return False
        if abs(round(num, self.accury) - num) > 1E-5:
            return False
        return True


class TextCtrl(ParaCtrl):
    def __init__(self, parent, title, unit, command=None, app=None):
        super().__init__(parent, command)
        
        self.prefix = ttk.Label(self, text=title)
        self.prefix.pack(side="left", padx=5)
        self.ctrl = ttk.Entry(self, width=10)
        self.ctrl.pack(side="left", fill='x', expand=True)
        self.postfix = ttk.Label(self, text=unit)
        self.postfix.pack(side="left", padx=5)
        self.ctrl.bind("<KeyRelease>", self.ontext)
        self.pack(pady=5, fill='x')
        
    def ontext(self, event):
        if self.command: self.command()
        
    def set(self, n):
        self.ctrl.delete(0, 'end')
        self.ctrl.insert(0, n)
        
    def get(self):
        return self.ctrl.get()
    
class ColorCtrl(ParaCtrl):
    def __init__(self, parent, title, unit, command=None, app=None):
        super().__init__(parent, command)
        
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
        if self.valid(): self.colorbox.config(bg=self.ctrl.get())
        self.ctrl.config(bootstyle=('danger', 'default')[self.valid()])
        if self.command: self.command()
            
    def valid(self):
        pattern = r'^#[a-fA-F0-9]{6}$'
        return not re.match(pattern, self.ctrl.get()) is None

    def oncolor(self, event):
        color = tk.colorchooser.askcolor()
        if color[1]:
            self.colorbox.config(bg=color[1])
            self.ctrl.delete(0, 'end')
            self.ctrl.insert(0, color[1])
            if self.command: self.command()
    
    def set(self, color):
        color = '#%.2x%.2x%.2x'%(color)
        self.colorbox.config(bg=color)
        self.ctrl.delete(0, tk.END)
        self.ctrl.insert(0, color)
        
    def get(self):
        color = self.ctrl.get()[1:]
        return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
    

class Choice(ParaCtrl):
    def __init__(self, parent, choices, tp, title, unit, command=None, app=None):
        super().__init__(parent, command)
        self.tp, self.choices = tp, choices
        
        self.prefix = ttk.Label(self, text=title)
        self.prefix.pack(side=tk.LEFT, padx=5)
        
        self.ctrl = ttk.Combobox(self, values=choices, width=5)
        self.ctrl.pack(side=tk.LEFT, fill='x', expand=True)
        self.ctrl.bind('<<ComboboxSelected>>', self.on_choice)
        
        self.postfix = tk.Label(self, text=unit)
        self.postfix.pack(side=tk.LEFT, padx=5)
        
        self.pack(pady=5, fill='x')
        
    def on_choice(self, *args):
        if self.command: self.command()
        
    def set(self, x):
        if x in self.choices: self.ctrl.set(x)
        
    def get(self): return self.tp(self.ctrl.get())

class Label(ParaCtrl):
    def __init__(self, parent, title, command=None, app=None):
        super().__init__(parent, None)
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

class Choices(ParaCtrl):
    def __init__(self, parent, choices, title, command=None, app=None):
        self.choices = list(choices)
        super().__init__(parent, command)
        ttk.Labelframe.__init__(self, parent, text=title)
        self.ctrl = ScrolledFrame(self, width=0, height=100)
        # self.ctrl = ttk.Listbox(self.sizer, selectmode=tk.MULTIPLE)
        self.ctrls = []
        for choice in choices:
            btn = Checkbutton(self.ctrl, text=choice, command=lambda:self.on_check(None))
            btn.pack(side=tk.BOTTOM, fill=tk.X, pady=3)
            self.ctrls.append(btn)
            
        self.ctrl.pack(side='top', pady=5, fill='x')
        self.ctrl.bind("<ButtonRelease-1>", self.on_check)
        self.pack(pady=5, padx=5, fill='x')

    def on_check(self, event):
        if self.command: self.command()

    def get(self):
        return [i for i,j in zip(self.choices, self.ctrls) if j.get()]

    def set(self, value):
        for i in range(len(self.choices)):
            self.ctrls[i].set(self.choices[i] in value)

class Check(ParaCtrl):
    def __init__(self, parent, title, command=None, app=None):
        super().__init__(parent, command)
        self.value = tk.BooleanVar()    
        self.ctrl = Checkbutton(self, text=title, command=self.on_check)

        self.ctrl.pack(side=tk.TOP, padx=5, pady=5, anchor="w")
        self.ctrl.set(True)
        self.pack(pady=5, fill='x')
        self.get = self.ctrl.get
        self.set = self.ctrl.set
        
    def on_check(self, *args):
        if self.command: self.command()

class FloatSlider(ParaCtrl):
    """NumCtrl: derived from tk.Entry"""
    def __init__(self, parent, rang, accury, title, unit, command=None, app=None):
        super().__init__(parent, command)
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
        self.ctrl.delete(0, "end")
        value = round(self.scale.get(), self.accury)
        value = (int, float)[self.accury>0](value)
        self.ctrl.insert(0, str(value))
        if self.command: self.command()

    def ontext(self, event):
        style = ('danger', 'default')[self.valid()]
        self.ctrl.config(bootstyle=style)
        if self.valid(): self.scale.set(self.get())
    
    def set(self, n):
        self.ctrl.delete(0, "end")
        if self.accury > 0:
            self.ctrl.insert(0, str(round(n, self.accury)))
        else: self.ctrl.insert(0, str(int(round(n))))
        # self.scale.config(command=None)
        command, self.command = self.command, None
        self.scale.set(n)
        self.command = command
        # self.scale.config(command=self.onscale)
        
    def valid(self):
        sval = self.ctrl.get()
        try:
            num = float(sval) if self.accury > 0 else int(sval)
        except ValueError:
            return False
        if num < self.min or num > self.max:
            return False
        if abs(round(num, self.accury) - num) > 1E-5:
            return False
        return True

    def get(self):
        if self.valid() is None: return None
        return (int, float)[self.accury>0](self.ctrl.get())

from tkinter.filedialog import askdirectory, askopenfile, asksaveasfile

class PathCtrl(ParaCtrl):
    """NumCtrl: derived from tk.Entry"""
    def __init__(self, parent, filt, io, title, command=None, app=None):
        super().__init__(parent, command)
        self.filt, self.io = filt, io
        self.prefix = ttk.Label(self, text=title)
        self.prefix.pack(side="left", padx=5)
        self.ctrl = ttk.Entry(self, width=30)
        self.ctrl.pack(side="left", fill='x', expand=True)
        self.btn = ttk.Button(self, text='...', command=self.onselect)
        self.btn.pack(side="left", padx=5)
        self.pack(pady=5, fill='x')
        
    def onselect(self):
        if isinstance(self.filt, str): self.filt = self.filt.split(',')
        filt = [('%s files'%i, '*.%s'%i) for i in self.filt]

        dic = {'open':askopenfile, 'save':asksaveasfile, 'folder': askdirectory}
        if self.io == 'folder': path = askdirectory()
        else: path = dic[self.io](filetypes=filt)
        if path: self.set(path if isinstance(path, str) else path.name)
        
    def set(self, value):
        self.ctrl.delete(0, "end")
        self.ctrl.insert(0, value)
        
    def get(self):
        return self.ctrl.get()
        
'''
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
    PathCtrl(frame, 'txt', 'open', 'Open')
    frame.bind('<<ParameterEvent>>', print)
    app.mainloop() 
