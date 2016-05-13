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
    c.stroke(path.circle(x, y, r), [style.linewidth.thick])


N = 20

def dopath(ps, extra=[], fill=[], closepath=False, smooth=0.0):
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

def timeslice(x, y, transparency=0., label="", W=3):
    dopath([(-1.1, y0), (-0.1, y1), (W + .2, y1), (W -0.8, y0)],
        fill=[shade, color.transparency(0.3)],
        extra=[trafo.translate(x, y)], closepath=True)
    if label:
        c.text(W+0.2, 0., label, west+[trafo.translate(x, y)])



#############################################################################
#
#


c = canvas.canvas()


# hole spacing
w = 1.0
W = 3*w

# total hight
H = 3.0

N = 100

ps0 = []
ps1 = []
ps2 = []
for i in range(N+1):
    r = 1.*i/N
    y = r*H
    r = bump(r)

    x = w - w*cos(2*pi*r)
    ps0.append((x, y))

    x = w + w*sin(2*pi*r)
    ps1.append((x, y))

    x = 1*w + w*cos(2*pi*r)
    ps2.append((x, y))


y0, y1 = -0.3, 0.3

timeslice(0., 0., 0., "$t_0$")

for ps in draw(ps0, [ps1, ps2], [True, True, False, False]):
    dopath(ps, st_Thick)

for ps in draw(ps1, [ps0, ps2], [True, False, False, True]):
    dopath(ps, st_Thick)

for ps in draw(ps2, [ps0, ps1], [False, False, True, True]):
    dopath(ps, st_Thick)


timeslice(0., H, 0.3, "$t_1$")

for i in range(3):
    c.fill(path.circle(i*w, 0., 0.06))
    c.fill(path.circle(i*w, H, 0.06))


x = -1.5*w
c.stroke(path.line(x, -0.2, x, H+0.2), [deco.earrow()])
c.text(x, H+0.5, "time", south)


c.writePDFfile("pic-braid-worldlines.pdf")



#############################################################################
#
#

def braid_1(x0=0., y0=0., H=3.0, t0="", t1="", inverse=False):

    if inverse:
        rev = lambda x : list(reversed(x))
        rev1 = lambda ps : [(x, H-y) for (x, y) in reversed(ps)]
    else:
        rev = list
        rev1 = list

    tr = [trafo.translate(x0, y0)]

    ps0 = []
    ps1 = []
    ps2 = []
    for i in range(N+1):
        r = 1.*i/N
        y = r*H
        r1 = bump(r)
    
        x = 0.5*(w - w*cos(2*pi*r1))
        ps0.append((x, y))
    
        x = w + w*(sin(0.5*pi*r))
        ps1.append((x, y))
    
        x = 1*w + w*cos(1.5*pi*r1)
        ps2.append((x, y))
    ps0 = rev1(ps0)
    ps1 = rev1(ps1)
    ps2 = rev1(ps2)
    
    if not inverse: # HACK
        timeslice(x0, y0, 0., t0)
    
    for ps in draw(ps0, [ps1, ps2], rev([True, False])):
        dopath(ps, st_Thick+tr)
    
    for ps in draw(ps1, [ps0, ps2], rev([False])):
        dopath(ps, st_Thick+tr)
    
    for ps in draw(ps2, [ps0, ps1], rev([True, False, True])):
        dopath(ps, st_Thick+tr)
    
    timeslice(x0, y0+H, 0.3, t1)
    
    for i in range(3):
        c.fill(path.circle(i*w, 0., 0.06), tr)
        c.fill(path.circle(i*w, H, 0.06), tr)


def braid_id(x0=0., y0=0., H=3.0, t0="", t1=""):

    tr = [trafo.translate(x0, y0)]

    timeslice(x0, y0, 0., t0)

    for i in range(3):
        x = i*w
        c.stroke(path.line(x, 0., x, H), st_Thick+tr)

    timeslice(x0, y0+H, 0.3, t1)
    
    for i in range(3):
        c.fill(path.circle(i*w, 0., 0.06), tr)
        c.fill(path.circle(i*w, H, 0.06), tr)



c = canvas.canvas()


# hole spacing
w = 1.0
W = 3*w

# total hight
H = 1.8

N = 100


ps0 = []
ps1 = []
ps2 = []
for i in range(N+1):
    r = 1.*i/N
    y = r*H
    r = bump(r)

    x = 0.
    ps0.append((x, y))

    x = w + 0.5*w*(1 - cos(1*pi*r))
    ps1.append((x, y))

    x = 2*w - 0.5*w*(1 - cos(1*pi*r))
    ps2.append((x, y))

y0, y1 = -0.3, 0.3

timeslice(0., 0., 0.)

for ps in draw(ps0, [ps1, ps2], []):
    dopath(ps, st_Thick)

for ps in draw(ps1, [ps0, ps2], [False]):
    dopath(ps, st_Thick)

for ps in draw(ps2, [ps0, ps1], [True]):
    dopath(ps, st_Thick)


timeslice(0., H, 0.3)

ps0 = []
ps1 = []
ps2 = []
for i in range(N+1):
    r = 1.*i/N
    y = r*H
    r = bump(r)

    x = 0.
    ps0.append((x, y))

    x = w + 0.5*w*(1 - cos(2*pi*r))
    ps1.append((x, y))

    x = 2*w - 0.5*w*(1 - cos(2*pi*r))
    ps2.append((x, y))

tr = [trafo.translate(0., H)]

for ps in draw(ps0, [ps1, ps2], []):
    dopath(ps, st_Thick+[trafo.translate(2*w, H)])

for ps in draw(ps1, [ps0, ps2], [True, False]):
    dopath(ps, st_Thick+[trafo.translate(-w, H)])

for ps in draw(ps2, [ps0, ps1], [False, True]):
    dopath(ps, st_Thick+[trafo.translate(-w, H)])


timeslice(0., 2*H, 0.3)

for i in range(3):
    c.fill(path.circle(i*w, 0., 0.06))
    c.fill(path.circle(i*w, H, 0.06))
    c.fill(path.circle(i*w, 2*H, 0.06))

c.text(4*w, H, "$=$")

braid_1(6*w, 0.4*H, 1.2*H)


c.writePDFfile("pic-braid-compose.pdf")


#############################################################################
#
#


c = canvas.canvas()


# hole spacing
w = 1.0
W = 3*w

# total hight
H = 2.5

N = 100


braid_1(0., 0., H)
braid_1(0., H, H, inverse=True)

c.text(4*w, H, "$=$")


braid_id(6*w, 0.5*H, H)


c.writePDFfile("pic-braid-inverse.pdf")


#############################################################################
#
#


c = canvas.canvas()


# hole spacing
w = 0.8
W = 3*w

# total hight
H = 2.5

N = 100

ps0 = []
ps1 = []
for i in range(N+1):
    r = 1.*i/N
    y = r*H
    r = bump(r)

    x = 3*w + 0.5*w*(1 - cos(pi*r))
    ps0.append((x, y))

    x = 3*w + 0.5*w*(1 + cos(pi*r))
    ps1.append((x, y))


for frame in [0, 1]:

    X = 11.5*w*frame

    tr = [trafo.translate(X, 0.)]
    timeslice(X, 0., 0., W=7*w)
    
    for ps in draw(ps0, [ps1, ps2], [not frame]):
        dopath(ps, st_Thick+tr)
    
    for ps in draw(ps1, [ps0, ps2], [frame]):
        dopath(ps, st_Thick+tr)
    
    for i in [0, 1, 6]:
        c.stroke(path.line(i*w, 0., i*w, H), st_Thick+tr)
    
    timeslice(X, H, 0.3, W=7*w)
    
    labels = "1 2 ... i i+1 ... n".split()
    for ii, i in enumerate([0, 1, 3, 4, 6]):
        c.fill(path.circle(i*w, 0., 0.06), tr)
        c.fill(path.circle(i*w, H, 0.06), tr)
    
    if not frame:
        c.text(-2.4*w, 0.5*H, r"$\sigma_i =$", center+tr)
    else:
        c.text(-2.4*w, 0.5*H, r"$\sigma_i^{-1} =$", center+tr)

    for i in range(7):
        c.text(i*w, -0.7, "$%s$"%labels[i], center+tr)
        if i==2 or i==5:
            c.text(i*w, 0.5*H, "$%s$"%labels[i], center+tr)


c.writePDFfile("pic-braid-sigma.pdf")



#############################################################################
#
#

c = canvas.canvas()


# hole spacing
w = 1.0
W = 3*w

# total hight
H = 2.8

N = 100

def cos_up(theta): # 0 -> 1 -> 0
    return 0.5 - 0.5*cos(theta)

def cos_dn(theta): # 0 -> -1 -> 0
    return -cos_up(theta)


for frame in range(2):

    X = 7.5*w*frame

    ps0 = []
    ps1 = []
    ps2 = []
    for i in range(N+1):
        r = 1.*i/N
        y = r*H
        #r = bump(r)
    
        x = 2*w*cos_up(pi*r)
        ps0.append((x, y))
    
        if frame == 0:
            x = w + cos_dn(2*pi*r)
        else:
            x = w + cos_up(2*pi*r)
        ps1.append((x, y))
    
        x = 2*w + 2*w*cos_dn(pi*r)
        ps2.append((x, y))
    
    tr = [trafo.translate(X, 0.)]
    
    if frame == 0:
        c.text(-4.0*w, 0.5*H, r"$\sigma_i\sigma_{i+1}\sigma_i =$", tr)
    else:
        c.text(-3.0*w, 0.5*H, r"$=$", tr)
        c.text(+4.5*w, 0.5*H, r"$=\sigma_{i+1}\sigma_i\sigma_{i+1}$", tr)

    #c.text(-1.*w, 0.5*H, "$...$", tr)
    #c.text(3.*w, 0.5*H, "$...$", tr)
    c.text(-1.*w, -0.6, "$...$", tr)
    c.text(2.7*w, -0.6, "$...$", tr)
    for i in range(3):
        c.text(i*w, -0.6, "$i$ $i+1$ $i+2$".split()[i], center+tr)
    
    timeslice(X-1*w, 0., 0., W=5*w)
    
    for ps in draw(ps0, [ps1, ps2], [True, True]):
        dopath(ps, st_Thick+tr)
    
    for ps in draw(ps1, [ps0, ps2], [frame, not frame]):
        dopath(ps, st_Thick+tr)
    
    for ps in draw(ps2, [ps0, ps1], [False, False]):
        dopath(ps, st_Thick+tr)
    
    timeslice(X-1*w, H, 0.3, W=5*w)
    
    for i in range(3):
        c.fill(path.circle(i*w, 0., 0.06), tr)
        c.fill(path.circle(i*w, H, 0.06), tr)


c.writePDFfile("pic-braid-YB.pdf")



