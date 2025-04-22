import tkinter as tk
from tkinter import ttk
import numpy as np

class HistPanel(tk.Frame):
    """ HistCanvas: derived from tk.Frame """
    def __init__(self, parent, hist=None, size=(256, 80), app=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.hist = hist
        self.w, self.h = size
        self.canvas = tk.Canvas(self, width=self.w, height=self.h, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.x1, self.x2 = 0, self.w-1

        self.bind("<Configure>", lambda e: self.update())
        # self.update()

    def update(self): self.draw()

    def set(self, hist):
        self.hist = (hist*self.h/hist.max())
        self.logh = (np.log(self.hist+1.0))*(self.h/(np.log(self.h+1)))
        self.update()

    def set_lim(self, x1, x2):
        self.x1, self.x2 = x1, x2
        self.update()

    def draw(self):
        self.canvas.delete("all")
        if self.hist is not None:
            # Adjust the histogram to fit the number of pixels in width
            hist = self.logh[np.linspace(0, len(self.hist)-1, self.w, dtype=np.int16)]
            # Draw log-scaled histogram
            for i in range(self.w):
                self.canvas.create_line(i, self.h, i, self.h - hist[i], fill='#C8C8C8')
            # Draw the original histogram scaled to the window height
            hist = self.hist[np.linspace(0, len(self.hist)-1, self.w, dtype=np.int16)]
            for i in range(self.w):
                self.canvas.create_line(i, self.h, i, self.h - hist[i], fill='#646464')
            # Draw limit lines
            self.canvas.create_line(self.x1, self.h-1, self.x2, 0, fill='black')
        # Draw the border
        self.canvas.create_rectangle(0, 0, self.w-1, self.h-1, outline='black')

# Example usage:
if __name__ == '__main__':
    root = tk.Tk()
    hist_canvas = HistCanvas(root, size=(300,100))
    hist_canvas.set(np.random.rand(256))
    hist_canvas.pack(fill='both')
    root.mainloop()