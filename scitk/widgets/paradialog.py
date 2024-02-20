import tkinter as tk
from tkinter import ttk
from .normal import *
#from .advanced import *
#from .histpanel import HistPanel
#from .curvepanel import CurvePanel
#from .threpanel import ThresholdPanel

widgets = { 'ctrl':None, 'slide':FloatSlider, int:NumCtrl, 'path':'PathCtrl',
            float:NumCtrl, 'lab':Label, bool:Check, str:TextCtrl, list:Choice,
            'color':ColorCtrl, 'cmap':'CMapSelPanel', 'any':'AnyType', 'chos':Choices, 'hist':'ThresholdPanel',
            'curve':'CurvePanel', 'img':'ImageList', 'tab':'TableList', 'field':'TableField', 'fields':'TableFields'}

def add_widget(key, value): widgets[key] = value

class ParaDialog(ttk.Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        self.tus = []
        self.on_ok = self.on_cancel = self.on_help = None
        self.handle = print
        self.ctrl_dic = {}
        self.para = {}
        self.modal = True
        self.status = None
        # super().bind("<Configure>", lambda e: self.on_pack())
        self.after(100, self.pack)
        super().bind('<<ParameterEvent>>', self.para_changed)

    def commit(self, state):
        self.status = state == 'ok'
        if state == 'ok' and self.on_ok:
            self.on_ok()
        elif state == 'cancel' and self.on_cancel:
            self.on_cancel()
        self.destroy()

    def add_confirm(self, modal):
        frame = ttk.Frame(self)
        ttk.Frame(frame).pack(side='left', fill='x', expand=True)
        self.btn_ok = ttk.Button(frame, text='OK', command=lambda: self.commit('ok'))
        self.btn_ok.pack(side='left', padx=5, pady=5)

        self.btn_cancel = ttk.Button(frame, text='Cancel', command=lambda: self.commit('cancel'))
        self.btn_cancel.pack(side='left', padx=5, pady=5)

        self.btn_help = ttk.Button(frame, text='Help', command=self.on_help)
        self.btn_help.pack(side='left', padx=5, pady=5)
        frame.pack(fill='x')

    def init_view(self, items, para, preview=False, modal=True, app=None):
        self.para = para
        self.modal = modal
        for item in items:
            self.add_ctrl_(widgets[item[0]], item[1], item[2:], app=app)
        if preview:
            self.add_ctrl_(Check, 'preview', ('preview',), app=app)
        self.reset(para)
        for p in self.ctrl_dic:
            if p in para:
                para[p] = self.ctrl_dic[p].get()
        self.add_confirm(modal)
        

    def OnDestroy(self):
        self.handle = print
        self.on_cancel = self.on_ok = self.on_help = None
        del self.ctrl_dic

    def parse(self, para):
        self.add_ctrl_(widgets[para[0]], *para[1:])

    def add_ctrl_(self, Ctrl, key, p, app=None):
        ctrl = Ctrl(self, *p, app=app)

        if p[0] is not None:
            self.ctrl_dic[key] = ctrl
        # if hasattr(ctrl, 'bind'):
        pre = ctrl.prefix if hasattr(ctrl, 'prefix') else None
        post = ctrl.postfix if hasattr(ctrl, 'postfix') else None
        # print('haha')
        self.tus.append((pre, post))

    def pack(self):
        maxt, maxu = 0, 0
        for t, u in self.tus:
            if t is not None:
                maxt = max(maxt, t.winfo_width())
            if u is not None:
                maxu = max(maxu, u.winfo_width())
                
        for t, u in self.tus:
            if t is not None:
                t.configure(width=int(maxt*0.15))
            if u is not None:
                u.configure(width=int(maxu*0.15))
            
    def para_check(self, para, key):
        pass

    def para_changed(self, event):
        # print('parameter changed', event.state, event.widget)
        if event.state==0:
            return self.btn_ok.config(state='disable')
        else: self.btn_ok.config(state='normal')

        obj = event.widget
        key = ''
        para = self.para
        for p in self.ctrl_dic:
            if p in para:
                para[p] = self.ctrl_dic[p].get()
            if self.ctrl_dic[p] == event.widget:
                key = p
        
        self.para_check(para, key)
        if 'preview' not in self.ctrl_dic: return
        if not self.ctrl_dic['preview'].get():
            if key == 'preview' and self.on_cancel is not None:
                return self.on_cancel()
            else: return
        self.handle(para)

    def reset(self, para=None):
        if para is not None:
            self.para = para
        for p in self.para.keys():
            if p in self.ctrl_dic:
                self.ctrl_dic[p].set(self.para[p])

    def get_para(self):
        return self.para

    def bind(self, tag, f):
        if tag == 'parameter':
            self.handle = f if f is not None else print
        if tag == 'commit':
            self.on_ok = f
        if tag == 'cancel':
            self.on_cancel = f
        if tag == 'help':
            self.on_help = f

    def show(self):
        self.pack()
        if self.modal:
            self.grab_set()
            self.wait_window()
            print(self.status)
            return self.status
        else:
            self.deiconify()

    def __del__(self):
        print('panel config deleted!')

def get_para(para, view, title='Parameter', parent=None):
    pd = ParaDialog(parent, title)
    pd.init_view(view, para)
    pd.pack()
    rst = pd.ShowModal()
    pd.Destroy()
    return rst == 5100

if __name__ == '__main__':
    para = {'name':'yxdragon', 'age':10, 'h':1.72, 'w':70, 'sport':True, 'sys':'Mac', 'lan':['C/C++', 'Python'], 'c':(255,0,0)} 

    view = [('lab', 'lab', 'This is a questionnaire'),
            (str, 'name', 'name', 'please'), 
            (int, 'age', (0,150), 0, 'age', 'years old'),
            (float, 'h', (0.3, 2.5), 2, 'height', 'm'),
            ('slide', 'w', (1, 150), 0, 'weight','kg'),
            (bool, 'sport', 'do you like sport'),
            (list, 'sys', ['Windows','Mac','Linux'], str, 'favourite', 'system'),
            ('chos', 'lan', ['C/C++','Java','Python'], 'lanuage you like(multi)'),
            ('color', 'c', 'which', 'you like')]

    app = ttk.Window('parameter')
    app.withdraw()
    pd = ParaDialog(app, 'nothing')
    pd.init_view(view, para, preview=True, modal=False)
    # pd.on_pack()
    app.mainloop()
