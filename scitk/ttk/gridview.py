import tkinter as tk
import ttkbootstrap as ttk
from copy import copy
from time import time
import re

def iscolor(color_string):
    if not isinstance(color_string, str): return False
    pattern = r'^#[0-9a-fA-F]{6}$'
    return True if re.match(pattern, color_string) else False
    
def column_labels(num):
    result = ''
    while num > 0:
        remainder = (num - 1) % 26
        result = chr(65 + remainder) + result
        num = (num - 1) // 26
    return result

def cumsum(arr, l=0):
    result = []
    s = sum(arr) + 0j
    real, imag = s.real, s.imag
    d = max(l-real, 0)/max(imag, 1)
    
    total = 0
    for num in arr:
        total += num.real + (num.imag * d)
        result.append(total)
    return result

def binary_search(sep, x):
    if len(sep)<=1: return 0
    if x < sep[0]: return 0
    left, right = 0, len(sep)-1
    while True:
        if right == left+1: return right
        mid = (left+right)//2
        if x<sep[mid]: right = mid
        else: left = mid

def getselectrg(msk):
    if isinstance(msk, int): return msk, msk+1
    if isinstance(msk, tuple): return msk
    if isinstance(msk, list): return min(msk), max(msk)+1
    
def isselected(rmsk, cmsk, r, c):
    '''check whether r,c is selected'''
    if rmsk is None or cmsk is None:
        return False
    isr = rmsk == slice(None) or rmsk[r]
    isc = cmsk == slice(None) or cmsk[c]
    return isr & isc

def build_style(name='primary'):
    style = ttk.Style()
    cmap = {'header':name, 'fg':'inputfg', 'line':'border', 'bg':'inputbg',
            'stripe':'secondary', 'selectbg':'selectbg', 'selectfg':'selectfg'}
    for i in cmap: cmap[i] = style.colors.get(cmap[i])
    cmap['stripe'] = style.colors.update_hsv(cmap['bg'], vd=0.3)
    return cmap

def fill(msk):
    for s in range(len(msk)):
        if msk[s]: break
    for e in range(len(msk)-1, -1, -1):
        if msk[e]: break
    for i in range(s, e):
        msk[i] = True

def snapshot(msk, snap):
    for i in range(len(msk)):
        msk[i] = snap[i]
        
def select(msk, sli, ctrl=False, shift=False):
    if sli is None:
        for i in range(len(msk)): msk[i] = False
        return None
    if sli == slice(None):
        for i in range(len(msk)): msk[i] = True
        return slice(None)
    if isinstance(sli, int):
        if ctrl:
            msk[sli] = not msk[sli]
        elif shift:
            msk[sli] = True
            fill(msk)
        else:
            for i in range(len(msk)): msk[i]=False
            msk[sli] = True
    if isinstance(sli, tuple):
        r1, r2 = min(sli), max(sli)+1
        if ctrl:
            for i in range(r1, r2): msk[i] = not msk[i]
        elif shift:
            msk[sli[1]] = True
            fill(msk)
        else:
            for i in range(len(msk)): msk[i]=False
            for i in range(r1, r2): msk[i] = True
    return msk

def get_selection(msk):
    if msk is None: return None
    if isinstance(msk, slice): return msk
    return [i for i in range(len(msk)) if msk[i]]

default = {'header':'lightgray', 'fg':'black', 'line':'gray', 'bg':'white',
           'selectbg':'lightblue', 'selectfg':'white'}

class TableCanvas(tk.Canvas):
    """ HistCanvas: diverid from wx.core.Panel """
    def __init__(self, parent, box=None, margin=(50,50,30,30), mode='grid', selmode='multi',
                 stripe=False, edit=False, rowheight=24, indexwidth=50, headerheight=30, bootstyle='default'):
        tk.Canvas.__init__ ( self, parent, bg="white", height=300, width=300 )
        self.pack(fill='both', expand=True)
        self.value = [[]]
        self.nrows = 0
        self.ncols = 0
        self.index = []
        self.columns = []
        self.colwidths = {}
        self.width = []
        self.height = []
        self.rmsk = []
        self.cmsk = []
        self.cwidth = [0]
        self.cheight = [0]
        self.dirty = True
        self.offsetx = 0
        self.offsety = 0
        self.headerh = headerheight
        self.rowheight = rowheight
        self.headerw = indexwidth
        self.stripe = stripe
        self.status = None
        self.mode = mode
        self.selmode = selmode
        self.edit = edit
        self.cmap = {}
        self.bootstyle = bootstyle
        self.on_idle()

        self.style = build_style(self.bootstyle)
        self.selection = [None, None]

        self.bind("<MouseWheel>", self.on_mousewheel)
        self.bind("<Button-1>", self.on_mousedown)
        self.bind("<ButtonRelease-1>", self.on_mouseup)
        self.bind('<Motion>', self.on_mousemove)
        self.bind("<Configure>", self.on_resize)

        self.bind("<Double-Button-1>", self.on_active)
        self.actcell = tk.Frame(self)
        self.entry = tk.Entry(self.actcell, width=0)
        self.entry.place(x=0, y=0)
        self.entry.bind("<Key>", self.on_input)
        self.activecell = None
        self.yscrollcommand = lambda x:x
        self.xscrollcommand = lambda x:x

    def on_idle(self, event=None):
        if self.dirty == True:
            self.draw()
            self.dirty = False
        self.after(100, self.on_idle)

    def on_active(self, event):
        x, y = event.x, event.y
        row, col = self.panel_to_cell(x, y, 3)
        
        if self.edit: return self.active(row, col)
        elif isinstance(row, int) and isinstance(col, int):
            self.event_generate('<<Cell-Active>>', when='tail', x=col, y=row)

    def active(self, row, col):
        self.activecell = row, col
        if isinstance(row, int) and isinstance(col, int):
            self.entry.delete(0, 'end')
            self.entry.insert(0, str(self.value[row][col]))
            self.draw()

    def on_input(self, event):
        i, j = self.activecell
        if isinstance(i, int) and isinstance(j, int):
            if event.keysym == "Return":
                self.activecell = None
                self.value[i][j] = self.entry.get()
                self.actcell.place(x=-10000, y=-10000)
                self.draw()
            elif event.keysym == "Escape":
                self.activecell = None
                self.actcell.place(x=-10000, y=-10000)
                self.draw()

    def config(self, **kwargs):
        if 'yscrollcommand' in kwargs:
            self.yscrollcommand = kwargs['yscrollcommand']
        if 'xscrollcommand' in kwargs:
            self.xscrollcommand = kwargs['xscrollcommand']
        super().config(**kwargs)
            
    def position_y(self):
        if self.nrows==0: return 0, 1
        fraction = self.offsety/self.cheight[-1]
        thumb = (self.winfo_height()-self.headerh)/self.cheight[-1]
        return fraction, fraction+thumb

    def position_x(self):
        fraction = self.offsetx/self.cwidth[-1]
        thumb = (self.winfo_width()-self.headerw)/self.cwidth[-1]
        return fraction, fraction+thumb

    def yview(self, *args):
        if self.nrows==0: return
        maxy = self.cheight[-1]+self.headerh-self.winfo_height()
        if args[0] == 'moveto':
            offsety = int(self.cheight[-1] * float(args[1]))
            self.offsety = max(0, min(offsety, maxy))
            self.yscrollcommand(*self.position_y())
            self.draw()
        elif args[0] == 'scroll':
            scale = {'units':1, 'pages':10}[args[2]]
            self.offsety += int(args[1]) * self.rowheight * scale
            self.offsety = max(0, min(self.offsety, maxy))
            self.yscrollcommand(*self.position_y())
            self.draw()
        else: return

    def xview(self, *args):
        maxx = self.cwidth[-1]+self.headerw-self.winfo_width()
        if args[0] == 'moveto':
            offsetx = int(self.cwidth[-1] * float(args[1]))
            self.offsetx = max(0, min(offsetx, maxx))
            self.xscrollcommand(*self.position_x())
            self.draw()
        elif args[0] == 'scroll':
            scale = {'units':1, 'pages':10}[args[2]]
            self.offsetx += int(args[1]) * self.rowheight * scale
            self.offsetx = max(0, min(self.offsetx, maxx))
            self.xscrollcommand(*self.position_x())
            self.draw()
        else: return
        
    def on_mousewheel(self, event):
        if self.nrows==0: return
        self.offsety -= ((event.delta>0)*2-1) * self.rowheight
        maxy = self.cheight[-1]+self.headerh-self.winfo_height()
        self.offsety = min(self.offsety, maxy)
        self.offsety = max(0, self.offsety)
        self.yscrollcommand(*self.position_y())
        self.draw()

    def build_status(self, name, row, col, ctrl, shift):
        status = {'cmd':name, 'row':row, 'col':col, 'ctrl':ctrl, 'shift':shift}
        status.update({'rbuf':copy(self.rmsk), 'cbuf':copy(self.cmsk)})
        return status

    def slider_visable(self):
        diff = lambda x: x[1] - x[0]
        if diff(self.position_y()) >= 1:
            self.yscrollcommand.__self__.grid_remove()
        else: self.yscrollcommand.__self__.grid()
        if diff(self.position_x()) >= 1:
            self.xscrollcommand.__self__.grid_remove()
        else: self.xscrollcommand.__self__.grid()
        
    def on_resize(self, event):
        self.cwidth = cumsum(self.width, self.winfo_width()-self.headerw)
        
        self.xview('scroll', '0', 'units')
        self.yview('scroll', '0', 'units')

        # print(event.width)

        self.after(10, lambda:self.xscrollcommand(*self.position_x()))
        self.after(10, lambda:self.yscrollcommand(*self.position_y()))
        self.slider_visable()
        
        
    def on_mousedown(self, event):
        x, y = event.x, event.y
        alt, ctrl, shift = [event.state&i>0 for i in (0x20000, 0x0004, 0x0001)]
        row, col = self.panel_to_cell(x, y, 3)
        if isinstance(row, int) and isinstance(col, int):
            self.event_generate('<<Cell-Select>>', when='tail', x=col, y=row)
        if self.mode=='row' and isinstance(col, int) and isinstance(row, int): col='header'
            
        # if self.seletmode == 'single': alt = ctrl = shift = False

        self.activecell = None
        self.actcell.place(x=-10000, y=-10000)
        
        
        if row=='header' and col=='header' and self.selmode=='multi':
            print('header-header')
            # for i in range(len(self.rmsk)): self.rmsk[i] = True
            # for i in range(len(self.cmsk)): self.cmsk[i] = True
            self.select(slice(None), slice(None))
        if row=='header' and isinstance(col, int) and self.mode=='grid':
            print('col', col)
            
            self.status = self.build_status('col', row, col, ctrl, shift)
            if self.selmode == 'single': self.status = None
            self.select(slice(None), col, ctrl, shift)
        if row=='header' and isinstance(col, tuple):
            print('col-sep', col[0])
            w = self.cwidth[col[0]] - self.cwidth[col[0]-1] * (col[0]>0)
            self.status = {'cmd':'col-sep',
                'i':col[0], 'w':w, 'x':x}
        # click index header
        if col=='header' and isinstance(row, int):
            print('row', row)
            self.status = self.build_status('row', row, col, ctrl, shift)
            if self.selmode == 'single': self.status = None
            self.select(row, slice(None), ctrl, shift)
        if col=='header' and isinstance(row, tuple):
            print('row-sep', row[0])
            self.status = {'cmd':'row-sep',
                'i':row[0], 'h':self.height[row[0]], 'y':y}
        # click a cell
        if isinstance(row, int) and isinstance(col, int):
            print('cell', row, col)
            # with shift
            self.status = self.build_status('cell', row, col, ctrl, shift)
            if self.selmode == 'single': self.status = None
            self.select(row, col, False, shift)
        
        self.draw()

    def config_cursor(self, cursor=None):
        if cursor == self.configure('cursor')[-1]: return
        self.config(cursor=cursor)
        posx, posy = self.position_x(), self.position_y()
        
        self.after(1, lambda:self.yscrollcommand(*posy))
        self.after(1, lambda:self.xscrollcommand(*posx))
        
    def on_mousemove(self, event):
        x, y = event.x, event.y
        row, col = self.panel_to_cell(x, y, 3)
        cursor = self.configure('cursor')[-1]

        if row=='header' and isinstance(col, tuple):
            self.config_cursor(cursor="sb_h_double_arrow")
        elif col=='header' and isinstance(row, tuple):
            self.config_cursor(cursor="sb_v_double_arrow")
        else: self.config_cursor(cursor="arrow")
        
        if self.status is None: return
        

        names = 'row', 'col', 'ctrl', 'shift', 'rbuf', 'cbuf'
        oldrow, oldcol, ctrl, shift, rbuf, cbuf = [
            self.status.get(i, None) for i in names]
        
        if self.status['cmd']=='col-sep': # adjust col width
            _i, _w, _x = [self.status[j] for j in 'iwx']
            self.width[_i] = max(_w + x - _x, 10)
            self.cwidth = cumsum(self.width, self.winfo_width()-self.headerw)
        elif self.status['cmd']=='row-sep': # adjust row height
            _i, _h, _y = [self.status[j] for j in 'ihy']
            self.height[_i] = max(_h + y - _y, self.rowheight)
            self.cheight = cumsum(self.height)
        elif self.status['cmd']=='col': # col select
            row, col = self.panel_to_cell(x, y, 0)
            newcol = {'header':0, None:self.ncols-1}.get(col, col)
            self.select(slice(None), (oldcol, newcol), ctrl, shift, rbuf, cbuf)
        elif self.status['cmd']=='row': # col select
            row, col = self.panel_to_cell(x, y, 0)
            newrow = {'header':0, None:self.ncols-1}.get(row, row)
            self.select((oldrow, newrow), slice(None), ctrl, shift, rbuf, cbuf)
        elif self.status['cmd']=='cell': # select cell
            row, col = self.panel_to_cell(x, y, 0)
            newrow = {'header':0, None:self.nrows-1}.get(row, row)
            newcol = {'header':0, None:self.ncols-1}.get(col, col)
            self.select((oldrow, newrow), (oldcol, newcol), ctrl, shift, rbuf, cbuf)
        self.draw()
            
    def on_mouseup(self, event):
        x, y = event.x, event.y
        cur = self.panel_to_cell(x, y)
        self.status = None
        
    def panel_to_cell(self, x, y, tor=0):
        # print(x, y, '>>>>>>>>>>>>>')
        ix = iy = None
        realy = y - self.headerh + self.offsety
        iy = binary_search(self.cheight, realy)
        
        if self.nrows and abs(realy - self.cheight[iy])<tor: iy=(iy, iy+1)
        elif self.nrows and abs(realy - self.cheight[iy-1])<tor: iy=(iy-1, iy)
        if y < self.headerh - tor: iy = 'header'
        # print(y, self.headerh, tor, 'yyy')
        if realy > (self.nrows and self.cheight[-1]) + tor: iy = None

        realx = x - self.headerw + self.offsetx
        ix = binary_search(self.cwidth, realx)
        if abs(realx - self.cwidth[ix])<tor: ix=(ix, ix+1)
        elif abs(realx - self.cwidth[ix-1])<tor: ix=(ix-1, ix)
        if x < self.headerw - tor: ix = 'header'
        # print(x, self.headerw, tor, 'xxx')
        if realx > self.cwidth[-1] + tor: ix = None
        # print(ix, iy)
        return iy, ix

    def set(self, value, columns=None, index=None):
        self.value = value
        self.selection = [None, None]
        self.nrows = len(value)
        self.ncols = len(value[0]) if columns is None else len(columns)
        if columns is None:
            columns = [column_labels(i+1) for i in  range(self.ncols)]
        if index is None: index = list(range(1, self.nrows+1))     
        self.columns, self.index = columns, index

        if len(self.width)!=self.ncols:
            self.width = [80 for i in range(self.ncols)]
        self.height = [self.rowheight for i in range(self.nrows)]
        
        self.cwidth = cumsum(self.width, self.winfo_width())
        self.cheight = cumsum(self.height)

        self.rmsk = [False for i in range(self.nrows)]
        self.cmsk = [False for i in range(self.ncols)]

        self.slider_visable()
        self.dirty = True

    def select(self, slir=None, slic=slice(None), ctrl=False, shift=False, rbuf=None, cbuf=None):
        if self.selmode == False: return
        if self.selmode == 'single': ctrl = shift = False
        rmsk, cmsk = self.rmsk, self.cmsk
        if not rbuf is None: snapshot(rmsk, rbuf)
        if not cbuf is None: snapshot(cmsk, cbuf)
        if not slice(None) in (slir, slic): ctrl=False

        sr = select(rmsk, slir, ctrl, shift)
        sc = select(cmsk, slic, ctrl, shift)

        # print(sr, sc)

        self.selection = (sr, sc)

    '''
    def get_selection(self):
        if self.mode=='row':
            return where(self.rmsk)
        else 
    '''
        
    def draw_headers(self, style, sr, er, sc, ec):
        offx, offy = self.offsetx, self.offsety
        if self.nrows:
            self.create_rectangle(0,0, self.headerw, self.cheight[er]+self.headerh-offy, fill=style['header'], outline='')
            for i in range(sr, er+1):
                if self.headerw==0: break
                y = self.cheight[i]
                self.create_line(0, y+self.headerh-offy, self.headerw, y+self.headerh-offy, fill=style['line'])
                self.create_text(self.headerw/2, y+self.headerh-self.height[i]/2-offy, text=self.index[i],  fill=style['bg'])
            
        self.create_rectangle(0,0, self.cwidth[ec]+self.headerw-offx, self.headerh, fill=style['header'], outline='')
        for i in range(sc, ec+1):
            if self.headerh==0: break
            x = self.cwidth[i]
            halfw = (x - (self.cwidth[i-1] if i>0 else 0))/2
            self.create_line(x+self.headerw-offx, 0, x+self.headerw-offx, self.headerh, fill=style['line'])
            self.create_text(x+self.headerw-halfw-offx, self.headerh/2, text=self.columns[i], fill=style['bg'])
        self.create_rectangle(0, 0, self.headerw, self.headerh, fill=style['header'], outline='')
        self.create_line(self.headerw, 0, self.headerw, self.headerh, fill=style['line'])
        self.create_line(0, self.headerh, self.cwidth[ec]+self.headerw-offx, self.headerh, fill=style['line'])
        
    def draw_grid(self, style, sr, er, sc, ec):
        # print(self.selection)
        offx, offy = self.offsetx, self.offsety
        index_width, col_height = self.headerw, self.headerh
        # self.create_rectangle(0, 0, self.winfo_width(), self.winfo_height(), fill='', outline=style['line'])

        box = None
        rmsk, cmsk = self.selection
        for i in range(sr, er+1):
            for j in range(sc, ec+1):
                r = index_width + self.cwidth[j]
                l = index_width + (self.cwidth[j-1] if j>0 else 0) # r - self.width[j]
                b = col_height + self.cheight[i]
                t = b - self.height[i]
                
                selected = isselected(*self.selection, i, j)                
                bg = ((style['bg'], style['stripe'])[i%2 * self.stripe], style['selectbg'])[selected]
                fg = (style['fg'], style['selectfg'])[selected]

                fg = self.cmap.get(('x',j), None) or fg
                fg = self.cmap.get((i,'x'), None) or fg
                fg = self.cmap.get((i,j), None) or fg
                
                # print(self.cwidth, self.width)
                self.create_rectangle(l-offx, t-offy, r-offx, b-offy, fill=bg, outline=style['line'] if self.mode=='grid' else '')
                self.create_text(l+3-offx, (t+b)/2-offy, text=self.value[i][j], anchor='w',  fill=fg)

            # self.create_rectangle(l+self.width[-1]+1-offx, t-offy, r+300-offx, b-offy, fill=style['bg'], outline='')
        
    def draw_active(self):
        i, j = self.activecell or (None, None)
        offx, offy = self.offsetx, self.offsety
        index_width, col_height = self.headerw, self.headerh
        if isinstance(i, int) and isinstance(j, int):
            r = index_width + self.cwidth[j]
            l = index_width + (self.cwidth[j-1] if j>0 else 0) # r - self.width[j]
            b = col_height + self.cheight[i]
            t = b - self.height[i]
            dh = max(col_height - (t-offy), 0)
            dw = max(index_width - (l-offx), 0)
            if dh > b-t or dw > r-l:
                return self.actcell.place(x=-10000, y=-10000)
            self.entry.focus()
            self.entry.place(x=-dw, y=-dh, width=r-l+1, height=b-t+(self.mode=='grid'))
            self.actcell.place(x=l-offx+dw, y=t-offy+dh, width=r-l+1-dw, height=b-t+1-dh)
        
    def draw(self, counter=[0,0]):
        self.style = build_style(self.bootstyle)
        start = time()
        self.delete('all')
        if self.ncols == 0: return
        sr, sc = self.panel_to_cell(self.headerw, self.headerh)
        er, ec = self.panel_to_cell(self.winfo_width(), self.winfo_height())
        if self.winfo_height()<self.headerh: return
        er, ec = er or self.nrows-1, ec or self.ncols-1

        if self.nrows>0: self.draw_grid(self.style, sr, er, sc, ec)
        self.draw_headers(self.style, sr, er, sc, ec)
        self.draw_active()

        counter[0] += 1
        counter[1] += time()-start
        if counter[0] == 50:
            print('frame rate:',int(50/max(0.001,counter[1])))
            counter[0] = counter[1] = 0

    def set_column_width(self, i=None, w=None, expand=0):
        # if i is None: del self.colwidths[:]
        self.width[i] = w + expand*1j
        self.cwidth = cumsum(self.width)
        self.dirty = True

    def set_cell_color(self, r='x', c='x', color='#FFFFFF'):
        if r=='x' and c=='x': self.cmap.clear()
        else: self.cmap[(r, c)] = color

    def get(self): return self.body

class Gridview(ttk.Frame):
    def __init__(self, parent, bootstyle='primary', **key):
        super().__init__(parent)
        self.view = TableCanvas(self, bootstyle=bootstyle, **key)
        self.view.pack_forget()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.view.grid(row=0, column=0, padx=1, pady=1, sticky='news')
        # self.pack(fill='both', expand=True)
        self.set = self.view.set
        self.get = self.view.get
        self.active = self.view.active
        self.set_cell_color = self.view.set_cell_color
        self.set_column_width = self.view.set_column_width
        self.select = self.view.select
        self.bind = self.view.bind

        self._vbar = ttk.Scrollbar(self,
            command=self.view.yview,
            orient='vertical',
        )
        self._vbar.grid(row=0, column=1, sticky='nsew')
        self.view.config(yscrollcommand=self._vbar.set)

        self._hbar = ttk.Scrollbar(self,
            command=self.view.xview,
            orient='horizontal',
        )
        self._hbar.grid(row=1, column=0, sticky='nsew')
        self.view.config(xscrollcommand=self._hbar.set)

        self._hbar.bind("<MouseWheel>",
            lambda e:self.view.xview('scroll', str(((e.delta>0)*2-1)*-4), 'units'))

    def on_select(self, event):
        print('event', event.x, event.y)

    def on_active(self, event):
        print('active', event.x, event.y)
        
    @property
    def selection(self):
        r, c = self.view.selection
        if self.view.mode=='grid':
            return get_selection(r), get_selection(c)
        if self.view.mode=='row':
            return get_selection(r)
    
if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    
    data = np.random.rand(50,20).round(3)
    data = pd.read_csv('PDF#05-0628#石盐.csv', index_col=0)[:]
    
    # data = pd.DataFrame(data, columns=['columns_%d'%i for i in range(5)])

    root = ttk.Window()
    ttk.Style()
    grid = Gridview(root, mode='grid', selmode='multi',
                    indexwidth=80, rowheight=18, stripe=True, edit=True, bootstyle='primary')
    '''
                    , bootstyle=None,
                    mode='row', rowheight=18, headerheight=30,
                    indexwidth=False, stripe=True, edit=False)
    '''
    grid.set_cell_color('x', 1, '#FF0000')
    grid.set_cell_color(1, 'x', '#00FF00')
    grid.pack(fill='both', expand=True)
    grid.set(data.values, columns=data.columns, index=data.index)
    grid.set_column_width(1, 60, expand=1)
    # grid.set([], ['a', 'b', 'c'], None)
    root.mainloop()
