#!/usr/bin/env python

import sys
import os

from math import *
from random import *

from pyx import canvas, path, deco, trafo, style, text, color, unit, epsfile, deformer, bitmap


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



text.set(mode="latex")
text.set(docopt="10pt")
text.preamble(r'\usepackage{amsmath,amsfonts,amssymb}')
text.preamble(r'\usepackage{mathrsfs}')
#text.preamble(r"\def\I{\mathbb{I}}")
text.preamble(r"\def\ket #1{|#1\rangle}")
text.preamble(r"\def\H{\mathscr{H}}")
text.preamble(r"\def\A{\mathcal{A}}")


rgb = color.rgb
rgbfromhexstring = color.rgbfromhexstring

red, green, blue, yellow, orange = (
    rgbfromhexstring("#d00000"),
    rgbfromhexstring("#006000"),
    rgb.blue, 
    rgb(0.75, 0.75, 0),
    rgb(0.75, 0.55, 0),
    )

blue = rgb(0., 0., 0.8)
pale_blue = rgb(0.7, 0.7, 1.0)
pink = rgb(1., 0.4, 0.4)
white = rgb(1., 1., 1.)
grey = rgb(0.8, 0.8, 0.8)

brown = rgbfromhexstring("#AA6C39"),

light_shade = rgb(0.85, 0.65, 0.1)

#shade = brown
#shade = orange
shade = grey




st_tau = [style.linewidth.Thick, red, style.linecap.round]
#st_vac = [style.linewidth.thick, red]+st_dotted

st_arrow = [deco.earrow()]

st_curve = g_curve = [green, style.linewidth.THick]+st_arrow



N = 20

def dopath(ps, extra=[], fill=[], closepath=True, smooth=0.3):
    ps = [path.moveto(*ps[0])]+[path.lineto(*p) for p in ps[1:]]
    if closepath:
        ps.append(path.closepath())
    p = path.path(*ps)
    if fill:
        c.fill(p, [deformer.smoothed(smooth)]+extra+fill)
    c.stroke(p, [deformer.smoothed(smooth)]+extra)


stack = []
def push():
    global c
    stack.append(c)
    c = canvas.canvas()

def pop(*args):
    global c
    c1 = stack.pop()
    c1.insert(c, *args)
    c = c1

SINGLE_COLUMN = False



#############################################################################
#
#

L = 4

dx, dy = 1.6, 1.6
m = 0.1
w, h = dx-m, dy-m


def anyon(x, y, extra=[], r=0.07):
    c.fill(path.circle(x, y, r), [white]+extra)
    c.stroke(path.circle(x, y, r), extra)


def pop(x, y, hflip=False, up=False, down=False):
    extra = []
    if hflip:
        extra.append(trafo.scale(x=x, y=y, sx=-1, sy=1.))
    elif up:
        extra.append(trafo.rotate(90, x=x, y=y))
    elif down:
        extra.append(trafo.rotate(-90, x=x, y=y))
    r = 0.4*w
    x0, x1 = x-1.0*r, x+1.0*r
    c.stroke(path.circle((x0+x1)/2, y, r),
        [trafo.scale(x=(x0+x1)/2, y=y, sy=0.4, sx=1.)]+extra)
    c.stroke(path.line(x0, y, x1, y), st_curve+extra)
    anyon(x-0.4*r, y, extra)
    anyon(x+0.4*r, y, extra)


#############################################################################
#
#

c = canvas.canvas()

c.fill(path.rect(-m, -m, L*dx+1*m, L*dy+1*m), [shade])

pop(1*dx-0.5*m, 1.3*dy-0.5*m, hflip=True)
pop(1*dx-0.5*m, 1.7*dy-0.5*m, hflip=False)

pop(3*dx-0.5*m, 0.5*dy, hflip=True)
pop(2*dx-0.5*m, 3.5*dy, hflip=True)

delta = 0.1
for (i, j) in [(2, 0), (1, 3), (2, 1), (3, 3)]:
    pop(j*dx+0.5*dx-delta, i*dy-0.5*m, up=True)
    delta = 0.

pop(0.3*dx, 3*dy-0.5*m, down=True)
pop(0.7*dx, 3*dy-0.5*m, down=True)

# Draw tiles
for i in range(L):
  for j in range(L):

    # bottom-left corner of tile
    x = j*dx
    y = i*dy
    c.stroke(path.rect(x, y, w, h))


c.writePDFfile("pic-pair-create.pdf")


#############################################################################
#
#

class Turtle(object):
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
        self.ps = [(x, y)]
        self.holes = []

    def fwd(self, d):
        self.x += d*sin(self.theta)
        self.y += d*cos(self.theta)
        self.ps.append((self.x, self.y))
        return self

    def reverse(self, d):
        self.fwd(-d)
        return self

    def right(self, dtheta, r=0.):
        theta = self.theta
        self.theta += dtheta
        if r==0.:
            return
        N = 20
        x, y = self.x, self.y
        x0 = x - r*sin(theta-pi/2)
        y0 = y - r*cos(theta-pi/2)
        for i in range(N):
            theta += (1./(N))*dtheta
            x = x0 - r*sin(theta+pi/2)
            y = y0 - r*cos(theta+pi/2)
            self.ps.append((x, y))
        self.x = x
        self.y = y
        return self

    def left(self, dtheta, r=0.):
        self.right(-dtheta, -r)
        return self

    def pair(self, r0, include=None):
        self.fwd(0.2*r0)
        if include != 1:
            self.holes.append((self.x, self.y))
        self.fwd(0.6*r0)
        if include != 0:
            self.holes.append((self.x, self.y))
        self.fwd(0.2*r0)
        return self

    def stroke(self, extra=[], fill=[], closepath=False):
        dopath(self.ps, extra, fill, closepath, smooth=0.)
        for x, y in self.holes:
            anyon(x, y)
        return self



#############################################################################
#
#

c = canvas.canvas()

c.fill(path.rect(0, 0, L*dx, L*dy), [shade])
c.fill(path.rect(-m, -m, L*dx+1*m, L*dy+1*m), [shade])

r0 = 0.5*h # cross a tile
r1 = 0.1*w # tight cap radius
r2 = 2*r1  # big cap radius

t = Turtle(0.5*w, 3*dy+0.5*r0, pi)

t.fwd(0.1*r0).pair(r0).right(pi, r1).fwd(r0).right(pi, 2*r1).pair(r0)

a, b = 2*r2, h-r0
#theta = atan(a/b)
#print theta/pi
theta = 0.265*pi
t.right(theta, r2)
t.fwd(0.6*(a**2+b**2)**0.5)
t.left(theta, r2)
t.fwd(r0).left(pi, r1).pair(r0).right(pi, r1).fwd(r0).left(pi/2, r1)
t.pair(r0).right(pi, r1).pair(r0).left(pi, r1).fwd(r0)
t.left(pi/2, 0.3*w).fwd(0.2*w).pair(r0)
t.fwd(r2)

t.stroke(st_curve)

t = Turtle(3*dx+0.63*r0, 0.49*h-r2, 1.5*pi)
t.fwd(0.2*r0).pair(r0)
t.right(pi, r2).fwd(1.4*r0).left(pi/2, r1).pair(r0).fwd(r2)
t.stroke(st_curve)

t = Turtle(2*dx+0.5*r0+0.05, 3*dy+0.5*h, 1.5*pi).fwd(0.1).pair(r0).fwd(r2)
t.stroke(st_curve)

t = Turtle(3*dx+0.5*w, 3*dy-0.5*m-0.7*r0, 0).fwd(0.2*r0).pair(r0).fwd(r2)
t.stroke(st_curve)

# Draw tiles
for i in range(L):
  for j in range(L):

    # bottom-left corner of tile
    x = j*dx
    y = i*dy
    c.stroke(path.rect(x, y, w, h))


c.writePDFfile("pic-join-pairs.pdf")


#############################################################################
#
#


c = canvas.canvas()

c.fill(path.rect(0, 0, L*dx, L*dy), [shade])
c.fill(path.rect(-m, -m, L*dx+1*m, L*dy+1*m), [shade])

r0 = 0.5*h # cross a tile
r1 = 0.1*w # tight cap radius
r2 = 2*r1  # big cap radius

t = Turtle(0.5*w, 3*dy+0.5*r0, pi)

t.fwd(0.1*r0).pair(r0).right(pi, r1).fwd(r0).right(pi, 2*r1).fwd(r0)

a, b = 2*r2, h-r0
#theta = atan(a/b)
#print theta/pi
theta = 0.265*pi
t.right(theta, r2)
t.fwd(0.6*(a**2+b**2)**0.5)
t.left(theta, r2)
t.fwd(r0).left(pi, r1).pair(r0, 0).right(pi, r1).fwd(r0).left(pi/2, r1)
t.fwd(r0).right(pi, r1).fwd(r0).left(pi, r1).fwd(r0)
t.left(pi/2, 0.3*w).fwd(0.2*w).pair(r0)
t.fwd(r2)

t.stroke(st_curve)

t = Turtle(3*dx+0.63*r0, 0.49*h-r2, 1.5*pi)
t.fwd(0.2*r0).pair(r0)
t.right(pi, r2).fwd(1.4*r0).left(pi/2, r1).pair(r0, 1).fwd(r2)
t.stroke(st_curve)

t = Turtle(2*dx+0.5*r0+0.05, 3*dy+0.5*h, 1.5*pi).fwd(0.1).pair(r0).fwd(r2)
t.stroke(st_curve)

t = Turtle(3*dx+0.5*w, 3*dy-0.5*m-0.7*r0, 0).fwd(0.2*r0).pair(r0).fwd(r2)
t.stroke(st_curve)

# Draw tiles
for i in range(L):
  for j in range(L):

    # bottom-left corner of tile
    x = j*dx
    y = i*dy
    c.stroke(path.rect(x, y, w, h))



c.writePDFfile("pic-curve-uniq.pdf")




