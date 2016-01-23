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

shade = rgb(0.75, 0.55, 0)
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
    r = (x**2+y**2)**0.5
    return x/r, y/r

def rotate(dv):
    x, y = dv
    x, y = -y, x
    return x, y

def getlevel(x, y):
    dv = getgrad(x, y)
    dv = rotate(dv)
    return dv


#print getv(5.5, 5.5), getv(5.6, 5.5)
#print getv(5.5, 5.6), getv(5.6, 5.6)
#print getgrad(5.5, 5.5)

c = canvas.canvas()
dx = 0.1
dy = 0.1

for i in range(H):
  for j in range(W):
    r = v[i, j]
    cl = rgb(r, r, r)
    #cl = color.gradient.RedBlue
    c.fill(path.rect(j*dx, i*dy, 1.2*dx, 1.2*dy), [cl])

def plotlevelset(x, y, length=100):
    ps = [path.moveto(x*dx, y*dy)]
    #while 1:
    z0 = getv(x, y)
    for i in range(length):

        dv = getgrad(x, y)
        #print x, y, dv
        if abs(dv[0])+abs(dv[1])<1e-4:
            break

        dv = rotate(dv)

        dv = normalize(dv)
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

        ps.append(path.lineto(x*dx, y*dy))
    c.stroke(path.path(*ps), [white])


rnd = lambda : 0.9*random() + 0.05
for count in range(5):
    #x, y = 0.2*W, 5.
    x, y = rnd()*W, rnd()*H
    #plotlevelset(x, y)

plotlevelset(0.05*W, H/2., 200)
plotlevelset(0.10*W, H/2., 150)
plotlevelset(0.15*W, H/2., 50)
plotlevelset(0.32*W, H/2., 50)
plotlevelset(0.70*W, H/2., 50)

c.writePDFfile("pic-pants.pdf")





