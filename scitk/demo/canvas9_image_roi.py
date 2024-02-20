import sys
sys.path.append('../../')
from skimage.data import astronaut, camera
from scitk.canvas import ICanvas
from sciapp.action import Tool
from sciapp.object import ROI, Line
import tkinter as tk
import ttkbootstrap as ttk

if __name__ == '__main__':
    app = ttk.Window('ROI')
    canvas = ICanvas(app, autofit=True)
    canvas.set_img(camera())
    roi = ROI([Line([(0,0),(100,100),(300,500)])])
    canvas.image.roi = roi
    canvas.pack(fill='both', expand=True)
    app.mainloop()
