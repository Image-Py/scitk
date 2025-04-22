import ttkbootstrap as ttk

class Notebook(ttk.Frame):
    def __init__(self, parent, bootstyle='info', **key):
        super().__init__(parent, **key)
        self.tags = ttk.Frame(self)
        self.bootstyle = bootstyle
        ttk.Separator(self.tags, bootstyle=bootstyle).pack(side='bottom', fill='x')
        #self.tags.grid(row=0, column=0, sticky='ew')
        self.tags.pack(side='top', fill='x')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        f = lambda : self.add(ttk.Button(self), title='Image')
        # ttk.Button(self.tags, padding=0, bootstyle='light', command=f).pack(side='right')
        self.panels = []
        self.cursor = None

    @property
    def npage(self): return len(self.panels)
    
    def set_title(self, i, title):
        self.panels[i][0].config(text=title)

    def get_title(self, i):
        return self.panels[i][0].cget('text')
        
    def add(self, panel, title):
        # btn = ttk.Button()
        tag = ttk.Button(self.tags, padding=(5,0,5,0), text=title, takefocus=False, bootstyle=self.bootstyle)
        tag.config(command=lambda btn=tag:self.on_select(btn))
        x = ttk.Button(tag, padding=(0,-4,0,-4), text="\u00D7", bootstyle=self.bootstyle)
        x.config(command=lambda btn=tag:self.on_remove(btn))
        x.place(relx=1, rely=0.5, x=-100, y=-1, anchor='e')
        self.panels.append((tag, x, panel))
        tag.pack(side='left', padx=1)
        self.select(len(self.panels)-1)
        
    def get(self, idx=None):
        if idx is None: idx = self.cursor
        if idx is None: return None
        return self.panels[idx][2]
    
    def remove(self, idx=None):
        btn, x, pan = self.panels.pop(idx)
        btn.destroy()
        pan.destroy()
        self.cursor = None
        if len(self.panels)>0:
            self.select(max(0, idx-1))

    def select(self, idx):
        last = self.get()
        if not last is None: last.pack_forget()
        self.panels[idx][2].pack(fill='both', expand=True) #grid(row=1, column=0, sticky='nsew')
        
        self.cursor = idx

        for i in range(len(self.panels)):
            btn, x, pan = self.panels[i]
            
            if i != idx:
                btn.config(padding=(5,0,5,0), bootstyle='outline-'+self.bootstyle)
                x.place(relx=1, rely=0.5, x=100, anchor='e')
            else:
                btn.config(padding=(5,0,20,0), bootstyle=self.bootstyle)
                x.place(relx=1, rely=0.5, x=-5, anchor='e')
        self.event_generate("<<NoteActiveEvent>>", x=idx)
            
            
    def on_select(self, btn):
        idx = [i[0] for i in self.panels].index(btn)
        self.select(idx)

    def on_remove(self, btn):
        idx = [i[0] for i in self.panels].index(btn)
        self.event_generate("<<NoteCloseEvent>>", x=idx)
        self.remove(idx)

if __name__ == '__main__':
    import pandas as pd
    import tkinter as tk
    app = ttk.Window(title='Notebook')
    app.geometry('800x600')

    bar = ttk.Frame(app)
    panel = ttk.Frame(bar, bootstyle='primary')
    panel.pack(side='left', padx=3, pady=3)

    container = ttk.Frame(panel)
    container.pack(side='top', fill='x', padx=1, pady=(1,0))

    lab = ttk.Label(panel, text='tool set 1', anchor='center', bootstyle='inverse-primary')
    lab.pack(side='bottom', fill='x', padx=1, pady=(0,1))
        
    ttk.Button(container, text='tool1').pack(side='left', padx=3, pady=3)
    ttk.Button(container, text='tool2').pack(side='left', padx=3, pady=3)
    ttk.Button(container, text='tool3').pack(side='left', padx=3, pady=3)
    bar.pack(side='top', fill='x')
    
    book = Notebook(app, bootstyle='dark')
    book.pack(fill='both', expand=True)
    
    def create(colors=['red', 'green', 'blue'], count = [0]):
        count[0] += 1
        frame = tk.Frame(book, width=300, height=100, autostyle=False, bg=colors[count[0]%3])
        book.add(frame, 'new tab %d'%count[0])
        
    ttk.Button(app, text='create book', command=create).pack(side='bottom')
    
    app.mainloop()
