import ttkbootstrap as ttk

class Panedbook(ttk.Frame):
    def __init__(self, parent, **key):
        super().__init__(parent, **key)
        self.pane = ttk.Panedwindow(self, orient='vertical')
        self.pane.pack(fill='both', expand=True, padx=1, pady=1)

    def add(self, title, weight=1):
        frame = ttk.Frame(self.pane)
        label = ttk.Label(frame, text=title, bootstyle='inverse-dark')
        label.pack(side='top', fill='x')
        x = ttk.Button(label, text='X', padding=(5,0), bootstyle='dark')
        x.config(command=frame.destroy)
        x.pack(side='right')
        self.pane.add(frame, weight=weight)
        return frame

if __name__ == '__main__':
    import pandas as pd
    import tkinter as tk
    app = ttk.Window()
    book = Panedbook(app)
    book.pack(fill='both', expand=True)
    
    p = book.add('abc', 2)
    red = tk.Frame(p, width=300, height=100, autostyle=False, bg="red")
    red.pack(fill='both', expand=True)
    
    p = book.add('ddd')
    red = tk.Frame(p, width=300, height=100, autostyle=False, bg="blue")
    red.pack(fill='both', expand=True)
    
    app.mainloop()
