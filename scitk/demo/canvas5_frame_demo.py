import sys
sys.path.append('../../')

from skimage.data import astronaut, camera
from scitk.canvas import CanvasFrame, CanvasNoteFrame
import tkinter as tk

def canvas_frame_test():
    cf = CanvasFrame(app, autofit=True)
    cf.set_imgs([camera(), 255-camera()])

def canvas_note_test():
    cnf = CanvasNoteFrame(app)
    cv1 = cnf.add_canvas()
    cv1.set_img(camera())
    cv2 = cnf.add_canvas()
    cv2.set_img(astronaut())
    cv2.set_cn((2,1,0))

if __name__ == '__main__':
    app = tk.Tk()
    app.withdraw()
    canvas_frame_test()
    canvas_note_test()
    app.mainloop()
