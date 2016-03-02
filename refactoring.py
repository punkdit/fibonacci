#!/usr/bin/env python

import sys
from math import *
from random import *
import numpy

from pyx import canvas, path, deco, trafo, style, text, color, deformer

text.set(mode="latex") 
text.set(docopt="10pt")
text.preamble(r"\usepackage{amsmath,amsfonts,amssymb}")
text.preamble(r'\usepackage{mathrsfs}')
#text.preamble(r"\def\I{\mathbb{I}}")
text.preamble(r"\def\ket #1{|#1\rangle}")
text.preamble(r"\def\H{\mathscr{H}}")
text.preamble(r"\def\F{\mathscr{H}}")
text.preamble(r"\def\A{\mathcal{A}}")


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

#shade = rgb(0.75, 0.55, 0)

grey = rgb(0.75, 0.75, 0.75)
shade = grey
shade0 = rgb(0.75, 0.75, 0.75)
shade1 = rgb(0.80, 0.80, 0.80)
shade2 = rgb(0.85, 0.85, 0.85)

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


def dopath(ps, extra=[], fill=[], closepath=True, smooth=0.3):
    ps = [path.moveto(*ps[0])]+[path.lineto(*p) for p in ps[1:]]
    if closepath:
        ps.append(path.closepath())
    p = path.path(*ps)
    if fill:
        c.fill(p, [deformer.smoothed(smooth)]+extra+fill)
    c.stroke(p, [deformer.smoothed(smooth)]+extra)



class Turtle(object):
    def __init__(self, x, y, theta):
        # theta==0 is up
        # theta==pi/2 is right
        self.x = x
        self.y = y
        self.theta = theta
        self.ps = [(x, y)]

    def fwd(self, d):
        self.x += d*sin(self.theta)
        self.y += d*cos(self.theta)
        self.ps.append((self.x, self.y))
        return self

    def goto(self, x, y):
        self.x = x
        self.y = y
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



st_curve = [green, style.linewidth.THick]
st_curve = st_curve + [deco.earrow(size=0.2)]


def circle(x, y, r, shade, deco=[], mark=False):
    p = path.circle(x, y, r)
    c.fill(p, [shade])
    c.stroke(p, deco)
    if mark:
        c.fill(path.circle(x, y-r, 0.05))




###############################################################################
#
#

w, h = 2.2, 2.4

c = canvas.canvas()

r0 = 0.4*w # second hole
r1 = 1.4*w # last hole

count = 0

def manifold(x, y, labels):

    global count
    if count in [0, 2]:
        c.stroke(path.line(x-r0, y, x+r1+r0, y), st_curve)
    else:
        extra = list(st_curve)
        if count==3:
            extra.append(trafo.scale(x=x, y=y, sx=1, sy=-1))
        Turtle(x-0.85*r0, y, pi/2).\
            fwd(0.3).\
            right(0.25*pi, 0.4).left(0.50*pi, 0.73).left(0.88*pi, 0.15).\
            fwd(0.55).\
            right(0.88*pi, 0.15).right(0.50*pi, 0.73).left(0.25*pi, 0.4).goto(x+r1+r0, y).\
            stroke(extra)

#    st_target = st_curve+st_dashed
    st_target = [red, style.linewidth.THick, deco.earrow(size=0.2)]
    if count == 0:
        Turtle(x, y, 3*pi/4).left(0.95*pi/2, 2**0.5/2*r1).stroke(st_target)
    elif count == 3:
        Turtle(x-0.05, y, 0.90*pi).left(0.30*pi, 0.8).left(0.3*pi, 2.8).stroke(st_target)
    else:
        Turtle(x+r0, y, 3*pi/4).left(0.95*pi/2, 2**0.5/2*(r1-r0)).stroke(st_target)

    for i in range(3):
        _x = [x, x+r0, x+r1][i]
        p = path.circle(_x, y, 0.08)
        c.fill(p, [white])
        c.stroke(p)
        ydelta = 0.25
        xdelta = 0.00
        if count==1  and labels[i]=="a":
            ydelta = -0.35
            xdelta = +0.1
        if count==3  and labels[i]=="a":
            ydelta = -0.35
            xdelta = -0.1
        c.text(_x+xdelta, y+ydelta, r"$\scriptstyle %s$"%labels[i], south)

    c.text(x+(r0+r1)/2., y-0.2, "...", north)

    c.stroke(path.circle(x+r0/2, y, r0), [trafo.scale(x=x+r0/2, y=y, sx=1.0, sy=0.8)])

    if count in [0, 3]:
        c.text(x+r0, y+0.3*h, "$\omega$", southwest)
    else:
        c.text(x+r0, y+0.3*h, "$f(\omega)$", southwest)

    count += 1


x, y = 0., 4*h


c.text(x, y, r"$\H(M)$", center)
c.text(x-0.2*w, y-0.5*h, r"$\H(f)$", southeast)
c.stroke(path.line(x, y-0.2*h, x, y-0.8*h), [deco.earrow()])

manifold(x + w, y, "abc")


# ~~~~~~~~~~~~

y -= h

c.text(x, y, r"$\H(N)$", center)
c.text(x-0.2*w, y-0.5*h, r"$R$", southeast)
c.stroke(path.line(x, y-0.2*h, x, y-0.8*h), [deco.earrow()])

manifold(x + w, y, "bac")

# ~~~~~~~~~~~~

y -= h

c.text(x, y, r"$\H(N)$", center)
c.text(x-0.2*w, y-0.5*h, r"$\H(f^{-1})$", southeast)
c.stroke(path.line(x, y-0.2*h, x, y-0.8*h), [deco.earrow()])

manifold(x + w, y, "bac")

# ~~~~~~~~~~~~

y -= h

c.text(x, y, r"$\H(M)$", center)

manifold(x + w, y, "abc")


c.writePDFfile("pic-refactoring.pdf")



###############################################################################
#
#

w, h = 2.2, 2.4

c = canvas.canvas()

r0 = 0.4*w # second hole

count = 0

def manifold(x, y, labels):

    global count

    p = path.circle(x+r0/2, y, r0)
    extra = [trafo.scale(x=x+r0/2, y=y, sx=1.0, sy=0.8)]
    c.fill(p, extra+[shade])
    c.stroke(p, extra)

    if count in [0, 2]:
        c.stroke(path.line(x-0.5*r0, y, x+r0+0.5*r0, y), st_curve)
    else:
        extra = list(st_curve)
        if count==3:
            extra.append(trafo.scale(x=x, y=y, sx=1, sy=-1))
        Turtle(x-0.85*r0+0.3, y, pi/2).\
            right(0.25*pi, 0.4).left(0.50*pi, 0.73).left(0.88*pi, 0.15).\
            fwd(0.55).\
            right(0.88*pi, 0.15).right(0.50*pi, 0.73).left(0.25*pi, 0.4).\
            stroke(extra)

    for i in range(2):
        _x = [x, x+r0][i]
        p = path.circle(_x, y, 0.08)
        c.fill(p, [white])
        c.stroke(p)
        ydelta = 0.25
        xdelta = 0.00
        if count==1  and labels[i]=="a":
            ydelta = -0.35
            xdelta = +0.1
        if count==3  and labels[i]=="a":
            ydelta = -0.35
            xdelta = -0.1
        c.text(_x+xdelta, y+ydelta, r"$\scriptstyle %s$"%labels[i], south)

    c.text(x+1.5*r0, y-0.6, r"$\scriptstyle \hat{c}$", center)
    c.text(x+1.7*r0, y, r"$\bigr)$", center)
    c.text(x-0.9*r0, y, r"$\H\bigl($", center)

    count += 1


x, y = 0., 4*h

dy = 1.2*h

# top right
manifold(x, y, "ab")

x0, y0 = x+0.5*r0, y-0.5*dy
c.stroke(path.line(x0, y0+0.2*dy, x0, y0-0.2*dy), [deco.earrow()])
c.text(x0+0.3, y0, r"$\H(f)$", west)


# ~~~~~~~~~~~~

y -= dy

# bottom right
manifold(x, y, "ba")

# ~~~~~~~~~~~~

x -= 2*w

# bottom left
manifold(x, y, "ba")

x0, y0 = x+0.5*r0+1.0*w, y
c.stroke(path.line(x0-0.3*w, y0, x0+0.2*w, y0), [deco.earrow()])
c.text(x0, y0+0.4, "$R^{ba}_c$", center)

# ~~~~~~~~~~~~


y += dy

# top left
manifold(x, y, "ab")

x0, y0 = x+0.5*r0+1.0*w, y
c.stroke(path.line(x0-0.3*w, y0, x0+0.2*w, y0), [deco.earrow()])
c.text(x0, y0+0.4, "$R^{ab}_c$", center)

x0, y0 = x+0.5*r0, y-0.5*dy
c.stroke(path.line(x0, y0+0.2*dy, x0, y0-0.2*dy), [deco.earrow()])
c.text(x0-0.3, y0, r"$\H(f)$", east)

c.writePDFfile("pic-natural.pdf")


###############################################################################
#
#

w, h = 2.2, 2.4

c = canvas.canvas()

r0 = 0.4*w # second hole
r1 = 1.4*w # last hole

#st_target = st_curve+st_dashed
#st_target = [red, style.linewidth.THick, deco.earrow(size=0.2)]
#st_target = st_curve+st_dashed
st_target = st_curve+[
    style.linestyle(style.linecap.butt, style.dash([2], offset=1, rellengths=False))]

def manifold(x, y, labels, count):

    if count in [0, 2]:
        c.stroke(path.line(x-r0, y, x+r1+r0, y), st_curve)
    else:
        extra = list(st_curve)
        #if count==3:
        #    extra.append(trafo.scale(x=x, y=y, sx=1, sy=-1))
        Turtle(x-0.85*r0, y, pi/2).\
            fwd(0.3).\
            right(0.25*pi, 0.4).left(0.50*pi, 0.73).left(0.88*pi, 0.15).\
            fwd(0.55).\
            right(0.88*pi, 0.15).right(0.50*pi, 0.73).\
            left(0.25*pi, 0.52).goto(x+r1+r0, y).\
            stroke(extra)

    if count==0:
        c.text(x+r1+r0, y-0.2, "$f$", northwest)
    else:
        c.text(x+r1+r0, y-0.2, "$R^{a_1a_2}_{b_1}f$", northwest)

    c.text(x+(r0+r1)/2, y+0.7, "$f'$", southwest)

    if count == 0:
        Turtle(x, y, 3*pi/4).left(0.95*pi/2, 2**0.5/2*r1).stroke(st_target+[trafo.scale(x=x, y=y, sx=1, sy=-1)])
    elif count == 3:
        Turtle(x-0.05, y, 0.90*pi).left(0.30*pi, 0.8).left(0.3*pi, 2.8).\
            stroke(st_target+[trafo.scale(x=x, y=y, sx=1, sy=-1)])
    else:
        Turtle(x+r0, y, 3*pi/4).left(0.95*pi/2, 2**0.5/2*(r1-r0)).stroke(st_target)

    for i in range(3):
        _x = [x, x+r0, x+r1][i]
        p = path.circle(_x, y, 0.08)
        c.fill(p, [white])
        c.stroke(p)
        ydelta = -0.25
        xdelta = 0.00
        if count==3  and labels[i]=="a_2":
            ydelta = -0.35
            xdelta = +0.1
        if count==3  and labels[i]=="a_1":
            xdelta = -0.1
            ydelta = +0.3
        c.text(_x+xdelta, y+ydelta, r"$\scriptstyle %s$"%labels[i], center)

    x1 = x+(r0+r1)/2.
    c.text(x1, y-0.2, "...", north)

    c.fill(path.rect(x1-0.4, y-0.1, 0.8, 0.2), [white])
    c.stroke(path.line(x1-0.4, y, x1+0.4, y), [green, style.linewidth.THick]+st_dotted)

    c.stroke(path.circle(x+r0/2, y, r0), [trafo.scale(x=x+r0/2, y=y, sx=1.0, sy=0.8)])

    c.text(x, y+0.3*h, "$b_1$", southeast)


x, y = 0., 4*h

labels = "a_1 a_2 a_n".split()

manifold(x + w, y, labels, 0)

dx, dy = w, -h

x0, y0 = x + 0.7 + 0.2*dx, y - 0.2 + 0.2*dy
c.stroke(path.line(x0, y0, x0+0.6*dx, y0+0.6*dy), [deco.earrow()])
c.stroke(path.line(x0+0.03*dy, y0-0.03*dx, x0-0.03*dy, y0+0.03*dx), st_thick)

c.text(x0-0.2+0.3*dx, y0+0.3*dy, "$R^{a_1a_2}_{b_1}$", northeast)


x += 0.8*dx
y += dy

manifold(x + w, y, labels, 3)


c.writePDFfile("pic-theorem.pdf")





