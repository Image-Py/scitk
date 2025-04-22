import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap import Style
import ttkbootstrap.constants as tc
import pandas as pd

class Table(Tableview):
    def __init__(self, parent, check=False, **key):
        Tableview.__init__(self, parent,
            # paginated=page,
            # searchable=search,
            bootstyle=tc.PRIMARY,
            stripecolor=('#eeeeee', None),
            **key)
        
        self.check = check
        self.data = []
        self.pack()
        self.view.bind('<Double-1>', self.on_double_click)
        self.view.bind('<Button-1>', self.on_click)
        self.on_item_active = print
        self.on_item_click = print
        self.sss = 0

    def insert_row(self, index='end', values=[]):
        if self.check:
            values = list(values)
            values[0] = ('\u2610','\u2611')[values[0]]
        Tableview.insert_row(self, index, values)
    
    def set_col_width(self, ws=30):
        if isinstance(ws, int):
            for i in range(len(self.tablecolumns)):
                self.view.column(i, width=ws)
        if isinstance(ws, list):
            for i, w in enumerate(ws):
                self.view.column(i, width=w)
        if ws == 'auto':
            self.autofit_columns()

    def on_double_click(self, event):
        c = self.view.identify_column(event.x)
        r = self.view.identify_row(event.y)
        r, c = int(r[1:], 16)-1-self.sss, int(c[1:], 16)-1
        self.on_item_active(r, c, self.data.values[r, c])

    def on_click(self, event):
        tc = self.view.identify_column(event.x)
        tr = self.view.identify_row(event.y)
        r, c = int(tr[1:], 16)-1-self.sss, int(tc[1:], 16)-1
        # on check
        if c==0 and self.check:
            v = self.data.loc[self.data.index[r], self.data.columns[c]]
            self.data.loc[self.data.index[r], self.data.columns[c]] = not v
            self.view.set(tr, tc, ('\u2610','\u2611')[int(not v)])
        else: self.on_item_click(r, c, self.data.values[r, c])
    
    def bind(self, tag, f=print):
        if tag == '<Item-active>':
            self.on_item_active = f
        elif tag == '<Item-click>':
            self.on_item_click = f
        else: Tableview.bind(self, tag, f)

    def set_data(self, data):
        self.sss += len(self.data)
        self.data = data
        self.build_table_data(data.columns, data.values)
        
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('800x600')
    table = Table(root, check=True, autofit=True, paginated=False, searchable=False)

    data = pd.read_csv('./矿物衍射数据/PDF#05-0628#石盐.csv', index_col=0)
    data.insert(0, '', False)
    data = pd.concat([data] * 1000)
    table.set_data(data)
    
    root.mainloop()
