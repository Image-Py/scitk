from scipy.cluster.vq import kmeans
from shapely.ops import voronoi_diagram
from shapely.geometry import MultiPoint, MultiPolygon
import matplotlib.pyplot as plt
from time import time
import numpy as np

# 空间采样，边界，点数，过采样倍数（越高越均质）
def sample(box, n, k=1):
    x1, y1, x2, y2 = box
    xs = np.random.uniform(x1, x2, int(n*k))
    ys = np.random.uniform(y1, y2, int(n*k))
    return kmeans(np.array([xs, ys]).T, n)[0]

# voronoi剖分，传入边界多边形，采样点
def voronoi(polygon, pts):
    mpoly = voronoi_diagram(MultiPoint(pts))
    mpoly = [i.intersection(polygon) for i in mpoly.geoms]
    return MultiPolygon(mpoly)

# 生成随机内接多边形，点数越大越丰满
def random_polygon(polygon, n=15):
    x1,y1,x2,y2 = polygon.bounds
    xs = np.random.uniform(x1, x2, n)
    ys = np.random.uniform(y1, y2, n)
    xys = MultiPoint(np.array([xs, ys]).T)
    mps = xys.intersection(polygon)
    return mps.convex_hull

# 生成muliolygon的内接多边形集合
def random_inner(mpoly, n=15):
    mpoly = [random_polygon(i, n) for i in mpoly.geoms]
    return MultiPolygon(mpoly)

# 小球填充，传入多边形，半径
def fill_ball(polygon, r):
    x1,y1,x2,y2 = polygon.bounds
    x = np.mgrid[x1:x2:2*r, y1:y2:2*3**0.5*r]
    x = x.reshape(2, -1).T
    x = np.concatenate((x, x+(r,r*3**0.5)))
    p = MultiPoint(x).intersection(polygon)
    # ps = [i.buffer(r, 4) for i in p.geoms]
    return p.buffer(r, 4)

# 绘制多边形
def plot(ax, mpoly, color):
    ax.set_aspect('equal')
    for poly in mpoly.geoms:
        ax.plot(*poly.exterior.xy, color)

if __name__ == '__main__':
    box = MultiPoint([(0,0), (20,10)]).envelope
    spts = sample(box.bounds, 200, 2)
    frags = voronoi(box, spts)
    random_frags = random_inner(frags, 55)
    balls = fill_ball(random_frags, 0.1)

    plot(plt.gca(), frags, 'green')
    plot(plt.gca(), random_frags, 'black')
    plot(plt.gca(), balls, 'red')
    
    plt.show()
