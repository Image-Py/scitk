import numpy as np
from math import sin, cos
from sciapp import Source

point = {'type':'point', 'color':(255,0,0), 'lw':1, 'body':(10,10)}
points = {'type':'points', 'color':(255,0,0), 'lw':1, 'body':[(10,10),(100,200)]}
line = {'type':'line', 'color':(255,0,0), 'lw':1, 'style':'-', 'body':[(10,10),(100,200),(200,200)]}
lines = {'type':'lines', 'color':(255,0,0), 'lw':1, 'style':'-', 'body':[[(10,10),(100,200),(200,200)],[(150,10),(50,250)]]}
polygon = {'type':'polygon', 'color':(255,0,0), 'fcolor':(255,255,0), 'lw':1, 'style':'o', 'body':[(10,10),(100,200),(200,200)]}
polygons = {'type':'polygons', 'color':(255,0,0), 'fcolor':(255,255,0,30), 'fill':False, 'lw':1, 'style':'o', 'body':[[(10,10),(100,200),(200,200)],[(150,10),(50,250),(288,0)]]}
circle = {'type':'circle', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':False, 'body':(100,100,50)}
circles = {'type':'circles', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':False, 'body':[(100,100,50),(300,300,100)]}
ellipse = {'type':'ellipse', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':False, 'body':(100,100,100,50,1)}
ellipses = {'type':'ellipses', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':False, 'body':[(100,100,100,50,1),(200,250,50,100,3.14)]}
rectangle = {'type':'rectangle', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':True, 'body':(100,100,80,50)}
rectangles = {'type':'rectangles', 'color':(255,0,0), 'fcolor':(255,255,0), 'fill':False, 'body':[(100,100,80,50),(200,200,80,100)]}
text = {'type':'text', 'color':(255,255,0), 'fcolor':(0,0,0), 'lw':8, 'fill':True, 'body':(100,200,'id=0')}
texts = {'type':'texts', 'color':(255,255,0), 'fcolor':(0,0,0), 'lw':8, 'fill':True, 'body':[(100,200,'id=0'),(180,250,'id=1')]}

layer = {'type':'layer', 'num':-1, 'clolor':(255,255,0), 'fcolor':(255,255,255), 'fill':False, 
            'body':[point, points, line, lines, polygon, polygons, circle, circles, ellipse, ellipses, rectangle, rectangles, text, texts]}
        
layers = {'type':'layers', 'num':-1, 'clolor':(255,255,0), 'fcolor':(255,255,255), 'fill':False, 
    'body':{1:points, 2:line, 3:layer}}

def cross(ori, cont, win, cell):
    kx = (cont[2]-cont[0])/(ori[2]-ori[0])
    ky = (cont[3]-cont[1])/(ori[3]-ori[1])
    ox = cont[0] - ori[0]*kx
    oy = cont[1] - ori[1]*kx
    cell = [cell[0]*kx+ox, cell[1]*ky+oy, 
        cell[2]*kx+ox, cell[3]*kx+oy]
    if cell[0]>win[2] or cell[2]<win[0]: return 0
    if cell[1]>win[3] or cell[3]<win[1]: return 0
    l = (cell[2]-cell[0])**2 + (cell[3]-cell[1])**2
    return max(int(l ** 0.5), 5)

def update_style(style, shp):
    if shp.color: style['color'] = "#%02x%02x%02x" % shp.color[:3]
    if shp.tcolor: style['tcolor'] = "#%02x%02x%02x" % shp.tcolor[:3]
    if shp.fcolor: style['fcolor'] = "#%02x%02x%02x" % shp.fcolor[:3]
    if not shp.size is None: style['size'] = shp.size
    if not shp.font is None: style['font'] = shp.font
    if not shp.lw is None: style['lw'] = shp.lw
    if shp.fill is False: style['fcolor'] = ''
    
def plot(pts, dc, f, style, **key):
    oribox, conbox, winbox = key['oribox'], key['conbox'], key['winbox']
    sap = cross(oribox, conbox, winbox, pts.box)
    if sap == 0: return

    update_style(style, pts)    
    if pts.dtype == 'point':
        x, y =  f(*pts.body)
        r = pts.r or 2
        dc.create_oval(x-r, y-r, x+r, y+r, fill=style['color'], outline=style['color'])
        
    elif pts.dtype in {'points','line'}:
        lst, plst = [], []
        r = pts.r or 2
        x, y = f(*pts.body.T[:2])
        xy = np.array([x, y]).T.tolist()
        # lst = np.array([x-r, y-r, x+r, y+r]).T.tolist()
        isline = pts.lstyle and '-' in pts.lstyle
        ispoint = pts.lstyle and 'o' in pts.lstyle
        if pts.dtype == 'polygon':
            dc.create_polygon(xy, fill=style['fcolor'], outline=style['color'], width=style['lw'])
        
        if isline or pts.dtype == 'line':
            if len(xy)>=2: dc.create_line(xy, fill=style['color'], width=style['lw'])
        
        if pts.dtype=='points' or ispoint:
            for x, y in xy:
                dc.create_oval(x-r, y-r, x+r, y+r, fill=style['color'], outline=style['color'])
            
    elif pts.dtype in {'lines','polygon', 'polygons'}:
        body, lst, plst = [], [], []
        if pts.dtype != 'polygons':
            body = pts.body
        else:
            for i in pts.body: body.extend(i)
        r = 2
        for i in body:
            if len(i)>sap:
                idx = np.linspace(0, len(i), min(len(i), sap), False, dtype=np.uint16)
                i = i[idx]
            x, y = f(*i.T[:2])
            xy = np.array((x,y)).T.ravel().tolist()
            # ps = np.array((x-r, y-r, x+r, y+r)).T.tolist()
            # lst.append(ps)
            plst.append(xy)
        isline = pts.lstyle and '-' in pts.lstyle
        ispoint = pts.lstyle and 'o' in pts.lstyle
        if pts.dtype in {'polygon', 'polygons'}:
            for poly in plst:
                dc.create_polygon(poly, fill=style['fcolor'], outline=style['color'], width=style['lw'])
        
        if isline or pts.dtype == 'lines':
            for poly in plst:
                dc.create_line(poly, fill=style['color'], width=style['lw'])
        
        if ispoint:
            for poly in plst:
                for x,y in poly:
                    dc.create_oval(x-r, y-r, x+r, y+r, fill=style['color'], outline=style['color'])

def draw_circle(pts, dc, f, style, **key):
    update_style(style, pts)
    if pts.dtype == 'circle':
        x, y ,r = pts.body
        x, y =  f(x, y)
        r = r*key['k']
        dc.create_oval(x-r, y-r, x+r, y+r, fill=style['fcolor'], outline=style['color'], width=style['lw'])
    if pts.dtype == 'circles':
        lst = []
        x, y, r = pts.body.T
        x, y = f(x, y)
        r = r * key['k']
        lst = np.vstack([x-r, y-r, x+r, y+r]).T
        for circle in lst.tolist():
            dc.create_oval(*circle, fill=style['fcolor'], outline=style['color'], width=style['lw'])


def make_ellipse(l1, l2, ang):
    m = np.array([[l1*cos(-ang),-l2*sin(-ang)],
                 [l1*sin(-ang),l2*cos(-ang)]])
    a = np.linspace(0, np.pi*2, 36)
    xys = np.array((np.cos(a), np.sin(a)))
    return np.dot(m, xys).T

def draw_ellipse(pts, dc, f, style, **key):
    update_style(style, pts)

    if pts.dtype == 'ellipse':
        x, y ,l1, l2, a = pts.body
        elp = make_ellipse(l1,l2,a) + (x,y)
        elp = np.vstack(f(*elp.T[:2])).T.ravel().tolist()
        dc.create_polygon(elp, fill=style['fcolor'], outline=style['color'], width=style['lw'])
    if pts.dtype == 'ellipses':
        lst = []
        for x, y, l1, l2, a in pts.body:
            elp = make_ellipse(l1,l2,a) + (x,y)
            elp = np.vstack(f(*elp.T[:2])).T.ravel().tolist()
            dc.create_polygon(elp, fill=style['fcolor'], outline=style['color'], width=style['lw'])
            # lst.append(np.vstack(f(*elp.T[:2])).T)
        # dc.DrawPolygonList(lst)

def draw_rectangle(pts, dc, f, style, **key):
    update_style(style, pts)

    if pts.dtype == 'rectangle':
        x, y, w, h = pts.body
        w, h = f(x+w, y+h)
        x, y = f(x, y)
        dc.create_rectangle(x, y, w, h, fill=style['fcolor'], outline=style['color'], width=style['lw'])
    if pts.dtype == 'rectangles':
        x, y, w, h = pts.body.T
        w, h = f(x+w, y+h)
        x, y = f(x, y)
        lst = np.vstack((x,y,w,h)).T.tolist()
        for rect in lst:
            dc.create_rectangle(*rect, fill=style['fcolor'], outline=style['color'], width=style['lw'])

def draw_text(pts, dc, f, style, **key):
    update_style(style, pts)

    if pts.dtype == 'text':
        (x, y), text = pts.body, pts.txt
        ox, oy = pts.offset
        x, y = f(x, y)
        dc.create_text(x+1+ox, y+1+oy, text=text, fill=style['tcolor'], font=(style['font'], style['size']), anchor='nw')
        if not pts.lstyle is None:
            dc.create_oval(x+ox-2, y+oy-2, 4, 4, fill=style['color'], outline=style['color'])
    if pts.dtype == 'texts':
        tlst, clst, elst = [], [], []
        x, y = pts.body.T
        ox, oy = pts.offset
        tlst = pts.txt

        x, y = f(x, y)
        x += ox; y += oy;
        r = x * 0 + 4
        xy = np.array((x+1, y+1)).T.tolist()
        for (x,y), text in zip(xy, tlst):
            dc.create_text(x, y, text=text, fill=style['tcolor'], font=(style['font'], style['size']), anchor='nw')
            if pts.fill:
                dc.create_oval(x-2, y-2, x+2, y+2, fill=style['color'], outline=style['color'])


draw_dic = {'points':plot, 'point':plot, 'line':plot, 
            'polygon':plot, 'lines':plot, 'polygons':plot, 
            'circle':draw_circle, 'circles':draw_circle, 
            'ellipse':draw_ellipse, 'ellipses':draw_ellipse, 
            'rectangle':draw_rectangle, 'rectangles':draw_rectangle, 
            'text':draw_text, 'texts':draw_text}

def draw(obj, dc, f, style, **key): 
    if len(obj.body)==0: return
    draw_dic[obj.dtype](obj, dc, f, style.copy(), **key)

def draw_layer(pts, dc, f, style, **key):
    update_style(style, pts)
    for i in pts.body: draw(i, dc, f, style.copy(), **key)

draw_dic['layer'] = draw_layer

def draw_layers(pts, dc, f, style, **key):
    update_style(style, pts)
    if key['cur'] in pts.body:
        draw(pts.body[key['cur']], dc, f, style.copy(), **key)

draw_dic['layers'] = draw_layers
    
def drawmark(dc, f, body, **key):
    style = body.default.copy()
    style['color'] = "#%02x%02x%02x" % style['color']
    style['tcolor'] = "#%02x%02x%02x" % style['tcolor']
    style['fcolor'] = "#%02x%02x%02x" % style['fcolor']
    if style['fill'] is False: style['fcolor'] = ''
    draw(body, dc, f, style, **key)

if __name__ == '__main__':
    pass
    # print(make_ellipse(0,0,2,1,0))
