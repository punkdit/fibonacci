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



g_arrow = [green, style.linewidth.THick]

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

c = canvas.canvas()


x = 0.
y = 0.
m = 0.1*w
m0 = m/2
r = 0.3*w

c.fill(path.rect(x-m0, y-m0, 2*m0+w, 2*m0+h), [shade])
c.stroke(path.rect(x, y, w, h))

p = path.path(
    path.moveto(x+r, y-m), 
    path.lineto(x+r, y),
    path.arc(x, y, r, 0, 90),
    path.lineto(x-m, y+r), 
)
c.stroke(p, g_arrow+[trafo.scale(1.0, 1.3, x=x, y=y-m)])

c.stroke(path.line(x+0.5*w, y-m, x+0.5*w, y+h+m), g_arrow)

r = 0.2*w
p = path.path(
    path.moveto(x+w+m, y+0.5*h+r), 
    path.lineto(x+w, y+0.5*h+r), 
    path.arc(x+w, y+0.5*h, r, 90, 270),
    path.lineto(x+w+m, y+0.5*h-r), 
)
c.stroke(p, g_arrow+[trafo.scale(1.4, 1.0, x=x+1.*w+m, y=y+0.5*h)])


x += w + 6*m

c.fill(path.rect(x-m0, y-m0, 2*m0+w, 2*m0+h), [shade])
c.stroke(path.rect(x, y, w, h))

r = 0.2*w
p = path.path(
    path.moveto(x+0.4*w, y+1.0*h+m), 
    path.lineto(x+0.4*w, y+1.0*h), 
    path.arc(x+0.6*w, y+1.0*h, r, 180, 0),
    path.lineto(x+0.8*w, y+1.0*h+m), 
)
c.stroke(p, g_arrow+[trafo.scale(1.0, 1.5, x=x+0.3*w, y=y+1.0*h+m)])

c.stroke(path.line(x+w+m, y+0.5*h, x+w-1.6*r, y+0.5*h), g_arrow) #+[deco.earrow(size=0.2)])

r = 0.7*h
p = path.path(
    path.moveto(x+r, y-m),
    path.lineto(x+r, y),
    path.arc(x, y, r, 0, 90),
    path.lineto(x-m, y+r),
)
c.stroke(p, g_arrow)

r = 0.3*h
p = path.path(
    path.moveto(x+r, y-m),
    path.lineto(x+r, y),
    path.arc(x, y, r, 0, 90),
    path.lineto(x-m, y+r),
)
c.stroke(p, g_arrow)

c.writePDFfile("pic-cells.pdf")


c = canvas.canvas()


x = 0.
y = 0.
m = 0.1*w
m0 = m/2
r = 0.3*w


c.fill(path.rect(x-m0, y-m0, 2*m0+w, 2*m0+h), [shade])
c.stroke(path.rect(x, y, w, h))

c.stroke(path.line(x+1.3*w, y+0.6*h, x+w+m, y+0.6*h), g_arrow+st_dotted)
c.stroke(path.line(x+w+m, y+0.6*h, x+0.5*w, y+0.6*h), g_arrow) #+[deco.earrow(size=0.2)])
c.stroke(path.line(x+w+m, y+0.6*h, x+0.6*w, y+0.6*h), g_arrow+[deco.earrow(size=0.2)])
c.stroke(path.line(x+0.5*w, y+0.6*h, x+0.2*w, y+0.6*h), g_arrow+st_dotted)
c.stroke(path.line(x+w-m, y+0.6*h, x+w-m, 0.2*h), st_tau+[deco.earrow(size=0.2)])
anyon(x+w-m, y+0.6*h)

c.stroke(path.line(x+1.3*w, y+0.2*h, x+w+m, y+0.2*h), g_arrow+st_dotted)
c.stroke(path.line(x+w+m, y+0.2*h, x+0.5*w, y+0.2*h), g_arrow) #+[deco.earrow(size=0.2)])
c.stroke(path.line(x+w+m, y+0.2*h, x+0.6*w, y+0.2*h), g_arrow)
c.stroke(path.line(x+0.5*w, y+0.2*h, x+0.2*w, y+0.2*h), g_arrow+st_dotted)

c.writePDFfile("pic-move-anyon.pdf")

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


w = 1.0
h = 1.0
r = 0.3*h

c = canvas.canvas()

x = 0.
y = 0.

#c.fill(path.circle(0, 0, 0.1))
#c.fill(path.circle(-w, 0, 0.1))

g = g_arrow+[deco.earrow(size=0.2)]
a = st_tau+[deco.earrow(size=0.2)]
Turtle(x, y, -pi/2).fwd(w).left(pi, r).fwd(w).stroke(g)
Turtle(x-0.5, y, pi).fwd(2*r).stroke(a)
anyon(x-0.5*w, y)
c.text(x-2.2*w, y-r, r"$-2:$", east)

c.text(x+1.2*w, y, r"$=$", center)
Turtle(x+5*w, y, -pi/2).fwd(3*w).stroke(g)
Turtle(x+4.5*w, y, 7*pi/6).right(2./3*pi, 1.1*w).stroke(a)
anyon(x+4.5*w, y)

y -= 4*r
Turtle(x, y, -pi/2).fwd(w).left(pi, 2*r).fwd(w).left(pi, r).fwd(w).stroke(g)
Turtle(x-0.5, y, pi).fwd(2*r).stroke(a)
anyon(x-0.5*w, y)
c.text(x-2.2*w, y-2*r, r"$-4:$", east)

y -= 2*r
c.text(x+1.2*w, y, r"$=$", center)
Turtle(x+5*w, y, -pi/2).fwd(3*w).stroke(g)
Turtle(x+4.5*w, y, 5*pi/4)\
    .right(0.35*pi, 2.2*w)\
    .right(0.20*pi, 0.8*w)\
    .right(0.20*pi, 0.5*w)\
    .right(pi, 0.45*w).stroke(a)
anyon(x+4.5*w, y)

y -= 6*r
Turtle(x, y, -pi/2).fwd(w).right(pi, r).fwd(w).right(pi, 2*r).fwd(w).stroke(g)
Turtle(x-0.5, y, pi).fwd(2*r).stroke(a)
anyon(x-0.5*w, y)
c.text(x-2.2*w, y, r"$+4:$", east)
c.text(x+1.2*w, y, r"$=$", center)

Turtle(x+5*w, y, -pi/2).fwd(3*w).stroke(g)
Turtle(x+4.5*w, y, pi)\
    .left(pi, 0.45*w)\
    .left(0.20*pi, 0.5*w)\
    .left(0.20*pi, 0.8*w)\
    .left(0.35*pi, 2.2*w)\
.stroke(a)
anyon(x+4.5*w, y)

y -= 6*r
Turtle(x, y, -pi/2).fwd(w).right(pi, r).fwd(w).right(pi, 3*r).fwd(w).right(pi, r).fwd(w).stroke(g)
Turtle(x-0.5, y, pi).fwd(2*r).stroke(a)
anyon(x-0.5*w, y)
c.text(x-2.2*w, y-r, r"$+6:$", east)
c.text(x+1.2*w, y, r"$=$", center)

Turtle(x+5*w, y, -pi/2).fwd(3*w).stroke(g)
Turtle(x+4.5*w, y, pi)\
    .left(1.35*pi, 0.45*w)\
    .left(0.30*pi, 3.4*w)\
    .left(1.35*pi, 0.45*w)\
.stroke(a)
anyon(x+4.5*w, y)


c.writePDFfile("pic-paperclip.pdf")


sys.exit(0)


#############################################################################
#
#


class Tracer(object):
    def __init__(self, x0, y0, r, theta):
        self.x0 = x0
        self.y0 = y0
        self.theta = theta
        self.r = r
        self.ps = []

    def get(self):
        theta = self.theta
        r = self.r
        x = self.x0 + r*sin(theta)
        y = self.y0 + r*cos(theta)
        return x, y

    def reset(self, r):
        # recalculate x0, y0
        if r==self.r:
            return
        x1, y1 = self.get()
        theta = self.theta
        self.x0 = x1 - r*sin(theta)
        self.y0 = y1 - r*cos(theta)
        self.r = r

    def trace(self, r=None, dtheta=0.05*pi):
        theta = self.theta
        if r is not None:
            self.reset(r)
        self.ps.append(self.get())
        if self.r > 0:
            self.theta = theta + dtheta
        else:
            self.theta = theta - dtheta

    def __call__(self, count=1, r=None):
        icount = int(count)
        for i in range(icount):
            self.trace(r)
        fcount = count - icount
        if fcount<1e-6:
            return
        self.trace(r, fcount*0.05*pi)

    def dopath(self, *args, **kw):
        dopath(self.ps, *args, **kw)


r = 0.5
w = 2.0

c = canvas.canvas()

push()

for count in range(2):
    push()
    
    ellipse(w, 0., 1.0*r, 1.8*r, fill=[shade])
    
    tracer = Tracer(w, r, 0.4*r, -0.8*pi)
    tracer(21.5, 0.4*r)
    tracer(8, 2.2*r)
    tracer(15.5, 0.6*r)
    tracer(5, 1.7*r)
    tracer(22, 0.3*r)
    #tracer(2., 2*r)
    tracer(5.1, -1*r)
    tracer(17.5, -0.3*r)
    tracer(10.4, -1.28*r)
    
    if count==1:
        tracer.dopath(closepath=True)
    
    if count==0:
        c.stroke(path.line(0., r, w, r), [style.linewidth.thick, red])
    
    N = 60
    ps1, ps2 = [], []
    
    x = 0.
    y = 1.
    dx = 1./(N-1)
    
    dys = [0.]*N
    N0 = 18
    N1 = 30
    N2 = 42
    N01 = (N0+N1)//2
    N12 = (N1+N2)//2
    
    for i in range(N0):
        x, y = 1.*i/(N-1), 1.
        ps1.append((w*x, 0.5*r*y-0.5*r))
        ps2.append((w*x, -0.5*r*y-0.5*r))
    
    for i in range(N0, N2):
        x = 1.*i/(N-1)
        t = 1.*(i-N0)/((N2-N0)-1)
        theta = 2*pi*t
        y = cos(theta)
        ps1.append((w*x, 0.5*r*y-0.5*r))
        ps2.append((w*x, -0.5*r*y-0.5*r))
    
    
    for i in range(N2, N):
        x, y = 1.*i/(N-1), 1.
        ps1.append((w*x, 0.5*r*y-0.5*r))
        ps2.append((w*x, -0.5*r*y-0.5*r))
    
    
    if count==0:
        for ps in (ps1[:N12-1], ps1[N12+1:]):
            dopath(ps, [style.linewidth.thick, red], closepath=False)
        
        for ps in (ps2[:N01-1], ps2[N01+1:]):
            dopath(ps, [style.linewidth.thick, red], closepath=False)
    
    ellipse(0., 0.,    1.0*r, 1.8*r, [white], fill=[shade])
    ellipse(0., 0.,    1.0*r, 1.8*r)

    if count==1:
        ellipse(0., 0.5*r, 0.7*r, 1.0*r)
    
    anyon(0., r)
    anyon(0., 0.)
    anyon(0., -r)
    
    anyon(w, r)
    anyon(w, 0.)
    anyon(w, -r)

    if count==0:
        pop()
    else:
        pop([trafo.translate(0., 8*r)])


pop([trafo.rotate(-90)])


x = -3.0*r
y = 0.0*r

c.text(x, y, r"$\sigma_1^{2}\ket{\psi}$", center)

y -= 4.0*r
c.text(x, y, r"$\ket{\psi}$", center)
c.stroke(path.line(x, y+r, x, -r), [deco.earrow(size=0.2)])
c.stroke(path.line(x-0.1, y+r, x+0.1, y+r))
 

x = +5.0*r
y = 0.0*r

c.text(x, y, r"$D_3$", center)

c.text(x-0.5*r, y-2.0*r, r"$f$", east)

y -= 4.0*r
c.text(x, y, r"$D_3$", center)
c.stroke(path.line(x, -r, x, y+r), [deco.earrow(size=0.2)])
 


c.writePDFfile("pic-interaction.pdf")



###############################################################################

def ellipse(x, y, radius, sx=1., sy=1., color=None, extra=[], arrow=None):
    p = path.circle(x, y, radius)
    t = trafo.scale(sx=sx, sy=sy)
    if color:
        c.fill(p, [t, shade]+extra)
    c.stroke(p, [t]+extra)
    if arrow is not None:
        c.stroke(p, [t]+extra+[deco.earrow(size=arrow)])

#def clip_ellipse(x, y, radius, sx=1., sy=1., extra=[]):
#    p = path.circle(x, y, radius)
#    t = trafo.scale(sx=sx, sy=sy)
#    c.clip(p, [t]+extra)


def hole(x, y, radius, msg=None, extra=[], arrow=None):
    p = path.circle(x, y, radius)
    c.fill(p, [white]+extra)
    c.stroke(p, extra)
    if arrow is not None:
        c.stroke(p, extra+[deco.earrow(size=arrow)])
    if msg:
        c.text(x, y, msg, [text.halign.boxcenter, text.valign.middle])
    

def arrowcircle(x, y, r, ar=0.1):
    p = path.circle(x, y, r)
    c.stroke(p)
    c.stroke(p, [deco.earrow(size=ar)])


###############################################################################

c = canvas.canvas()


p = path.circle(0.25, 0, 0.6)
t = trafo.scale(sx=3., sy=0.8)
c.fill(p, [t, shade])
t = trafo.scale(sx=2.6, sy=0.7)
c.stroke(p, [t])

p = path.circle(0.25, 0, 0.6)
t = trafo.scale(sx=1.5, sy=0.5)
c.stroke(p, [t])

p = path.circle(0.20, 0, 0.6)
t = trafo.scale(sx=0.8, sy=0.3)
c.stroke(p, [t])

xs = [0.0, 0.4, 1.0, 1.8]
for x in xs:
    hole(x, 0, 0.1)

dy = 0.3

y = -2.0*dy
x0, x1, x2, x3 = xs
x01 = (x0+x1)/2.0
x012 = (x0+x1+x2)/3.0
x0123 = (x0+x1+x2+x3)/4.0

c.stroke(path.line(x0, y, x01, y-dy), st_tau)
c.stroke(path.line(x1, y, x01, y-dy), st_tau)
c.stroke(path.line(x01, y-dy, x012, y-2*dy), st_tau)

c.stroke(path.line(x2, y, x012, y-2*dy), st_tau)
c.stroke(path.line(x012, y-2*dy, x0123, y-3*dy), st_tau)

c.stroke(path.line(x3, y, x0123, y-3*dy), st_tau)
c.stroke(path.line(x0123, y-3*dy, x0123, y-4*dy), st_tau)

c.writePDFfile("pic-tree-0.pdf")

    
###############################################################################

c = canvas.canvas()

p = path.circle(0.9, 0, 1.4)
t = trafo.scale(sx=1.1, sy=0.4)
c.fill(p, [t, shade])
t = trafo.scale(sx=1.0, sy=0.3)
c.stroke(p, [t])


p = path.circle(0.3, 0, 0.6)
t = trafo.scale(sx=1.0, sy=0.4)
c.stroke(p, [t])

p = path.circle(1.6, 0, 0.6)
t = trafo.scale(sx=1.0, sy=0.4)
c.stroke(p, [t])

xs = [0.0, 0.6, 1.2, 1.8]
for x in xs:
    hole(x, 0, 0.1)


y = -2.0*dy
x0, x1, x2, x3 = xs
x01 = (x0+x1)/2.0
x23 = (x2+x3)/2.0
x012 = (x0+x1+x2)/3.0
x0123 = (x0+x1+x2+x3)/4.0

c.stroke(path.line(x0, y, x01, y-dy), st_tau)
c.stroke(path.line(x1, y, x01, y-dy), st_tau)
c.stroke(path.line(x01, y-dy, x0123, y-3*dy), st_tau)

c.stroke(path.line(x2, y, x23, y-1*dy), st_tau)
c.stroke(path.line(x012, y-2*dy, x0123, y-3*dy), st_tau)

c.stroke(path.line(x3, y, x0123, y-3*dy), st_tau)
c.stroke(path.line(x0123, y-3*dy, x0123, y-4*dy), st_tau)

c.writePDFfile("pic-tree-1.pdf")


###############################################################################

p = path.circle(0., 0., 1.)
c = canvas.canvas() # [canvas.clip(p)])


t = trafo.translate(-0.8, 0.)
#ellipse(-0.5, 0., 0.5, 2.0, 1., shade, [t])
ellipse(-0.5, 0., 0.5, 2.0, 2., shade, [t])

#g_arrow = [green, deco.earrow(size=0.1)]
c.stroke(path.line(-2., 0., 0., 0.), [t]+g_arrow) 


t = trafo.translate(+1.8, 0.)

ellipse(0.0, 0., 1.0, 1., 1., shade, [t])

x = -1.
y = 0.
N = 800
pts = []
for i in range(N+1):
    pts.append((x, y))
    #y += 2./N
    x += 2./N

from twist import twist
pts = [twist(x, y, pi, 0.25, 0.8, 0.25) for (x, y) in pts]
pts = [twist(x, y, -pi, 0.25, 0.8, -0.25) for (x, y) in pts]

pts = [path.moveto(*pts[0])] + [path.lineto(*p) for p in pts[1:]]

c.stroke(path.path(*pts), [deformer.smoothed(2.0), t]+g_arrow)

c1 = canvas.canvas() # [canvas.clip(p)])
c1.insert(c, [trafo.scale(1., 0.6)])

c = c1

t = trafo.translate(-0.8, 0.)
hole(-1.5, 0., 0.07, '', [t])
hole(-1.0, 0., 0.07, '', [t])
hole(-0.5, 0., 0.07, '', [t])

t = trafo.translate(+1.8, 0.)
hole(-0.5, 0., 0.07, '', [t])
hole(-0.0, 0., 0.07, '', [t])
hole(+0.5, 0., 0.07, '', [t])

c.text(0.0, -0.3, r"$f$", [text.halign.boxcenter, text.valign.middle])
c.stroke(path.line(-0.5, 0, 0.5, 0), [style.linewidth.Thick, deco.earrow(size=0.2)])


c.writePDFfile("pic-twist.pdf")
#yield c, "pic-twist.pdf"



sys.exit(0)

###############################################################################

c = canvas.canvas()

p = lambda x : path.path(path.moveto(-0.5, -0.5), path.lineto(x, 1.), path.lineto(0.5, 2.5))

for x in [+1, +0.5, 0.0, -0.5, -1.]:
    c.stroke(p(x), [style.linewidth.THick, deformer.smoothed(3.0), grey])
c.stroke(p(-1.5), [style.linewidth.THick, deformer.smoothed(3.0), style.linestyle.dashed])
c.stroke(p(+1.5), [style.linewidth.THick, deformer.smoothed(3.0)])

c.stroke(path.line(-0.6, 1., +0.6, 1.), [deco.earrow(size=0.2)])

#c.writePDFfile("pic-isotopy.pdf")
#yield c, "pic-isotopy.pdf"


###############################################################################

N = 16
dx = 1.
dy = 2.
sz = 0.4

c = canvas.canvas()
x = 0.

for i in range(N):
    c.stroke(path.line(x, 0., x, dy),
        [style.linewidth.Thick, deco.earrow(size=sz)])
    x += dx

#c.writePDFfile("pic-spins.pdf")
#yield c, "pic-spins.pdf"

c = canvas.canvas()
x = 0.

up_spin = range(N)
dn_spin = [up_spin.pop(4), up_spin.pop(10), up_spin.pop(10)]

for i in up_spin:
    x = i*dx
    c.stroke(path.line(x, 0., x, dy),
        [style.linewidth.Thick, deco.earrow(size=sz)])

for i in dn_spin:
    x = i*dx
    c.stroke(path.line(x, dy, x, 0.),
        [style.linewidth.Thick, deco.earrow(size=sz)])
    if i-1 not in dn_spin:
        c.fill(path.circle(x-dx/2, 0.5*dy, dx/4), [red])
    if i+1 not in dn_spin:
        c.fill(path.circle(x+dx/2, 0.5*dy, dx/4), [red])

#c.writePDFfile("pic-spins-frust.pdf")
#yield c, "pic-spins-frust.pdf"


###############################################################################

c = canvas.canvas()
    
#c.fill(path.circle(0., 0., 1.), [shade])
#c.stroke(path.circle(0., 0., 1.))
#hole(0., 0., 0.3)

dy = 1.0

c.text(0., 4*dy, r"{\Large Quantum field theory}", [text.halign.boxcenter, text.valign.middle])

c.stroke(path.line(0., 3.7*dy, 0., 2.3*dy), 
    [style.linewidth.Thick, deco.earrow(size=0.4)])

c.text(0.5, 3.0*dy, "forget scale, keep angles", [text.halign.boxleft])

c.text(0., 2*dy, r"{\Large Conformal field theory}", [text.halign.boxcenter, text.valign.middle])

c.stroke(path.line(0., 1.7*dy, 0., 0.3*dy), 
    [style.linewidth.Thick, deco.earrow(size=0.4)])

c.text(0.5, 1.0*dy, "forget metric", [text.halign.boxleft])

c.text(0., 0*dy, r"{\Large Topological field theory}", [text.halign.boxcenter, text.valign.middle])

#c.writePDFfile("pic-forgetting.pdf")
#yield c, "pic-forgetting.pdf"



###############################################################################

c = canvas.canvas()
    

c.fill(path.circle(0., 0., 1.), [shade])
c.stroke(path.circle(0., 0., 1.))
c.stroke(path.circle(0., 0., 1.), [deco.earrow(size=0.2),
    trafo.scale(sx=1., sy=-1.)])

hole(0., 0., 0.3, arrow=0.2)

c.text(1.5, 0., r"$=$", [text.halign.boxcenter, text.valign.middle])

#c.writePDFfile("pic-anulus.pdf")
#yield c, "pic-anulus.pdf"


###############################################################################

c = canvas.canvas()

#c.fill(path.circle(x, y, radius), [shade])
#c.stroke(path.circle(x, y, radius), [style.linewidth.Thick])


def wiggle(x0, y0, radius, wiggle=0.3, n=1):
    seed(n)
    
    items = []
#    theta = 0.
    theta = 2*pi
    while theta > 0:
        r = radius + wiggle*random()
        p = [x0+r*sin(theta), y0+r*cos(theta)]
        items.append(p)
        theta -= 0.3*pi*random()
    
    #print items
    items = [path.moveto(*items[0])] + [path.lineto(*p) for p in items[1:]]\
        + [path.lineto(*items[0])] 
    items = path.path(*items)

    return items


p = wiggle(0, 0, 0.75, 0.3, 1)
c.fill(p, [shade, deformer.smoothed(2.0)])
#c.stroke(items, [style.linewidth.Thick])
    
#c.fill(path.circle(0., 0., 0.4), [shade])
#
#c.fill(path.circle(0, 0, 0.2), [white])

#arrowcircle(0., 0., 0.2)

p = wiggle(0, 0, 0.3, 0.2, 3)
c.stroke(p, [style.linewidth.Thick, deco.earrow(size=0.2), deformer.smoothed(2.0)])
c.stroke(p, [style.linewidth.Thick, deformer.smoothed(2.0)])

r = 0.08
c.fill(path.circle(-0.15, -0.1, r), [white])
c.fill(path.circle(0.2, 0.5, r), [white])
c.fill(path.circle(0.3, -0.05, r), [white])

c.text(0., 0., r"?", [text.halign.boxcenter, text.valign.middle])


c.writePDFfile("pic-observable.pdf")
#yield c, "pic-observable.pdf"
    
###############################################################################

c = canvas.canvas()

for x in [-3, 3]:
    p = wiggle(x+0, 0, 2.0, 0.3, 3)
    c.fill(p, [shade, deformer.smoothed(2.0), trafo.scale(1., 0.6)])
    
    p = wiggle(x-1., 0., 0.2, 0.3, 4)
    c.fill(p, [white, deformer.smoothed(2.0)])
    
    p = wiggle(x+1., 0., 0.2, 0.3, 5)
    c.fill(p, [white, deformer.smoothed(2.0)])

w = style.linewidth.Thick

x = -3
p = path.rect(x-1.5, -0.6, 1., 1.2)
c.stroke(p, [deco.earrow(size=0.2), w])

p = path.rect(x-0.4, -0.6, 0.8, 1.2)
c.stroke(p, [deco.earrow(size=0.2), w, style.linestyle.dashed])

p = path.rect(x+0.5, -0.6, 1., 1.2)
c.stroke(p, [deco.earrow(size=0.2), w])

x = +3
p = path.rect(x-1.5, -0.6, 3., 1.2)
c.stroke(p, [deco.earrow(size=0.2), w])

c.text(-0.2, -0.2, r"$=$", [trafo.scale(sx=2., sy=2.)])

c.writePDFfile("pic-abelian.pdf")
#yield c, "pic-abelian.pdf"

#sys.exit(0)

###############################################################################

for i in range(2):
    c = canvas.canvas()
        
    dx = 2.5
    dy = -0.7 if i else -1.
    DY = 9*dy if i else 5.*dy
    x = 0.
    
    c.text(x, 0.15, "Environment", [text.halign.boxcenter, text.valign.bottom])
    c.stroke(path.line(x, 0., x, DY), [style.linewidth.THICK, blue])
    
    x += dx
    c.text(x, 0.1, "System", [text.halign.boxcenter, text.valign.bottom])
    c.stroke(path.line(x, 0., x, DY), [style.linewidth.THICK, blue])
    
    x += dx
    c.text(x, 0.1, "Apparatus", [text.halign.boxcenter, text.valign.bottom])
    c.stroke(path.line(x, 0., x, DY), [style.linewidth.THICK, blue])
    
    y = dy
    x = 0.
    mx = 0.2
    my = 0.2
    
    c.stroke(path.line(x+mx, y, x+dx-mx, y), [deco.earrow(size=0.3)])
    c.text(x+0.5*dx, y+my, "noise", [text.halign.boxcenter, text.valign.bottom])
    
    y+=dy
    x+=dx
    
    c.stroke(path.line(x+dx-mx, y, x+mx, y), [deco.earrow(size=0.3)])
    c.text(x+0.5*dx, y+my, "measure", [text.halign.boxcenter, text.valign.bottom])
    
    y+=dy
    c.stroke(path.line(x+mx, y, x+dx-mx, y), [deco.earrow(size=0.3)])
    c.text(x+0.5*dx, y+my, "syndrome", [text.halign.boxcenter, text.valign.bottom])
    
    y+=dy
    c.stroke(path.line(x+dx-mx, y, x+mx, y), [deco.earrow(size=0.3)])
    c.text(x+0.5*dx, y+my, "correct", [text.halign.boxcenter, text.valign.bottom])
    
    if i==1:
        y+=dy
        c.text(x+0.5*dx, y+my, "...", [text.halign.boxcenter, text.valign.bottom])
    
        y+=dy
        c.stroke(path.line(x+dx-mx, y, x+mx, y), [deco.earrow(size=0.3)])
        c.text(x+0.5*dx, y+my, "measure", [text.halign.boxcenter, text.valign.bottom])
        
        y+=dy
        c.stroke(path.line(x+mx, y, x+dx-mx, y), [deco.earrow(size=0.3)])
        c.text(x+0.5*dx, y+my, "syndrome", [text.halign.boxcenter, text.valign.bottom])
        
        y+=dy
        c.stroke(path.line(x+dx-mx, y, x+mx, y), [deco.earrow(size=0.3)])
        c.text(x+0.5*dx, y+my, "correct", [text.halign.boxcenter, text.valign.bottom])
        
    
    #c.writePDFfile("pic-simulation-%d.pdf"%i)
#yield c, "pic-simulation-%d.pdf"%i


###############################################################################

c = canvas.canvas()


p = path.circle(0.4, 0, 0.6)
t = trafo.scale(sx=6., sy=1.2)
c.fill(p, [t, shade])
t = trafo.scale(sx=5., sy=1.)
c.stroke(p, [t])

p = path.circle(0.4, 0, 0.6)
t = trafo.scale(sx=3., sy=0.8)
c.stroke(p, [t])

p = path.circle(0.3, 0, 0.6)
t = trafo.scale(sx=1.3, sy=0.5)
c.stroke(p, [t])

hole(0, 0, 0.2)
hole(0.8, 0, 0.2)
hole(2.0, 0, 0.2)
hole(4.0, 0, 0.2)

c.writePDFfile("pic-commuting-0.pdf")
#yield c, "pic-commuting-0.pdf"

    
###############################################################################

c = canvas.canvas()


p = path.circle(0.4, 0, 0.6)
t = trafo.scale(sx=6., sy=1.2)
c.fill(p, [t, shade])
t = trafo.scale(sx=5., sy=1.)
c.stroke(p, [t])

p = path.circle(0.3, 0, 0.6)
t = trafo.scale(sx=1.3, sy=0.6)
c.stroke(p, [t])

p = path.circle(3.6/1.3, 0, 0.6)
t = trafo.scale(sx=1.3, sy=0.6)
c.stroke(p, [t])

hole(0, 0, 0.2)
hole(0.8, 0, 0.2)
hole(3.2, 0, 0.2)
hole(4.0, 0, 0.2)

c.writePDFfile("pic-commuting-1.pdf")
#yield c, "pic-commuting-1.pdf"

    
################################################################################
#
#c = canvas.canvas()
#
#arrow = lambda sz=0.3 : deco.earrow(size=sz)
#
#p = path.circle(0.4, 0, 0.6)
#t = trafo.scale(sx=5., sy=1.)
#c.fill(p, [t, shade])
#c.stroke(p, [t, arrow(0.25)])
#
#p = path.circle(0.4, 0, 0.6)
#t = trafo.scale(sx=3., sy=0.8)
#c.stroke(p, [t, arrow(0.25)])
#
#p = path.circle(0.3, 0, 0.6)
#t = trafo.scale(sx=1.3, sy=0.5)
#c.stroke(p, [t, arrow(0.25)])
#
#hole(0, 0, 0.2, arrow=0.2)
#hole(0.8, 0, 0.2, arrow=0.2)
#hole(2.0, 0, 0.2, arrow=0.2)
#hole(4.0, 0, 0.2, arrow=0.2)
#
##c.writePDFfile("pic-commuting-0-arrows.pdf")
#yield c, "pic-commuting-0-arrows.pdf"
#
    
###############################################################################

c = canvas.canvas()


p = path.circle(0.0, 0, 0.6)
t = trafo.scale(sx=6., sy=1.2)
c.fill(p, [t, shade])

p = path.circle(-0.3, 0, 0.7)
t = trafo.scale(sx=3., sy=0.6)
c.stroke(p, [t])

p = path.circle(+0.3, 0, 0.7)
t = trafo.scale(sx=3., sy=0.8)
c.stroke(p, [t])

for x in [-1.5, -0.5, 0.5, 1.5]:
    hole(x, 0, 0.2)

c.writePDFfile("pic-noncommuting.pdf")
#yield c, "pic-noncommuting.pdf"

c = canvas.canvas()

x, y = 0., 0.
radius = 0.5

#c.fill(path.circle(x, y, radius), [shade])
#c.stroke(path.circle(x, y, radius), [style.linewidth.Thick])

seed(0)

items = []
theta = 0.
while theta < 2*pi:
    r = 1.5*radius * random()
    p = [r*sin(theta), r*cos(theta)]
    items.append(p)
    theta += 0.3*pi*random()

#print items
items = [path.moveto(*items[0])] + [path.lineto(*p) for p in items[1:]]\
    + [path.lineto(*items[0])] 
items = path.path(*items)

c.fill(items, [shade])
c.stroke(items, [style.linewidth.Thick])

x += 1.

c.text(x-0.1, y-0.1, r"$=$")

x += 1.

c.fill(path.circle(x, y, radius), [shade])
c.stroke(path.circle(x, y, radius), [style.linewidth.Thick])

x += 1.

c.text(x-0.1, y-0.1, r"$\ne$")

x += 1.

c.fill(path.circle(x, y, radius), [shade])
c.stroke(path.circle(x, y, radius), [style.linewidth.Thick])

c.fill(path.circle(x, y, radius/2), [white])
c.stroke(path.circle(x, y, radius/2), [style.linewidth.Thick])

c.writePDFfile("pic-topological.pdf")
#yield c, "pic-topological.pdf"


###############################################################################


def mkpath(x, y, radius=1.):

    pts = []
    pts.append((x+0.07*radius, y+0.05*radius))
    pts.append((x+0.5*radius, y+0.3*radius))
    pts.append((x+0.5*radius, y-0.3*radius))
    pts.append((x+0.07*radius, y-0.05*radius))

    pts = [path.moveto(*pts[0])] + [path.lineto(*p) for p in pts[1:]]

    pts = path.path(*pts)
    return pts


c = canvas.canvas()

x, y = 0., 0.
radius = 0.07
c.stroke(path.circle(x, y, radius), [style.linewidth.thick])
c.stroke(path.circle(x+1, y, radius), [style.linewidth.thick])


c.stroke(mkpath(x, y, 3),
    [deformer.smoothed(2.0),
    style.linewidth.Thick, deco.earrow(size=0.2)])

x += 2

c.text(x-0.1, y-0.1, r"$=$")

x += 1

c.stroke(path.circle(x, y, radius), [style.linewidth.thick])
c.stroke(path.circle(x+1, y, radius), [style.linewidth.thick])
c.stroke(mkpath(x, y, 1.4),
    [deformer.smoothed(2.0),
    style.linewidth.Thick, deco.earrow(size=0.2)])


x += 2

c.text(x-0.1, y-0.1, r"$=$")

x += 1

c.stroke(path.circle(x, y, radius), [style.linewidth.thick])
c.stroke(path.circle(x+1, y, radius), [style.linewidth.thick])


c.writePDFfile("pic-monodromy.pdf")
#yield c, "pic-monodromy.pdf"


###############################################################################

c = canvas.canvas()

x, y = 0., 0.
radius = 0.07
c.stroke(path.circle(x, y, radius), [style.linewidth.thick])
c.stroke(path.circle(x+1, y, radius), [style.linewidth.thick])
c.stroke(mkpath(x, y, 3),
    [deformer.smoothed(2.0),
    style.linewidth.Thick, deco.earrow(size=0.2)])

x += 2

c.text(x-0.1, y-0.1, r"$\ne$")

x += 1

c.stroke(path.circle(x, y, radius), [style.linewidth.thick])
c.stroke(path.circle(x+1, y, radius), [style.linewidth.thick])
c.stroke(mkpath(x, y, 1.4),
    [deformer.smoothed(2.0),
    style.linewidth.Thick, deco.earrow(size=0.2)])


c.writePDFfile("pic-monodromy-2d.pdf")
#yield c, "pic-monodromy-2d.pdf"


###############################################################################

c = canvas.canvas()

c.fill(path.circle(0., 0., 0.4), [shade])

c.fill(path.circle(0, 0, 0.2), [white])

arrowcircle(0., 0., 0.2)

c.text(0., 0., r"?", [text.halign.boxcenter, text.valign.middle])

c.writePDFfile("pic-observe.pdf")
#yield c, "pic-observe.pdf"




###############################################################################

c = canvas.canvas()

arrowcircle(1.5, 0, 0.2)
arrowcircle(2.8, 0, 0.2)

c.text(0, 0, r"$\ket{\psi} = \alpha\ket{\ I \ } + \beta\ket{\ \tau \ }.$",
    [text.valign.middle])

c.writePDFfile("pic-observe-state.pdf")
#yield c, "pic-observe-state.pdf"


###############################################################################

c = canvas.canvas()

p = path.circle(0.3, 0, 0.6)
t = trafo.scale(sx=1.7, sy=1.1)
c.fill(p, [t, shade])
#c.stroke(p, [t])

ellipse(0.3, 0., 0.6, 1.5, 0.9, shade, arrow=0.1)

hole(0, 0, 0.2, r"$\tau$", arrow=0.1)
hole(0.8, 0, 0.2, r"$\tau$", arrow=0.1)

c.text(0.4, -0.2, r"?", [text.halign.boxcenter, text.valign.middle])

c.writePDFfile("pic-fusion.pdf")
#yield c, "pic-fusion.pdf"


###############################################################################

c = canvas.canvas()


p = path.circle(0.4, 0, 0.6)
t = trafo.scale(sx=6., sy=1.1)
c.fill(p, [t, shade])
t = trafo.scale(sx=5., sy=1.)
c.stroke(p, [t])

p = path.circle(0.4, 0, 0.6)
t = trafo.scale(sx=3., sy=0.8)
c.stroke(p, [t])

p = path.circle(0.3, 0, 0.6)
t = trafo.scale(sx=1.3, sy=0.5)
c.stroke(p, [t])

hole(0, 0, 0.2, r"$\tau$")
hole(0.8, 0, 0.2, r"$\tau$")
hole(2.0, 0, 0.2, r"$\tau$")
hole(4.0, 0, 0.2, r"$\tau$")

c.text(0.4, -0.1, r"?", [text.halign.boxcenter, text.valign.middle])
c.text(1.4, -0.2, r"?", [text.halign.boxcenter, text.valign.middle])
c.text(3.4, -0.3, r"?", [text.halign.boxcenter, text.valign.middle])


c.writePDFfile("pic-fibonacci-1.pdf")
#yield c, "pic-fibonacci-1.pdf"


###############################################################################

c = canvas.canvas()

t = trafo.translate(0., 0.)
ellipse(-0.5, 0., 0.5, 2.0, 2., shade, [t])
hole(-1.5, 0., 0.07, '', [t])
hole(-1.0, 0., 0.07, '', [t])
hole(-0.5, 0., 0.07, '', [t])

c.writePDFfile("pic-D_3.pdf")
#yield c, "pic-D_3.pdf"


###############################################################################

c = canvas.canvas()

t = trafo.translate(-0.4, 0.)
#ellipse(-0.5, 0., 0.5, 2.0, 1., shade, [t])
ellipse(-0.5, 0., 0.5, 2.0, 2., shade, [t])
hole(-1.5, 0., 0.07, '', [t])
hole(-1.0, 0., 0.07, '', [t])
hole(-0.5, 0., 0.07, '', [t])

c.text(0., 0., r"$=$", [text.halign.boxcenter, text.valign.middle])

#ellipse(+0.7, 0., 0.5, 1.5, 1., shade)

t = trafo.translate(+2.4, 0.)
ellipse(-0.5, 0., 0.5, 2.0, 2., shade, [t])
hole(-1.5, 0., 0.07, '', [t])
hole(-1.0, 0., 0.07, '', [t])
hole(-0.5, 0., 0.07, '', [t])

c.writePDFfile("pic-equals.pdf")
#yield c, "pic-equals.pdf"


###############################################################################

c = canvas.canvas()

t = trafo.translate(-0.8, 0.)
#ellipse(-0.5, 0., 0.5, 2.0, 1., shade, [t])
ellipse(-0.5, 0., 0.5, 2.0, 2., shade, [t])
hole(-1.5, 0., 0.07, '', [t])
hole(-1.0, 0., 0.07, '', [t])
hole(-0.5, 0., 0.07, '', [t])

c.text(0.0, -0.3, r"$f$", [text.halign.boxcenter, text.valign.middle])

c.stroke(path.line(-0.5, 0, 0.5, 0),
    [style.linewidth.Thick, deco.earrow(size=0.2)])

t = trafo.translate(+2.8, 0.)
ellipse(-0.5, 0., 0.5, 2.0, 2., shade, [t])
hole(-1.5, 0., 0.07, '', [t])
hole(-1.0, 0., 0.07, '', [t])
hole(-0.5, 0., 0.07, '', [t])

c.writePDFfile("pic-mcg.pdf")
#yield c, "pic-mcg.pdf"


###############################################################################

#p = path.circle(0., 0., 1.)
c = canvas.canvas() # [canvas.clip(p)])


t = trafo.translate(-0.8, 0.)
st = trafo.scale(sx=1., sy=0.8)
#ellipse(-0.5, 0., 0.5, 2.0, 1., shade, [t])
ellipse(-0.5, 0., 0.5, 2.0, 2., shade, [t, st])

radius = 0.5
x0, y0 = -1.25, 0.
tt = trafo.scale(sx=1., sy=0.8)
c.stroke(path.circle(-1.25, 0., radius), [t, tt])

hole(-1.5, 0., 0.07, '', [t])
hole(-1.0, 0., 0.07, '', [t])
hole(-0.5, 0., 0.07, '', [t])

c.text(0.0, -0.3, r"$f$", [text.halign.boxcenter, text.valign.middle])

c.stroke(path.line(-0.5, 0, 0.5, 0),
    [style.linewidth.Thick, deco.earrow(size=0.2)])


t = trafo.translate(+1.8, 0.)

ellipse(0.0, 0., 1.0, 1., 1., shade, [t, st])

x0 += 1.

N = 200
pts = []
for i in range(N+1):
    r = 2*pi*i/N
    x = radius*sin(r) + x0
    y = 0.8*radius*cos(r) + y0
    pts.append((x, y))

from twist import twist
pts = [twist(x, y, -2*pi, 0.25, 0.7, 0.25) for (x, y) in pts]

pts = [path.moveto(*pts[0])] + [path.lineto(*p) for p in pts[1:]]
wiggle = path.path(*pts)
c.stroke(wiggle, [deformer.smoothed(2.0), t])

hole(-0.5, 0., 0.07, '', [t])
hole(-0.0, 0., 0.07, '', [t])
hole(+0.5, 0., 0.07, '', [t])

##c.writePDFfile("pic-mcg-observable.pdf") # XXX fixy fixy
#yield c, "pic-mcg-observable.pdf"


###############################################################################

c = canvas.canvas()


def slice(x, y):
    p = path.circle(x, y, 1.)
    t = trafo.scale(1., 0.3, x, y)
    c.fill(p, [shade, t])
    c.stroke(p, [t])

    hole(x-0.5, y, 0.07, '')
    hole(x, y, 0.07, '')
    hole(x+0.5, y, 0.07, '')


st = [text.valign.middle, text.halign.boxcenter]

m = 2.
x = -3.5

slice(-m, 0.)
c.text(x, 0., r"$\ket{\psi}$", st)

def braid(n, i, t, inverse=False):

    if not isinstance(t, list):
        t = [t]

    t = t + [style.linewidth.Thick, red, style.linecap.round]

    N = 10

    if i is None:
        items = range(n)
    else:
        assert 0<=i<i+1<n
        items = range(i)+range(i+2, n)
    
    for k in items:
        c.stroke(path.line(0.5*k, 0., 0.5*k, 1.), t)

    if i is None:
        return

    pts0 = []
    for j in range(N):
        theta = pi*j/(N-1)
        x = 0.5 * 0.5 * (cos(theta)-1.) + 0.5*(i+1)
        y = 1.*j/(N-1)
        pts0.append((x, y))

    pts1 = []
    for j in range(N):
        theta = pi*j/(N-1)
        x = 0.5 * 0.5 * (1.-cos(theta)) + 0.5*i
        y = 1.*j/(N-1)
        pts1.append((x, y))

    if inverse:
        pts0, pts1 = pts1, pts0

    pts = [path.moveto(*pts0[0])] + [path.lineto(*p) for p in pts0[1:]]
    wiggle = path.path(*pts)
    c.stroke(wiggle, [deformer.smoothed(2.0)]+t)

    c.fill(path.circle(0.5*(i+0.5), 0.5, 0.15), t+[white])

    pts = [path.moveto(*pts1[0])] + [path.lineto(*p) for p in pts1[1:]]
    wiggle = path.path(*pts)
    c.stroke(wiggle, [deformer.smoothed(2.0)]+t)


braid(3, 1, trafo.translate(-m-0.5, 0.))
braid(3, 1, trafo.translate(-m-0.5, 1.))

slice(-m, 2.)
c.text(x, 2., r"$\sigma_2^{2}\ket{\psi}$", st)

s = [style.linewidth.Thick, deco.earrow(size=0.2)]
c.stroke(path.line(x, 0.3, x, 1.7), s)
flat = [deco.earrow(angle=170, size=0.1)]
c.stroke(path.line(x, 1.7, x, 0.3), flat+[style.linewidth.Thick])

c.text(x-0.5, -1.0,
    "Braid group acts on states:\ \ \ \ \ \ \ \ \ \  \  ``Schrodinger picture''",
    [text.parbox(4.), text.valign.top, text.halign.flushleft])

# %%%%%%%%%%%%%%%%

x = +0.5

slice(+m, +2.)
c.stroke(path.circle(m-0.25, 2., 0.5), [trafo.scale(1., 0.3, m-0.25, 2.)])
c.text(x, 2., r"$D_3$", st)

slice(+m, 0.)
c.stroke(wiggle, [trafo.translate(m, 0.), trafo.scale(1., 0.4, m, 0.)])

c.text(x, 0., r"$D_3$", st)
c.text(x-0.2, 1., r"$f$", st)
s = [style.linewidth.Thick, deco.earrow(size=0.2)]
c.stroke(path.line(x, 1.7, x, 0.3), s)

c.text(x-0.5, -1.0,
    "Mapping class group acts on observables: ``Heisenberg picture''",
    [text.parbox(4.), text.valign.top, text.halign.flushleft])


##c.writePDFfile("pic-braid-mcg.pdf") # XXX fixy fixy
#yield c, "pic-braid-mcg.pdf"


###############################################################################

c = canvas.canvas()


c.text(-3., 0.5, "$\sigma_1 =$", [text.valign.middle])
braid(3, 0, [trafo.translate(-2., 0.2), trafo.scale(1., 0.8)])

c.text(-0., 0.5, "$\sigma_2 =$", [text.valign.middle])
braid(3, 1, [trafo.translate(1., 0.2), trafo.scale(1., 0.8)])


c.writePDFfile("pic-braid-group.pdf")
#yield c, "pic-braid-group.pdf"

###############################################################################

c = canvas.canvas()


c.text(-1.5, 0.5, "$\sigma_1^{-1}\sigma_1 =$", [text.valign.middle])

braid(3, 0, [trafo.translate(0.2, 0.), trafo.scale(1., 0.5, 0., 0.)])
braid(3, 0, [trafo.translate(0.2, 1.), trafo.scale(1., 0.5, 0., 0.)], inverse=True)

c.text(+1.4, 0.5, "$=$", [text.valign.middle])

braid(3, None, [trafo.translate(2.0, 0.)])

c.writePDFfile("pic-braid-group-1.pdf")
#yield c, "pic-braid-group-1.pdf"

###############################################################################

c = canvas.canvas()

c.text(-1.8, 0.5, "$\sigma_1\sigma_2\sigma_1 =$", [text.valign.middle])

braid(3, 0, [trafo.translate(0.2, 0.), trafo.scale(1., 1./3, 0., 0.)])
braid(3, 1, [trafo.translate(0.2, 1.), trafo.scale(1., 1./3, 0., 0.)])
braid(3, 0, [trafo.translate(0.2, 2.), trafo.scale(1., 1./3, 0., 0.)])

c.text(+1.4, 0.5, "$=$", [text.valign.middle])

braid(3, 1, [trafo.translate(2., 0.), trafo.scale(1., 1./3, 0., 0.)])
braid(3, 0, [trafo.translate(2., 1.), trafo.scale(1., 1./3, 0., 0.)])
braid(3, 1, [trafo.translate(2., 2.), trafo.scale(1., 1./3, 0., 0.)])

c.text(+3.2, 0.5, "$= \sigma_2\sigma_1\sigma_2$", [text.valign.middle])

c.writePDFfile("pic-braid-relation.pdf")
#yield c, "pic-braid-relation.pdf"


