import sys
sys.path.append('../../')
from skimage.data import astronaut, camera
from sciapp.object import Image
from scitk.canvas import ICanvas, MCanvas
import tkinter as tk

def image_canvas_test():
    obj = Image()
    obj.img = camera()
    obj.cn = 0

    frame = tk.Toplevel(app)
    frame.title('gray test')
    canvas = ICanvas(frame, autofit=True)
    canvas.set_img(obj)
    canvas.pack(fill="both", expand=True)

def image_mcanvas_test():
    obj = Image()
    obj.imgs = [astronaut(), 255-astronaut()]
    obj.cn = 0

    frame = tk.Toplevel(app)
    frame.title('gray test')
    canvas = MCanvas(frame, autofit=True)
    canvas.set_img(obj)
    canvas.pack(fill="both", expand=True)

if __name__ == '__main__':
    app = tk.Tk()
    app.withdraw()
    image_canvas_test()
    image_mcanvas_test()
    app.mainloop()
