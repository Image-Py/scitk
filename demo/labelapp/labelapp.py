import sys; sys.path.append('../../')

import ttkbootstrap as ttk
import scitk.ttk as sttk
from scitk.widgets.toolbar import ToolBar
from scitk.canvas import MCanvas as Canvas

class Classmanager(ttk.Frame):
    cmap = [
        "#a6cee3", "#1f78b4", "#b2df8a", "#33a02c",
        "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00",
        "#cab2d6", "#6a3d9a", "#ffff99", "#b15928"
    ]
    def __init__(self, parent, **key):
        super().__init__(parent, **key)
        self.toolbar = ttk.Frame(self)
        self.toolbar.pack(side='top', fill='x')
        btn_new = ttk.Button(self.toolbar, text='new', bootstyle='info-outline', padding=2)
        btn_new.pack(side='left', padx=3, pady=3)

        btn_edit = ttk.Button(self.toolbar, text='edit', bootstyle='info-outline', padding=2)
        btn_edit.pack(side='left', padx=3, pady=3)

        btn_del = ttk.Button(self.toolbar, text='del', bootstyle='info-outline', padding=2)
        btn_del.pack(side='left', padx=3, pady=3)

        btn_clear = ttk.Button(self.toolbar, text='clear', bootstyle='info-outline', padding=2)
        btn_clear.pack(side='left', padx=3, pady=3)

        btn_unsel = ttk.Button(self.toolbar, text='unsel', bootstyle='info-outline', padding=2)
        btn_unsel.pack(side='left', padx=3, pady=3)

        cls_lst = self.cls_lst = sttk.Gridview(self, indexwidth=False, mode='row', selmode='single', stripe=True, edit=True)
        cls_lst.set([], columns=['Name'])
        cls_lst.set_column_width(0, 80, 1)
        cls_lst.pack(fill='both', expand=True)

        btn_new.config(command=self.on_new)
        btn_clear.config(command=self.on_clear)
        btn_del.config(command=self.on_delete)
        btn_edit.config(command=self.on_edit)
        btn_unsel.config(command=self.on_unsel)
        self.classes = []

    def on_new(self):
        self.classes.append('new class')
        self.set(self.classes)
        self.cls_lst.active(len(self.classes)-1, 0)

    def on_clear(self): self.set([])

    def on_unsel(self):
        self.cls_lst.select(None)
        self.set(self.classes)
    
    def on_delete(self):
        if self.cls_lst.selection is None: return
        self.classes.pop(self.cls_lst.selection[0])
        self.set(self.classes)

    def on_edit(self):
        if self.cls_lst.selection is None: return
        self.cls_lst.active(self.cls_lst.selection[0], 0)

    def set(self, classes):
        self.classes = classes
        self.cls_lst.set([[i] for i in classes], columns=['Name'])
        for i in range(len(classes)):
            self.cls_lst.set_cell_color(i, 'x', self.cmap[i%12])

    def default(self):
        i = self.cls_lst.selection
        if i is None: return
        return self.classes[i], self.cmap[i%12]

    def get_classes(self):
        return [(c, self.cmap[i%12]) for (i,c) in enumerate(self.classes)]

classes = ['human', 'car', 'dog', 'cat', 'tree']

# from plugins import Gaussian

class MainFrame(ttk.Frame):
    def __init__(self, parent, **key):
        super().__init__(parent, **key)

        toolbar = self.toolbar = ToolBar(self)
        toolbar.add_tools('IO', [('Open', None, print),
                                 ('Open Folder', None, print),
                                 ('Save', None, print)], True)

        toolbar.add_tools('Browse', [('Next', None, print),
                                     ('Prev', None, print),
                                     ('Zoom', None, print),
                                     ('Move', None, print),
                                     ('Auto Fit', None, print)], True)
        
        toolbar.add_tools('Edit', [('Rectangle', None, print),
                                   ('Polygon', None, print),
                                   ('Line', None, print),
                                   ('Point', None, print),
                                   ('Editor', None, print),
                                   ('Clear', None, print)], True)

        toolbar.add_tools('AI', [('Sam', None, print),
                                 ('xxx', None, print)], True)
        
        toolbar.pack(fill='x', side='top')

        
        self.status = ttk.Label(self)
        self.status.config(text='状态栏')
        self.status.pack(side='bottom', fill='x')
        ttk.Separator(self).pack(side='bottom', fill='x')

    
        self.fmanager = sttk.FileManager(self)
        self.fmanager.pack(side='left', fill='y')

        self.canvas = Canvas(self)
        self.canvas.pack(side='left', fill='both', expand=True)

        
        rp = self.rpanel = sttk.Panedbook(self)
        panel = rp.add('Class Manager', weight=1)
        clsmanager = Classmanager(panel)
        clsmanager.pack(fill='both', expand=True, padx=1, pady=1)
        clsmanager.set(classes)

        panel = rp.add('Label Manager', weight=1)
        lab_lst = sttk.Gridview(panel, indexwidth=False)
        lab_lst.set([], columns=['Name'])
        lab_lst.set_column_width(0, 80, 1)
        lab_lst.pack(fill='both', expand=True, padx=1, pady=1)
    
        rp.config(width=200)
        rp.pack(side='right', fill='y')

        self.fmanager.bind('<<File-Select>>', self.on_open)

    def get_img(self): return self.canvas.image

    # def alert(
    def info(self, info):
        print(info)
        
    def on_open(self, path):
        from imageio import imread
        img = imread(path)
        self.canvas.set_img(img)

    def info(self, info):
        self.status.config(text=info)


if __name__ == '__main__':
    app = ttk.Window('标注工具')
    ttk.Style('darkly')
    frame = MainFrame(app)
    frame.pack(fill='both', expand=True)
    app.mainloop()
