import ttkbootstrap as ttk

class Panedbook(ttk.Panedwindow):
    def __init__(self, parent, **key):
        super().__init__(parent, orient='vertical', **key)

    def add(self, title, panel, weight=1):
        frame = ttk.Frame(panel)
        label = ttk.Label(frame, text=title, bootstyle='inverse')
        label.pack(side='top', fill='x')
        x = ttk.Button(label, text='X', padding=(5,0), bootstyle='dark')
        x.config(command=panel.destroy)
        x.pack(side='right')
        frame.pack(side='top', fill='x')
        
        super().add(panel, weight=weight)

    
if __name__ == '__main__':
    import pandas as pd
    import tkinter as tk
    app = ttk.Window()
    book = Panedbook(app)
    book.pack(fill='both', expand=True)
    
    
    red = tk.Frame(book, width=300, height=100, autostyle=False, bg="red")
    book.add('red', red)

    blue = tk.Frame(book, width=300, height=100, autostyle=False, bg="blue")
    book.add('blue', blue)
    
    app.mainloop()
