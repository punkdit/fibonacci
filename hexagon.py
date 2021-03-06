#!/usr/bin/env python

import sys
from math import *
from random import *
import numpy

from pyx import canvas, path, deco, trafo, style, text, color, deformer

text.set(mode="latex") 
text.set(docopt="10pt")
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

    def right(self, dtheta, r=0., penup=False):
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
            if not penup:
                self.ps.append((x, y))
        self.x = x
        self.y = y
        if penup:
            self.ps = [(x, y)] # HACK
        return self

    def left(self, dtheta, r=0., penup=False):
        self.right(-dtheta, -r, penup=penup)
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


w, h = 1.5, 1.5

r = 0.7*w
r0 = 0.06*w


###############################################################################
#
#

c = canvas.canvas()

x, y = 0., 0.

r = 0.7*w
r0 = 0.07*w

circle(x, y, r, shade, mark=True)

r1 = 0.29*w
theta = 1.8*pi
theta1 = 1.05*pi
r2 = 0.09*w
theta2 = 0.2*pi
r3 = 0.6*w
Turtle(x-1.1*r, y, 1*pi/2).\
    left(0.05*theta, r1, penup=True).\
    left(0.15*theta, r1).right(+0.4*theta, r1).left(0.2*theta, r1).\
    fwd(0.1*r).right(theta1, r2).right(theta2, r3).left(theta2, r3).left(theta1, r2).fwd(0.1*r).\
    right(0.2*theta, r1).left(0.4*theta, r1).right(0.15*theta, r1).\
    stroke(st_curve)

circle(x-0.5*r, y, r0, white, mark=True)
circle(x+0.5*r, y, r0, white, mark=True)

c.text(x+0.5*r, y+0.14*h, r"$a$", southwest)
c.text(x-0.5*r, y-0.14*h, r"$b$", northeast)
c.text(x+r, y-r, r"${c}$", southeast)

x += 1.5*w

#c.text(x, y, r"$\to$", center)
x0 = x-0.4*w
c.stroke(path.line(x0, y, x+0.4*w, y), [deco.earrow()])
c.stroke(path.line(x0, y-0.1, x0, y+0.1))
c.text(x, y+0.3*h, r"$R_c^{ab}$", center)

x += 1.5*w

circle(x, y, r, shade, mark=True)

c.stroke(path.line(x-1.0*r, y, x+1.0*r, y), st_curve)

circle(x-0.5*r, y, r0, white, mark=True)
circle(x+0.5*r, y, r0, white, mark=True)

c.text(x-0.5*r, y-0.14*h, r"$b$", northeast)
c.text(x+0.5*r, y+0.14*h, r"$a$", southwest)
c.text(x+r, y-r, r"${c}$", southeast)


c.writePDFfile("pic-rmove-1.pdf")


###############################################################################
#
#

def tetra(x, y, count=None, subcount=None, rev=1, back=True, front=True, reflect=False):

    if back:
        circle(x, y, r, shade)

    rr = 1.0*r
    if subcount is not None:
        ps = []
        for i in range(3):
            theta1 = rev*2*(i+subcount)*pi/3
            if i==0:
                # start of curve
                x1, y1 = x+rr*sin(theta1), y+rr*cos(theta1)
                ps.append((x1, y1))
            if i==1:
                x1, y1 = x+0.7*r*sin(theta1), y+0.7*r*cos(theta1)
                ps.append((x1, y1))
            else:
                x1, y1 = x+0.4*r*sin(theta1), y+0.4*r*cos(theta1)
                ps.append((x1, y1))
            if i==2:
                # end of curve
                x1, y1 = x+1.0*rr*sin(theta1), y+1.0*rr*cos(theta1)
                ps.append((x1, y1))
        c.stroke(path.path(
            path.moveto(*ps[0]),
            path.lineto(*ps[1]),
            path.lineto(*ps[2]), 
            path.lineto(*ps[3]), 
            path.lineto(*ps[4])), 
            st_curve+[deformer.smoothed(0.6)])

    if front:
        for theta1 in [0., 2*pi/3, 4*pi/3]:
            x1, y1 = x+0.5*r*sin(theta1), y+0.5*r*cos(theta1)
            circle(x1, y1, r0, white)

    if count is not None:

        assert 0<=count<=2
        s = 0.86*r
        r1 = 2.4*r0
        extra = []
        #c.text(x, y, count)
        if reflect:
            #count = [0, 1, 2][count]
            extra.append(trafo.scale(x=x, y=y, sx=-1, sy=1))
        extra += [trafo.rotate(-count*120, x=x, y=y)]
        t = Turtle(x1, y1-r1, -pi/2).right(pi, r1).fwd(s).right(pi, r1).fwd(s)
        t.stroke(extra)
        t.stroke(extra+[deco.earrow()])


c = canvas.canvas()

R = 1.7*r

for i in range(3):
    theta = 2*i*pi/3
    x, y = R*sin(theta), R*cos(theta)
    tetra(x, y, [1, 0, 2][i], reflect=(i in [0,1]))

    w = 30 + 120*i
    c.stroke(path.path(path.arc(0., 0., 1.1*R, w-20, w+20)), [deco.earrow()])
    c.stroke(path.path(path.arcn(0., 0., 1.1*R, w+20, w-20)), [deco.earrow()])
    theta = 2*(i+0.5)*pi/3
    x, y = 1.3*R*sin(theta), 1.3*R*cos(theta)
    c.text(x, y, "$F$", center)

c.writePDFfile("pic-fmove-relation.pdf")


c = canvas.canvas()

R = 1.7*r

for i in range(3):
    theta = 2*i*pi/3
    x, y = R*sin(theta), R*cos(theta)
    tetra(x, y, [2, 1, 0][i], reflect=(i in [0,2]))

    w = 30 + 120*i
    c.stroke(path.path(path.arc(0., 0., 1.1*R, w-20, w+20)), [deco.earrow()])
    c.stroke(path.path(path.arcn(0., 0., 1.1*R, w+20, w-20)), [deco.earrow()])
    theta = 2*(i+0.5)*pi/3
    x, y = 1.3*R*sin(theta), 1.3*R*cos(theta)
    c.text(x, y, "$F$", center)

c.writePDFfile("pic-fmove-relation-r.pdf")



c = canvas.canvas()

x, y = 0., 0.

R = 3*r


for i in range(6):
    theta = i*pi/3
    x, y = R*sin(theta), R*cos(theta)

    tetra(x, y, 
        [1, 0, 2][i//2],
        [2, 3, 3, 3, 3, 5][i],
        [1, -1, -1, 1, 1, 1][i], # reverse arrow
        reflect=[True, True, False][i//2],
    )
    #c.text(x, y, str(i), center) # debug numbering

    # Arrows
    w = 60*i
    if i == 3:
        c.stroke(path.path(path.arc(0., 0., 1.1*R, w-10, w+10)), [deco.earrow()])
    else:
        c.stroke(path.path(path.arcn(0., 0., 1.1*R, w+10, w-10)), [deco.earrow()])

    # Arrow labels
    theta = (i+0.5)*pi/3
    x, y = 1.25*R*sin(theta), 1.25*R*cos(theta)
    labels = "R^{-1} F R^{-1} F R F".split()
    c.text(x, y, "$%s$"%labels[i], center)


c.writePDFfile("pic-hexagon.pdf")


c = canvas.canvas()

x, y = 0., 0.

R = 3*r


for i in range(6):
    theta = i*pi/3
    x, y = R*sin(theta), R*cos(theta)

    tetra(x, y, 
        [2, 1, 0][(i+1)//2%3],
        [ 2,  2,  3,  3,  3,  3][i],
        [-1, -1, -1, -1,  1,  1][i], # reverse arrow
        reflect=[True, False, True][(i+1)//2%3],
    )
    #c.text(x, y, str(i), center) # debug numbering

    # Arrows
    w = 60*i
    if i != 0:
        c.stroke(path.path(path.arc(0., 0., 1.1*R, w-10, w+10)), [deco.earrow()])
    else:
        c.stroke(path.path(path.arcn(0., 0., 1.1*R, w+10, w-10)), [deco.earrow()])

    # Arrow labels
    theta = (i+0.5)*pi/3
    x, y = 1.25*R*sin(theta), 1.25*R*cos(theta)
    labels = "F R^{-1} F R F R".split()
    c.text(x, y, "$%s$"%labels[i], center)


c.writePDFfile("pic-hexagon-r.pdf")




###############################################################################
#
#

c = canvas.canvas()

x, y = 0., 0.

w, h = 1.5, 1.5

r0 = 0.8*w
r1 = 0.4*r0
r2 = 0.1*r0


circle(x, y, 1.2*r0, shade)

circle(x+r1, y+r1, r2, white)
circle(x-r1, y+r1, r2, white)
circle(x-r1, y-r1, r2, white)
circle(x+r1, y-r1, r2, white)


r3 = 2*r2
Turtle(x-r1, y+r1+r3, pi/2).fwd(2*r1).right(pi, r3).fwd(2*r1).right(pi, r3).stroke()

r3 = 2.8*r2
Turtle(x-r1, y+r1+r3, pi/2).fwd(2*r1).right(3*pi/4, r3).\
    fwd(1.42*2*r1).right(3*pi/4, r3).fwd(2*r1).right(pi/2, r3).stroke(closepath=True)


r3 = 3.4*r2
Turtle(x+r1+r3, y+r1, pi).fwd(2*r1).right(pi, r3)\
    .fwd(2*r1).right(pi, r3).stroke(st_dashed)


c.text(x+1.9*r1, y, "$\gamma$", west)

c.writePDFfile("pic-refactor.pdf")



