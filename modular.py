#!/usr/bin/env python

import sys
import os

from math import *
from random import *

from pyx import canvas, path, deco, trafo, style, text, color, unit, epsfile, deformer, bitmap

from PIL import Image

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
text.set(docopt="12pt")
text.preamble(r'\usepackage{amsmath,amsfonts,amssymb}')
text.preamble(r'\usepackage{mathrsfs}')
#text.preamble(r"\def\I{\mathbb{I}}")
text.preamble(r"\def\ket #1{|#1\rangle}")
text.preamble(r"\def\H{\mathscr{H}}")


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



g_curve = [green, style.linewidth.THick]

st_tau = [style.linewidth.Thick, red, style.linecap.round]
#st_vac = [style.linewidth.thick, red]+st_dotted



def anyon(x, y, r=0.07):
    c.fill(path.circle(x, y, r), [white])
    c.stroke(path.circle(x, y, r), [red, style.linewidth.thick])


N = 20

def dopath(ps, extra=[], fill=[], closepath=True, smooth=0.3):
    ps = [path.moveto(*ps[0])]+[path.lineto(*p) for p in ps[1:]]
    if closepath:
        ps.append(path.closepath())
    p = path.path(*ps)
    if fill:
        c.fill(p, [deformer.smoothed(smooth)]+extra+fill)
    c.stroke(p, [deformer.smoothed(smooth)]+extra)

def ellipse(x0, y0, rx, ry, extra=[], fill=[]):
    ps = []
    for i in range(N):
        theta = 2*pi*i / (N-1)
        ps.append((x0+rx*sin(theta), y0+ry*cos(theta)))
    dopath(ps, extra, fill)



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



#############################################################################
#
#

w = 1.5
h = 1.5

x = 0
y = 0

c = canvas.canvas()

#c.text(x+0.5*h, y, r"\bigoplus_a \H\bigl(", text.mathmode) #east)
c.text(x, y+0.5*h, r"$\bigoplus_a \H\Bigl($", east)
# XXX fix display math XXX

r = 1.0
x += 0.0*w

p = path.circle(x+r, y+0.5*h, r)
c.fill(p, [shade])
c.stroke(p)
c.fill(path.circle(x+2*r, y+0.5*h, 0.06))

x += 0.3*w
p = path.circle(x+0.1*w, y+0.5*h, 0.4*r)
c.fill(p, [white])
c.stroke(p)
p = path.circle(x+0.1*w+0.4*r, y+0.5*h, 0.06)
c.fill(p)

c.text(x+0.6*w, y+0.5*h, "...")

#c.text(x+0.1*w, y+0.0*h, "$M_a$", west)
c.text(x+0.2*w, y+0.0*h, "$M$", west)

c.text(x+0.3*w, y+0.7*h, "$a$", southwest)

x += 1.8*r

r = 0.7
p = path.circle(x+r, y+0.5*h, r)
c.fill(p, [shade])
c.stroke(p)
p = path.circle(x+2*r, y+0.5*h, 0.06)
c.fill(p)

x += 0.3*w

c.text(x+0.0*w, y+0.5*h, "...")

#c.text(x+0.0*w, y+0.2*h, "$N_{\hat{a}}$", west)
c.text(x+0.0*w, y+0.2*h, "$N$", west)

c.text(x+0.5*w, y+0.9*h, "$\widehat{a}$", southwest)

x += 1.8*r
c.text(x, y+0.5*h, r"$\Bigr)$", east)

x -= 0*r
y -= 3*r

#c.text(x, y+0.5*h, r"$\to\H\Bigl($", east)
#c.text(x, y+0.5*h, r"$\xrightarrow{\cong}\H\Bigl($", east)
c.text(x-0.8, y+0.5*h, r"$\H\Bigl($", west)
c.stroke(path.line(x-2.0, y+0.5*h, x-0.9, y+0.5*h), [deco.arrow()])
c.text(x-1.5, y+0.6*h, r"$\cong$", south)

print dir(deco)

r = 1.0
#x += 0.5*w

p = path.circle(x+r, y+0.5*h, r)
c.fill(p, [shade])
c.stroke(p)
c.stroke(p)
c.fill(path.circle(x+2*r, y+0.5*h, 0.06))

x += 0.3*w
p = path.circle(x+0.1*w, y+0.5*h, 0.4*r)
c.stroke(p, st_dashed)
p = path.circle(x+0.1*w+0.4*r, y+0.5*h, 0.06)
c.stroke(p, st_dashed)

c.text(x+0.1*w, y+0.5*h, r"$N$", center)
#c.text(x+0.2*w, y+0.5*h, r"$...$", center)

c.text(x+0.6*w, y+0.5*h, "...")

c.text(x+0.2*w, y+0.0*h, "$M$", west)

x += 1.8*r
c.text(x, y+0.5*h, r"$\Bigr)$", east)


c.writePDFfile("pic-glue.pdf")


#############################################################################
#
#

w = 1.5
h = 1.5

x = 0
y = 0

c = canvas.canvas()


def surface(x, y, r, fill=shade, mark=False):
    p = path.circle(x, y, r)
    if fill is not None:
        c.fill(p, [fill])
    c.stroke(p)
    if mark:
        p = path.circle(x+r, y, 0.06)
        c.fill(p)

r = 1.0

surface(x+0, y, r)
surface(x-0.6*r, y, 0.1*r, fill=white)
surface(x+0.0*r, y, 0.1*r, fill=white)
surface(x+0.6*r, y, 0.1*r, fill=white)

c.text(x-0.6*r, y+0.2, "$a$", south)
c.text(x,       y+0.2, "$b$", south)
c.text(x+0.6*r, y+0.2, "$c$", south)

c.stroke(path.circle(x-0.3*r, y, 0.6*r), st_dashed+[trafo.scale(1., 1.1, x, y)])
c.stroke(path.circle(x+0.3*r, y, 0.6*r), st_dashed+[trafo.scale(1., 1.1, x, y)])

c.text(x-1.5*r, y, r"$\H\Bigl($", center)
c.text(x+1.3*r, y, r"$\Bigr)$", center)

x -= 3.0*r
y -= 3.0*r

surface(x-0.7*r, y, 0.6*r)
surface(x+0.7*r, y, 0.6*r)
labels = "adbc"
for i, x0 in enumerate([x-0.9*r, x-0.5*r, x+0.5*r, x+0.9*r]):
    surface(x0, y, 0.1*r, fill=white)
    c.text(x0, y+0.2, "$%s$"%labels[i], south)
c.text(x+1.1*r, y+0.7, "$\widehat{d}$", west)

c.text(x-1.5*r, y, r"$\bigoplus_d\H\Bigl($", east)
c.text(x+1.7*r, y, r"$\Bigr)$", center)


c.text(0, y+0.1, r"$F$", south)
c.stroke(path.line(-1.0*r, y, +0.8*r, y), [deco.earrow()])

x += 7*r

surface(x-0.7*r, y, 0.6*r)
surface(x+0.7*r, y, 0.6*r)
labels = "abec"
for i, x0 in enumerate([x-0.9*r, x-0.5*r, x+0.5*r, x+0.9*r]):
    surface(x0, y, 0.1*r, fill=white)
    c.text(x0, y+0.2, "$%s$"%labels[i], south)
c.text(x-1.1*r, y+0.7, "$\widehat{e}$", east)

c.text(x-1.5*r, y, r"$\bigoplus_e\H\Bigl($", east)
c.text(x+1.7*r, y, r"$\Bigl)$", center)

c.stroke(path.line(-3.0*r, -2.0*r, -1.5*r, -0.8*r), [deco.earrow()])
c.text(-2.6*r, -1.4*r, "$\cong$", center)

c.stroke(path.line(+3.4*r, -2.0*r, +1.9*r, -0.8*r), [deco.earrow()])
c.text(+3.0*r, -1.4*r, "$\cong$", center)

c.writePDFfile("pic-glue-fmove.pdf")


#############################################################################
#
#



class Turtle(object):
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
        self.ps = [(x, y)]

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

    def stroke(self, extra=[], fill=[], closepath=False):
        dopath(self.ps, extra, fill, closepath, smooth=0.)
        return self



w = 1.5
h = 1.5

x = 0
y = 0

c = canvas.canvas()


r0 = 1.3
#surface(x, y, r0)
#c.fill(path.circle(x, y+r0, 0.04))
c.fill(path.circle(x, y, r0), [shade])


r = 0.15
dx = 4*r
x1 = x-1.5*dx

t = Turtle(x1, y, 0.*pi)
t.right(pi, 1.5*dx)
t.stroke(g_curve+[style.linecap.round])

t = Turtle(x1-0.4*dx, y, 0.*pi)
t.right(pi, 1.9*dx)
t.right(pi, 0.4*dx)
t.left(pi, 1.1*dx)
t.right(pi, 0.4*dx)
t.stroke(st_dashed)

c.stroke(path.circle(x, y, dx), st_dashed+[trafo.scale(0.9, 0.7)])

r = 0.14

t = Turtle(x1+1*dx, y+r, pi/2)
t.fwd(dx)
t.stroke(g_curve+[style.linecap.round])

for i in range(4):
    surface(x1, y, r, white)
    c.fill(path.circle(x1, y+r, 0.04))
    x1 += dx


c.writePDFfile("pic-2-curve.pdf")


#############################################################################
#
#

c = canvas.canvas()


r0 = 1.3


r = 0.2
dx = 4*r
x1 = x-1.5*dx

c.fill(path.circle(x+0.3*dx, y, r0), [shade, trafo.scale(1.6, 0.7)])


r = 0.20

t = Turtle(x1-0.0*dx, y+r, pi/2)
t.fwd(4*dx)
#t.stroke(g_curve+st_dotted)
t.stroke(g_curve)

for i in range(3):
    t = Turtle(x1, y+r, pi/2)
    t.fwd(dx)
    t.stroke(g_curve+[style.linecap.round])

    surface(x1, y, r, white)
    c.fill(path.circle(x1, y+r, 0.04))

    c.stroke(path.circle(x1+0.5*dx, y, dx), st_dashed+[trafo.scale(0.9, 0.6, x=x1+0.5*dx, y=0)])
    x1 += dx

surface(x1, y, r, white)
c.fill(path.circle(x1, y+r, 0.04))


#c.text(x-2.2*dx, y-r, "...", north)
c.text(x+2.4*dx, y-2*r, "...", north)

c.writePDFfile("pic-chain.pdf")


#############################################################################
#
#



