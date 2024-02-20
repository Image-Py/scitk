import sys
sys.path.append('../../')
from sciapp.object import mark2shp, Layer, json2shp
from sciapp.action import ShapeTool, PointEditor, LineEditor, PolygonEditor, \
RectangleEditor, EllipseEditor, FreeLineEditor, FreePolygonEditor, BaseEditor
from scitk.canvas import VectorFrame
from scitk.plugins.filters import Gaussian
import tkinter as tk
import ttkbootstrap as ttk

ellipse = {'type':'ellipse', 'body':(100,100,100,-50,1)}
rectangles = {'type':'rectangles', 'body':[(100,100,80,50),(200,200,80,100)]}
layer = {'type':'layer', 'num':-1, 'color':(0,0,255), 'fill':False, 'body':[rectangles, ellipse]}

    
if __name__ == '__main__':
    app = tk.Tk()
    app.withdraw()
    frame = VectorFrame(app)
    frame.set_shp(mark2shp(layer))
    bar = frame.add_toolbar()
    bar.add_tool('Select', ShapeTool)
    bar.add_tool('Editor', BaseEditor)
    bar.add_tool('Point', PointEditor)
    bar.add_tool('Line', LineEditor)
    bar.add_tool('Polygon', PolygonEditor)
    bar.add_tool('Rectangle', RectangleEditor)
    bar.add_tool('Ellipse', EllipseEditor)
    bar.add_tool('FreeLine', FreeLineEditor)
    bar.add_tool('FreePolygon', FreePolygonEditor)
    app.mainloop()
