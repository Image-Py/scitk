import sys
sys.path.append('../../')
from skimage.data import astronaut, camera
from scitk.canvas import MCanvas
import tkinter as tk

def mcanvas_test():
    frame = tk.Toplevel(app)
    frame.title('gray test1')
    canvas = MCanvas(frame, autofit=True)
    canvas.set_img(astronaut())
    canvas.set_cn((0,1,2))
    canvas.pack(fill="both", expand=True)

def channels_test():
    frame = tk.Toplevel(app)
    frame.title('gray test2')
    canvas = MCanvas(frame, autofit=True)
    canvas.set_img(astronaut())
    canvas.set_cn(0)
    canvas.pack(fill="both", expand=True)

def sequence_test():
    frame = tk.Toplevel(app)
    frame.title('gray test3')
    canvas = MCanvas(frame, autofit=True)
    canvas.set_imgs([astronaut(), 255-astronaut()])
    canvas.set_cn(0)
    canvas.pack(fill="both", expand=True)

if __name__ == '__main__':
    app = tk.Tk()
    app.withdraw()
    mcanvas_test()
    sequence_test()
    channels_test()
    app.mainloop()
