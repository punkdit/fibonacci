#!/usr/bin/env python

import sys
from math import *
from random import *
import numpy
import scipy

from pyx import canvas, path, deco, trafo, style, text, color, deformer

text.set(mode="latex") 
text.set(docopt="12pt")
text.preamble(r"\usepackage{amsmath,amsfonts,amssymb}")

rgb = color.rgb
rgbfromhexstring = color.rgbfromhexstring

red, green, blue, yellow = (
    rgbfromhexstring("#d00000"),
    rgbfromhexstring("#006000"),
    rgb.blue, rgb(0.75, 0.75, 0)) 

black = rgb(0., 0., 0.) 
blue = rgb(0., 0., 0.8)
lred = rgb(1., 0.4, 0.4)
white = rgb(1., 1., 1.) 

shade0 = rgb(0.75, 0.55, 0)
shade1 = rgb(0.70, 0.55, 0)
shade2 = rgb(0.65, 0.50, 0)
grey = rgb(0.75, 0.75, 0.75)

light_shade = rgb(0.85, 0.65, 0.1)
light_shade = rgb(0.9, 0.75, 0.4)


north = [text.halign.boxcenter, text.valign.top]
northeast = [text.halign.boxright, text.valign.top]
northwest = [text.halign.boxleft, text.valign.top]
south = [text.halign.boxcenter, text.valign.bottom]
southeast = [text.halign.boxright, text.valign.bottom]
southwest = [text.halign.boxleft, text.valign.bottom]
east = [text.halign.boxright, text.valign.middle]
west = [text.halign.boxleft, text.valign.middle]
center = [text.halign.boxcenter, text.valign.middle]


st_dashed = [style.linestyle.dashed]
st_dotted = [style.linestyle.dotted]

st_thick = [style.linewidth.thick]
st_Thick = [style.linewidth.Thick]

st_tau = [style.linewidth.Thick, red, style.linecap.round]
st_vac = [style.linewidth.thick, red]+st_dotted



###############################################################################
#
#

from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from numpy.linalg import solve, norm
from numpy.random import rand

H, W = 32, 96
#H, W = 8, 8
#H, W = 32, 32
HW = H*W

bdy = numpy.zeros((H, W), dtype=numpy.float64)
mask = numpy.zeros((H, W), dtype=numpy.int32)

if 0:
    for i in range(H):
        bdy[i, 0] = 1
        bdy[i, W-1] = 1
    for j in range(W):
        bdy[0, j] = -1
        bdy[H-1, j] = -1

else:
    for i in range(H):
        bdy[i, 0] = -1.
        bdy[i, W-1] = -1.
    for j in range(W):
        bdy[0, j] = -1.
        bdy[H-1, j] = -1.


#def drawcirc(x, y, r, val=1.):


bdy[H//2, 1*W//5] = 1.5
bdy[H//2, 2*W//5] = 1.
bdy[H//2, 4*W//5] = 1.

#print bdy
mask[numpy.where(bdy!=0.)] = 1

bdy.shape = HW
mask.shape = HW

v = numpy.zeros((HW,), dtype=numpy.float64)
A = lil_matrix((HW, HW))

for i in range(1, H-1):
  for j in range(1, W-1):
    assert A[i*W+j, i*W+j] == 0.
    A[i*W+j, (i-1)*W+j] = 0.25
    A[i*W+j, (i+1)*W+j] = 0.25
    A[i*W+j, i*W+(j-1)] = 0.25
    A[i*W+j, i*W+(j+1)] = 0.25


for i in range(H):
  for j in range(W):
    idx = i*W+j
    if mask[idx]:
        A[idx, :] = 0.
        A[idx, idx] = 1.0
        v[idx] = bdy[idx]

#numpy.set_printoptions(threshold='nan')

#print A

A = A.tocsr()
#b = rand(1000)
#x = spsolve(A, b)

#print A.todense()


#v[mask] = bdy[mask]
#v[:] = bdy
#v[:] = 1.
#print list(x)

#N = int(sys.argv[1])
N = 10000
for count in range(N):
    #print ".",;sys.stdout.flush()
    v = A.dot(v)
    #print list(v)
#print

v -= v.min()
v *= 1./v.max()
v.shape = (H, W)
#print v


def getv(x, y):
    # some kind of linear interpolation hack...
    x0 = int(x)
    rx = x-x0
    y0 = int(y)
    ry = y-y0

    z0 = v[y0, x0]
    z1 = v[y0, x0+1]
    z00 = rx*z1 + (1.-rx)*z0

    z0 = v[y0+1, x0]
    z1 = v[y0+1, x0+1]
    z11 = rx*z1 + (1.-rx)*z0

    z = ry*z11 + (1.-ry)*z00

    return z


def getgrad(x, y):
    # get the gradient
    x0 = int(x)
    rx = x-x0
    y0 = int(y)
    ry = y-y0

    if rx+ry <= 1.:
        dv = v[y0, x0+1] - v[y0, x0], v[y0+1, x0] - v[y0, x0]
    else:
        dv = v[y0+1, x0+1] - v[y0+1, x0], v[y0+1, x0+1] - v[y0, x0+1]

    return dv

def normalize(dv):
    x, y = dv
    r = (x**2.0+y**2.0)**0.5
    return x/r, y/r

def rotate(dv):
    x, y = dv
    x, y = -y, x
    return x, y

def getlevel(x, y):
    dv = getgrad(x, y)
    dv = rotate(dv)
    return dv

def dot(d0, d1):
    return d0[0]*d1[0] + d0[1]*d1[1]


#def getline(x0, y0, x1, y1):
def getline(*args):

    args1 = []
    for arg in args:
        if isinstance(arg, (list, tuple)):
            args1 += list(arg)
        else:
            args1.append(arg)
    assert len(args1)==4, repr( args1)
    x0, y0, x1, y1 = args1

    dv = x1-x0, y1-y0
    #r = (dv[0]**2 + dv[1]**2)**0.5
    #n = int(round(r))
    n = 100
    r = 1.*n
    dv = dv[0]/r, dv[1]/r    

    x, y = x0, y0
    z = getv(x, y)
    pts = [(x, y, z)]
    for i in range(n):
        x += dv[0]
        y += dv[1]
        pts.append((x, y, getv(x, y)))
    return pts


def getlevelset(x, y, length=None):
    z0 = getv(x, y)
    pts = [(x, y, z0)]
    dv0 = None

    state = True

    i = 0
    while 1:
        i += 1

        dv = getgrad(x, y)
        #print x, y, dv
        if abs(dv[0])+abs(dv[1])<1e-4:
            break

        dv = rotate(dv)
        dv = normalize(dv)

        if dv0 is None:
            dv0 = dv
        r = dot(dv, dv0)
        if state and r<-0.9:
            yield pts
            pts = [pts[-1]]
            state = 0
        elif not state and r>0.95:
            yield pts
            break

        x += dv[0]
        y += dv[1]
    
        z = getv(x, y)
        dz = z0-z
        #print "%.4f"%dz,
        dv = getgrad(x, y)
        r = (dv[0]**2+dv[1]**2)
        dv = dv[0]*dz/r, dv[1]*dz/r
        x += dv[0]
        y += dv[1]

        pts.append((x, y, z0))

        if length and i>length:
            break

    #return pts


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   pick a coordinate system:
#

c = canvas.canvas()
dx = 0.1
dy = 0.1

def transform(x, y, z):
    x1 = x + 0.3*y
    y1 = 0.5*y + 4*H*z

    return x1*dx, y1*dy

#def transform(x, y, z):
#    return x*dx, y*dy


for y in range(H-2,0,-1):
  for x in range(W-1):
    z00 = v[y, x]
    z01 = v[y+1, x]
    z10 = v[y, x+1]
    z11 = v[y+1, x+1]
    if max(z00,z01,z10,z11)>0.5:
        continue
    r = 2*z00
    cl = rgb(r,r,r)
    #c.fill(path.rect(x*dx, y*dy, 1.2*dx, 1.2*dy), [cl])

    ps = [
        path.moveto(*transform(x, y, z00)),
        path.lineto(*transform(x+1.2, y, z10)),
        path.lineto(*transform(x+1.2, y+1.2, z11)),
        path.lineto(*transform(x, y+1.2, z01)),
        path.closepath()]

    #c.fill(path.path(*ps), [cl])


def plotpts(pts, deco, closed=False, fill=False):
    x, y, z = pts[0]
    ps = [path.moveto(*transform(x, y, z))]
    for x, y, z in pts[1:]:
        ps.append(path.lineto(*transform(x, y, z)))
    if closed:
        ps.append(path.closepath())
    if fill:
        c.fill(path.path(*ps), deco)
    else:
        c.stroke(path.path(*ps), deco)


back, front = 0, 1

coords = [0.05*W, 0.10*W, 0.15*W, 0.32*W, 0.70*W]
levelsets = [list(getlevelset(coord, H/2.)) for coord in coords]

rev = lambda items : list(reversed(items))

edge = (
    getline(coords[0], H/2., coords[1], H/2.) +\
    rev(levelsets[1][front]) +\
    getline(levelsets[1][front][0][:2], coords[4], H/2.) +\
    rev(levelsets[4][front]) +\
    getline(levelsets[4][front][0][:2], 
        levelsets[0][front][0][:2]) +\
    levelsets[0][front])

plotpts(edge, [shade0]+st_Thick, closed=True, fill=True)

edge = (
    getline(coords[1], H/2., coords[2], H/2.) +\
    rev(levelsets[2][front]) +\
    getline(levelsets[2][front][0][:2], coords[3], H/2.) +\
    rev(levelsets[3][front]) +\
    getline(levelsets[3][front][0][:2], 
        levelsets[1][front][0][:2]) +\
    levelsets[1][front])

plotpts(edge, [shade0]+st_Thick, closed=True, fill=True)

back, front = getlevelset(coords[0], H/2.)
plotpts(back, [black]+st_dashed)
plotpts(front, [black]+st_thick)

#pts = getline(coords[0], H/2., coords[1], H/2.)
#plotpts(pts, [black]+st_thick)

back, front = getlevelset(coords[1], H/2.)
plotpts(back, [black]+st_dashed)
plotpts(front, [black]+st_thick)

back, front = getlevelset(coords[2], H/2.)
plotpts(back+front, [shade2]+st_thick, closed=True, fill=True)
plotpts(back+front, [black]+st_thick, closed=True)

back, front = getlevelset(coords[3], H/2.)
plotpts(back+front, [shade2]+st_thick, closed=True, fill=True)
plotpts(back+front, [black]+st_thick, closed=True)

back, front = getlevelset(coords[4], H/2.)
plotpts(back+front, [shade2]+st_thick, closed=True, fill=True)
plotpts(back+front, [black]+st_thick, closed=True)



c.writePDFfile("pic-pants.pdf")





