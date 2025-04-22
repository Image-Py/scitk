import sys; sys.path.append('../')

from sciapp.action import Filter

class Gaussian(Filter):
    title = 'Gaussian'
    note = ['auto_snap', 'preview']
    para = {'sigma':2}
    view = [(float, 'sigma', (0, 30), 1, '标准差', '像素')]

    def run(self, ips, img, snap, para):
        gaussian_filter(snap, para['sigma'], output=img)
