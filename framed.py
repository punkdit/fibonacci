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

st_Thick = [style.linewidth.Thick]


text.set(mode="latex")
text.set(docopt="10pt")
text.preamble(r'\usepackage{amsmath,amsfonts,amssymb}')
#text.preamble(r"\def\I{\mathbb{I}}")
text.preamble(r"\def\ket #1{|#1\rangle}")


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
black = rgb(0., 0., 0.)
grey = rgb(0.8, 0.8, 0.8)

brown = rgbfromhexstring("#AA6C39"),

light_shade = rgb(0.85, 0.65, 0.1)

#shade = brown
#shade = orange
shade = rgb(0.8, 0.8, 0.8)


g_curve = [green, style.linewidth.THick]

st_tau = [style.linewidth.Thick, red, style.linecap.round]
#st_vac = [style.linewidth.thick, red]+st_dotted


def anyon(x, y, r=0.07):
    c.fill(path.circle(x, y, r), [white])
    c.stroke(path.circle(x, y, r), [style.linewidth.thick])


N = 20

def dopath(ps, extra=[], fill=[], closepath=False, smooth=0.0, stroke=True):
    if not ps:
        print "dopath: empty"
        return
    ps = [path.moveto(*ps[0])]+[path.lineto(*p) for p in ps[1:]]
    if closepath:
        ps.append(path.closepath())
    p = path.path(*ps)
    extra = list(extra)
    if smooth:
        extra.append(deformer.smoothed(smooth))
    if fill:
        c.fill(p, extra+fill)
    if stroke:
        c.stroke(p, extra)


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



class Turtle(object):
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
        self.ps = [(x, y)]
        self.pen = True

    def penup(self):
        self.pen = False
        self.ps = []
        return self

    def pendown(self):
        self.pen = True
        self.ps = [(self.x, self.y)]
        return self

    def fwd(self, d):
        self.x += d*sin(self.theta)
        self.y += d*cos(self.theta)
        if self.pen:
            self.ps.append((self.x, self.y))
        return self

    def reverse(self, d):
        self.fwd(-d)
        return self

    def right(self, dtheta, r=0.):
        theta = self.theta
        self.theta += dtheta
        if r==0.:
            return self
        N = 20
        x, y = self.x, self.y
        x0 = x - r*sin(theta-pi/2)
        y0 = y - r*cos(theta-pi/2)
        for i in range(N):
            theta += (1./(N))*dtheta
            x = x0 - r*sin(theta+pi/2)
            y = y0 - r*cos(theta+pi/2)
            if self.pen:
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



def occluded(ps0, pss, radius=0.2):

    ps = []

    flag = True
    for i, p in enumerate(ps0):

        flag1 = True
        x, y = p
        for ps1 in pss:
            x1, y1 = ps1[i]
            if abs(x1-x)<radius:
                flag1 = False
        #print int(flag1),

        if flag1 == flag:
            ps.append(p)
        elif ps:
            yield flag, ps
            ps = [p]
        flag = flag1

    if ps:
        yield flag, ps


def draw(ps0, pss, descs, radius=0.25):

    descs = list(descs)
    desc = descs.pop(0) if descs else True
    _ps = []
    for flag, ps in occluded(ps0, pss, radius):
        #print '/',
        if flag or desc:
            _ps += ps
        else:
            yield _ps
            _ps = []
        if not flag:
            desc = descs.pop(0) if descs else True
    if _ps:
        yield _ps


def bump(x0, alpha=0.4):
    x1 = 0.5 - 0.5*cos(pi*x0)
    x = alpha*x0 + (1-alpha)*x1
    return x


def timeslice(x, y, transparency=0., label="", W=3.5, H=1.):
    y0 = -0.5*H
    y1 = +0.5*H
    x0 = -0.5*W
    x1 = +0.5*W
    slope = 0.3
    dopath([(x0-slope, y0), (x0+slope, y1), (x1+slope, y1), (x1-slope, y0)],
        fill=[shade, color.transparency(transparency)],
        extra=[trafo.translate(x, y)], closepath=True)
    if label:
        c.text(W+0.2, 0., label, west+[trafo.translate(x, y)])



###############################################################################
#


W = 5.
H = 4.

r = 0.4 # radius of ribbon

def tr(px, py, pz):
#    return px+0.2*pz, py+0.8*pz
    return px, 0.8*py+1.0*pz

c = canvas.canvas()


x = 0.
y = 0. # ---------------



timeslice(x, y)

c.stroke(path.line(x, y, x, y+H), st_Thick)
c.fill(path.circle(x, y, 0.04))

N = 15
THETA = 2*pi
dtheta = THETA / N
for i in range(N+1):

    x0 = x - r*cos(i*dtheta)
    x1 = x + r*cos(i*dtheta)
    y0 = y - r*sin(i*dtheta)
    y1 = y + r*sin(i*dtheta)
    z0 = z1 = 1.*i*H/N

    X0, Y0 = tr(x0, y0, z0)
    X1, Y1 = tr(x1, y1, z1)
    c.stroke(
        path.line(X0, Y0, X1, Y1), 
        [deco.earrow(size=0.1)])
    

timeslice(x, y+H, 0.5)

c.fill(path.circle(x, y+H, 0.04))
c.stroke(
    path.line(X0, Y0, X1, Y1), 
    [deco.earrow(size=0.1)])

x += W # ---------------

timeslice(x, y)

N = 60
THETA = 2*pi
dtheta = THETA / N

ps0 = []
ps1 = []
for i in range(N+1):
    x0 = x + r*cos(i*dtheta)
    x1 = x - r*cos(i*dtheta)
    y0 = y + r*sin(i*dtheta)
    y1 = y - r*sin(i*dtheta)
    z0 = z1 = 1.*i*H/N
    ps0.append((x0, y0, z0))
    ps1.append((x1, y1, z1))


d = 0.01
for i in range(N):
    x00, y00 = tr(*ps0[i])
    x01, y01 = tr(*ps0[i+1])
    x10, y10 = tr(*ps1[i])
    x11, y11 = tr(*ps1[i+1])

    rr = 0.2 + 0.6*cos(i*dtheta+0.8)**2
    cl = rgb(rr, rr, rr)
    w = x1-x0
    h = 1.*H/N
    p = path.path(
        path.moveto(x00, y00-d), 
        path.lineto(x01, y01+d),
        path.lineto(x11, y11+d),
        path.lineto(x10, y10-d),
        path.closepath())
    c.fill(p, [cl])

    #c.fill(path.circle(x00, y00, 0.02))
    c.stroke(path.line(x00, y00, x01, y01+d), [style.linewidth.Thick])
    c.stroke(path.line(x10, y10, x11, y11+d), [style.linewidth.Thick])



timeslice(x, y+H, 0.5)

x += W # ---------------

timeslice(x, y)

sy = 0.4
t = trafo.scale(1., sy, x, y)
c.stroke(path.circle(x, y, r), [t])
c.fill(path.circle(x, y-sy*r, 0.05))

c.fill(path.path(
    path.moveto(x-r, y),
    path.lineto(x+r, y),
    path.lineto(x+r, y+H),
    path.lineto(x-r, y+H),
    path.closepath()), [shade])

#c.stroke(path.circle(x, y, r), [t, rgb(0.5,0.5,0.5)])
c.stroke(path.path(path.arc(x, y, r, 0, 180)), [t, rgb(0.5,0.5,0.5)])

N = 40
THETA = 2*pi
dtheta = THETA / N

def tr(px, py, pz):
#    return px+0.2*pz, py+0.8*pz
    return px, sy*py+1.0*pz

ps0 = []
for i in range(N+1):
    x0 = x + 1.08*r*cos(i*dtheta-0.5*pi)
    y0 = y + 1.08*r*sin(i*dtheta-0.5*pi)
    z0 = z1 = 1.*i*H/N
    ps0.append((x0, y0, z0))


d = 0.01
for i in range(N):
    x00, y00 = tr(*ps0[i])
    x01, y01 = tr(*ps0[i+1])

    if i>N/4 and i<3*N/4:
        st = [rgb(0.5, 0.5, 0.5)]
    else:
        st = [style.linewidth.Thick, style.linecap.round]
    
    c.stroke(path.line(x00, y00, x01, y01+d), st)
            
        #c.fill(path.circle(x00, y00, 0.02))


timeslice(x, y+H, 0.5)

t = trafo.scale(1., sy, x, y+H)
p = path.circle(x, y+H, r)
c.fill(p, [t, white])
c.stroke(p, [t])
c.fill(path.circle(x, y-sy*r+H, 0.05))


c.writePDFfile("pic-framed.pdf")




