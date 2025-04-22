import numpy as np
import math
from .histpanel import HistPanel
from .normal import FloatSlider, ParaCtrl

class ThresholdPanel(ParaCtrl):
    def __init__(self, parent, mode, hist, rang, accury, command=None, app=None):
        super().__init__(parent, command)
        self.parent = parent
        self.mode = mode
        self.rang = rang
        self.accury = accury
        
        self.histpan = HistPanel(self)
        self.histpan.set(hist)
        self.histpan.pack(fill='both', expand=True)
        
        self.sli_high = FloatSlider(self, rang, accury, '', '')
        self.sli_high.set(rang[0])
        self.sli_high.config(command=lambda dir=True: self.on_threshold(dir, None))
        self.sli_high.pack(fill='x')
        
        if mode == 'bc': rang, accury = (1, 89), 0
            
        self.sli_low = FloatSlider(self, rang, accury, '', '')
        self.sli_low.set(rang[1])
        self.sli_low.config(command=lambda dir=False: self.on_threshold(dir, None))
        self.sli_low.pack(fill='x')
        self.pack(pady=5, fill='x')
        
    def on_threshold(self, dir, event):        
        a, b = self.get()
        
        if self.mode == 'lh':
            if dir:
                b = max(a, b)
            else:
                a = min(a, b)
            
            self.set((a, b))
            a = int((a - self.rang[0]) / (self.rang[1] - self.rang[0]) * 255)
            b = int((b - self.rang[0]) / (self.rang[1] - self.rang[0]) * 255)
            self.histpan.set_lim(a, b)
        
        if self.mode == 'bc':
            mid = 128 - a / (self.rang[1] - self.rang[0]) * 255
            length = 255 / math.tan(b / 180.0 * math.pi)
            self.histpan.set_lim(mid - length / 2, mid + length / 2)
        
        if self.command: self.command()
        
    def set(self, n):
        self.sli_high.set(n[0])
        self.sli_low.set(n[1])
        
    def get(self):
        b = self.sli_low.get()
        a = self.sli_high.get()
        return None if None in (a, b) else (a, b)

if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    hist = np.random.rand(256)
    command = lambda : print(hist.get())
    hist = ThresholdPanel(root, 'bc', hist, (-128, 128), 0, command=command)
    hist.set((0, 45))
    # hist.Bind(None, lambda x:x)
    hist.pack()
    root.mainloop()