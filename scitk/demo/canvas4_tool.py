import sys
sys.path.append('../../')
from skimage.data import astronaut, camera
from scitk.canvas import ICanvas
from sciapp.action import Tool
import tkinter as tk

class TestTool(Tool):
    def __init__(self): Tool.__init__(self)
    
    def mouse_down(self, image, x, y, btn, **key):
        print('x:%d y:%d btn:%d ctrl:%s alt:%s shift:%s'%
              (x, y, btn, key['ctrl'], key['alt'], key['shift']))
        
    def mouse_up(self, image, x, y, btn, **key):
        pass
        
    def mouse_move(self, image, x, y, btn, **key):
        pass
    
    def mouse_wheel(self, image, x, y, d, **key):
        image.img[:] = image.img + d
        key['canvas'].update()


if __name__ == '__main__':
    app = tk.Tk()
    app.withdraw()
    frame = tk.Toplevel(app)
    canvas = ICanvas(frame, autofit=True)
    canvas.set_img(camera())
    canvas.set_tool(TestTool())
    canvas.pack(fill="both", expand=True)
    app.mainloop()
