import ttkbootstrap as ttk
from tkinter.filedialog import askdirectory
from .gridview import Gridview
import re, os

class FileManager(ttk.Frame):
    def __init__(self, parent, format=None, bootstyle='primary', **key):
        super().__init__(parent, bootstyle='secondary')
        container = ttk.Frame(self)
        container.pack(fill='both', expand=True, padx=1, pady=1)
        # lab = ttk.Label(container, text='File Manager', bootstyle='inverse')
        # lab.grid(row=0, column=0, columnspan=5, sticky='nsew')
        
        self.txt_path = ttk.Entry(container, width=5)
        self.txt_path.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.btn_search = ttk.Button(container, text='open', command=self.on_browse, bootstyle=bootstyle)
        self.btn_search.grid(row=1, column=4, padx=5, pady=5, sticky="nsew")

        lab = ttk.Label(container, text='format')
        lab.grid(row=2, column=0, padx=5, pady=5)

        format = format or ['*', 'bmp', 'jpg', 'png', 'txt', 'csv', 'json']
        self.format = ttk.Combobox(container, values=format, width=8)
        self.format.set('*')
        self.format.bind("<<ComboboxSelected>>", self.on_filter)
        
        self.format.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        lab = ttk.Label(container, text='contains')
        lab.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")
        self.txt_filter = ttk.Entry(container, text='', width=10)
        fns = {'Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R'}
        txt_changed = lambda e: 1 if e.keysym in fns else self.on_filter(e)
        self.txt_filter.bind('<KeyRelease>', txt_changed)
        self.txt_filter.grid(row=2, column=4, padx=5, pady=5, sticky="nsew")

        # self.btn_search = ttk.Button(self, text='open')
        # self.btn_search.grid(row=0, column=2, padx=5, pady=5)
        lst_files = self.lst_files = Gridview(container, mode='row', indexwidth=False, stripe=False, bootstyle=bootstyle)
        lst_files.set([], columns=['Name'], index=None)
        lst_files.set_column_width(0, 80, expand=1)
        lst_files.grid(row=3, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")

        # self.lst_files('<<Cell-Select>>', self.on_select)
        self.lst_files.bind('<<Cell-Active>>', self.on_file)
        
        container.columnconfigure(2, weight=1)
        container.rowconfigure(3, weight=1)

        self.files = []
        self.subfiles = []
        self.workspace = ''

        self.dir_handle = self.file_handle = print

    def bind(self, sequence, func):
        if sequence == '<<File-Select>>':
            self.file_handle = func
        elif sequence == '<<Dir-Select>>':
            self.dir_handle = func
        else: super().bind(sequence, func)

    def on_file(self, event):
        self.file_handle(self.workspace+'/'+self.subfiles[event.y])
    
    def on_filter(self, event):
        fmt = self.format.get().lower()
        if fmt=='*': fmt = ''
        temp = self.txt_filter.get()
        sub = [i for i in self.files if i.lower().endswith(fmt.lower())]
        self.subfiles = [i for i in sub if re.compile(temp).search(i)]
        self.lst_files.set([[i] for i in self.subfiles], columns=['Name'])
        
    def on_browse(self):
        path = askdirectory(title='select workspace')
        if not path: return
        self.workspace = path
        self.txt_path.delete(0, "end")  # 删除现有文本
        self.txt_path.insert(0, path)
        self.files = os.listdir(path)
        self.on_filter(None)
        self.dir_handle(path)


if __name__ == '__main__':
    root = ttk.Window()
    ttk.Style('darkly')
    root.geometry('300x600')
    table = FileManager(root)
    table.pack(fill='both', expand=True)
    root.mainloop()
