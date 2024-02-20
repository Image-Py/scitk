import tkinter as tk

def hot_key(txt):
    sep = txt.split('-')
    acc, code = None, None
    if 'Ctrl' in sep:
        acc = 'Control'
    if 'Alt' in sep:
        acc = 'Alt'
    if 'Shift' in sep:
        acc = 'Shift'
    fs = ['F%d' % i for i in range(1, 13)]
    if sep[-1] in fs:
        code = f'<{acc}-{sep[-1]}>'
    elif len(sep[-1]) == 1:
        code = f'<{acc}-{sep[-1].lower()}>'
    return code

class MenuBar(tk.Menu):
    def __init__(self, app):
        tk.Menu.__init__(self, app)
        self.app = app
        app.config(menu=self)

    def parse(self, ks, vs, pt, short, rst):
        if isinstance(vs, list):
            menu = tk.Menu(pt, tearoff=0)
            for kv in vs:
                if kv == '-':
                    menu.add_separator()
                else:
                    self.parse(*kv, menu, short, rst)
            pt.add_cascade(label=ks, menu=menu)
        else:
            f = lambda p=vs: p().start(self.app)
            if ks in short:
                rst.append((hot_key(short[ks]), f))
            pt.add_command(label=ks, command=f)

    def load(self, data, shortcut={}):
        rst = []
        for k, v in data[1]:
            self.parse(k, v, self, shortcut, rst)
        return rst

if __name__ == '__main__':
    class P:
        def __init__(self, name):
            self.name = name

        def start(self, app):
            print(self.name)

        def __call__(self):
            return self

    data = ('menu', [
        ('File', [
            ('Open', P('O')),
            ('-'),
            ('Close', P('C'))]),
        ('Edit', [
            ('Copy', P('C')),
            ('A', [
                ('B', P('B')),
                ('C', P('C'))]),
            ('Paste', P('P'))])])

    app = tk.Tk()
    menubar = MenuBar(app)
    acc = menubar.load(data, {'Open': 'Ctrl-O'})
    for key, command in acc:
        app.bind_all(key, lambda event, command=command: command())
    app.config(menu=menubar)
    app.mainloop()
