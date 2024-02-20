import sys; sys.path.append('../../')
from scipy.ndimage import gaussian_filter
from scitk.canvas import CanvasFrame
from sciapp.action import ImgAction

import tkinter as tk
import ttkbootstrap as ttk

class Gaussian(ImgAction):
    title = 'Gaussian'
    note = ['auto_snap', 'preview']
    para = {'sigma':2}
    view = [(float, 'sigma', (0, 30), 1, 'sigma', 'pix')]

    def run(self, ips, img, snap, para):
        gaussian_filter(snap, para['sigma'], output=img)

class Undo(ImgAction):
    title = 'Undo'
    def run(self, ips, img, snap, para):
        ips.swap()

if __name__=='__main__':
    from skimage.data import camera, astronaut
    from skimage.io import imread

    app = ttk.Window()
    style = ttk.Style(theme='darkly')
    app.withdraw()
    
    ca = CanvasFrame(app, autofit=False)
    ca.set_img(camera())
    bar = ca.add_menubar()
    bar.load(('menu',[('Filter',[('Gaussian', Gaussian),
                                 ('Unto', Undo)]),
                      ]))
    app.mainloop()
