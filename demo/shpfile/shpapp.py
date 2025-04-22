import sys; sys.path.append('../../')

import ttkbootstrap as ttk
import scitk.ttk as sttk

print(sttk.ColorBox)
from scitk.widgets.toolbar import ToolBar
from scitk.canvas import VCanvas as Canvas
import numpy as np
import matplotlib.pyplot as plt

import geopandas as gpd

from sciapp.object import Layer
from sciapp.util import json2shp

cmap = []
for i in plt.colormaps()[::-1]:
    cm = plt.get_cmap(i)
    if i[-2:]=='_r': continue
    vs = np.linspace(0, cm.N, 256, endpoint=False)
    lut = cm(vs.astype(np.uint8), bytes=True)[:,:3]
    cmap.append((i, lut))

def shp2mark(df):
    feats = df.geometry.__geo_interface__['features']
    feats = [json2shp(i['geometry']) for i in feats]
    return Layer(feats, color=(255,0,0), lstyle='-o')
    
    
class MainFrame(ttk.Frame):
    def __init__(self, parent, **key):
        super().__init__(parent, **key)

        toolbar = self.toolbar = ToolBar(self)
        toolbar.add_tools('IO', [('Open', None, print),
                                 ('Save', None, print)], True)

        toolbar.add_tools('Browse', [('Move', None, print),
                                     ('Auto Fit', None, print)], True)
        
        toolbar.add_tools('Select', [('Rectangle', None, print),
                                     ('Polygon', None, print),
                                     ('Line', None, print),
                                     ('Point', None, print),
                                     ('Invert', None, print)], True)

        toolbar.add_tools('LUT', [('Unique Value', None, print),
                                 ('xxx', None, print)], True)
        
        toolbar.pack(fill='x', side='top')

        self.status = ttk.Label(self)
        self.status.config(text='状态栏')
        self.status.pack(side='bottom', fill='x')
        ttk.Separator(self).pack(side='bottom', fill='x')

        panebook = ttk.PanedWindow(self, orient='horizontal')
        self.canvas = Canvas(panebook)
        # self.canvas.pack(side='left', fill='both', expand=True)

        # linecolor, 属性映射，field, unique|max-min|std, cmap
        self.features = ttk.Frame(panebook)
        topframe = ttk.Frame(self.features)
        topframe.pack(side='top')
        ttk.Label(topframe, text='Pure Color', bootstyle='primary').pack(side='left')
        
        self.box_color = sttk.ColorBox(topframe)
        self.box_color.pack(side='left', padx=3, pady=5)

        ttk.Label(topframe, text='   Property Map', bootstyle='primary').pack(side='left')
        self.comb_field = ttk.Combobox(topframe, width=10, values=['Undefined', 'Province'])
        self.comb_field.pack(side='left', padx=3, pady=5)
        
        self.comb_method = ttk.Combobox(topframe, width=10, values=['Max-Min', 'Mean-Std', 'Unique'])
        self.comb_method.pack(side='left', padx=3, pady=5)

        self.box_cmap = sttk.ColorMapBox(topframe, cmap)
        self.box_cmap.pack(side='left', padx=3, pady=5)

        self.table = table = sttk.Gridview(self.features, indexwidth=50)
        # table.set([], columns=['Name'])
        # table.set_column_width(0, 80, 1)
        table.pack(fill='both', expand=True, padx=1, pady=1)

        panebook.add(self.canvas, weight=2)
        panebook.add(self.features, weight=0)
        panebook.pack(fill='both', expand=True)
        
        '''
        rp = self.rpanel = sttk.Panedbook(self)

        panel = rp.add('Feature Table', weight=1)
        lab_lst = sttk.Gridview(panel, indexwidth=False)
        lab_lst.set([], columns=['Name'])
        lab_lst.set_column_width(0, 80, 1)
        lab_lst.pack(fill='both', expand=True, padx=1, pady=1)
    
        rp.config(width=200)
        rp.pack(side='right', fill='y')
        '''

    def set_vector(self, shp):
        self.shp = shp
        shp = shp[[i for i in shp.columns if i!='geometry']]
        self.table.set(shp.values, columns=shp.columns, index=shp.index)

        self.canvas.set_shp(shp2mark(self.shp))

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

    shp = gpd.read_file('lines.json', encoding='utf-8')
    
    app = ttk.Window('标注工具')
    # ttk.Style('darkly')
    frame = MainFrame(app)
    frame.pack(fill='both', expand=True)
    frame.set_vector(shp)
    app.mainloop()
    
