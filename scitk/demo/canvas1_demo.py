import sys
sys.path.append('../../')
from skimage.data import astronaut, camera
from numpy.fft import fft2, fftshift
from scitk.canvas import ICanvas as Canvas
from sciapp.object import Image
import tkinter as tk
import ttkbootstrap as ttk

def gray_test():
    frame = ttk.Toplevel(app)
    frame.title('gray test')
    canvas = Canvas(frame, autofit=True)
    canvas.set_img(camera())
    canvas.pack(fill="both", expand=True)

def rgb_test():
    frame = ttk.Toplevel(app)
    frame.title('gray test')
    canvas = Canvas(frame, autofit=True)
    canvas.set_img(astronaut())
    canvas.set_cn((0,1,2))
    canvas.pack(fill="both", expand=True)

def rgb_gray_blend():
    frame = ttk.Toplevel(app)
    frame.title('blend')
    canvas = Canvas(frame, autofit=True)
    canvas.set_img(astronaut())
    canvas.set_cn((2,-1,-1))
    canvas.set_img(camera(), True)
    canvas.set_cn(0, True)
    canvas.set_mode(0.5)
    canvas.pack(fill="both", expand=True)

def complex_test():
    frame = ttk.Toplevel(app)
    frame.title('fft')
    canvas = Canvas(frame, autofit=True)
    canvas.set_img(fftshift(fft2(camera())))
    canvas.set_rg((0,31015306))
    canvas.set_log(True)
    canvas.pack(fill="both", expand=True)

if __name__ == '__main__':
    app = tk.Tk()
    app.withdraw()
    gray_test()
    rgb_test()
    rgb_gray_blend()
    complex_test()
    app.mainloop()
    
    
