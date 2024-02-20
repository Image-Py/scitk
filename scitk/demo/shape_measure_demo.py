import sys
sys.path.append('../../')
from sciapp.action import DistanceTool, AngleTool, SlopeTool, AreaTool, CoordinateTool
from scitk.canvas import CanvasFrame
from skimage.data import astronaut, camera
from sciapp.object import ROI, Line
import tkinter as tk
import ttkbootstrap as ttk

ellipse = {'type':'ellipse', 'body':(100,100,100,-50,1)}
rectangles = {'type':'rectangles', 'body':[(100,100,80,50),(200,200,80,100)]}
layer = {'type':'layer', 'num':-1, 'color':(0,0,255), 'fill':False, 'body':[rectangles, ellipse]}

if __name__ == '__main__':
    app = tk.Tk()
    app.withdraw()
    frame = CanvasFrame(app)
    bar = frame.add_toolbar()
    bar.add_tool('Coordinate', CoordinateTool)
    bar.add_tool('Distance', DistanceTool)
    bar.add_tool('Angle', AngleTool)
    bar.add_tool('Slop', SlopeTool)
    bar.add_tool('Area', AreaTool)
    frame.canvas.set_img(camera())
    app.mainloop()
