import sys
sys.path.append('../../')
from sciapp.object import mark2shp, Layer, json2shp
from sciapp.action import PolygonROI, LineROI, PointROI, EllipseROI, RectangleROI, FreeLineROI, FreePolygonROI
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
    frame.canvas.set_img(camera())
    roi = ROI([Line([(0,0),(100,100),(300,500)])])
    frame.canvas.image.roi = roi
    bar = frame.add_toolbar()
    
    bar.add_tool('Point', PointROI)
    bar.add_tool('Line', LineROI)
    bar.add_tool('Polygon', PolygonROI)
    bar.add_tool('Rectangle', RectangleROI)
    bar.add_tool('Ellipse', EllipseROI)
    bar.add_tool('Freeline', FreeLineROI)
    bar.add_tool('FreePolygon', FreePolygonROI)
    app.mainloop()
