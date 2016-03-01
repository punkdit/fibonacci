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



st_curve = g_curve = [green, style.linewidth.THick]

st_tau = [style.linewidth.Thick, red, style.linecap.round]
#st_vac = [style.linewidth.thick, red]+st_dotted

st_arrow = [deco.earrow()]



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

SINGLE_COLUMN = False




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

    def stroke(self, extra=[], fill=[], closepath=False, reverse=False):
        ps = list(reversed(self.ps)) if reverse else self.ps
        dopath(ps, extra, fill, closepath, smooth=0.)
        return self



#############################################################################
#
#

#def mathtext(x, y, text, *extra):
#    if text[0]=='$':
#        text = text[1:]
#    if text[-1]=='$':
#        text = text[:-1]
#    c.text(x, y, r"$\displaystyle %s$"%text, *extra)
#
#w = 1.5
#h = 1.5
#
#x = 0
#y = 0
#
#c = canvas.canvas()
#
##c.text(x+0.5*h, y, r"\bigoplus_a \H\bigl(", text.mathmode) #east)
#mathtext(x-0.1*w, y+0.4*h, r"$\bigoplus_a \H\Bigl($", east)
#
#r = 1.0
#x += 0.0*w
#
#p = path.circle(x+r, y+0.5*h, r)
#c.fill(p, [shade])
#c.stroke(p)
##c.fill(path.circle(x+2*r, y+0.5*h, 0.06))
#c.fill(path.circle(x+r, y+0.5*h-r, 0.06))
#
#x += 0.3*w
#p = path.circle(x+0.1*w, y+0.5*h, 0.4*r)
#c.fill(p, [white])
#c.stroke(p)
##p = path.circle(x+0.1*w+0.4*r, y+0.5*h, 0.06)
#p = path.circle(x+0.1*w, y+0.5*h-0.4*r, 0.06)
#c.fill(p)
#
#c.text(x+0.6*w, y+0.5*h, "...")
#
##c.text(x+0.1*w, y+0.0*h, "$M_a$", west)
#c.text(x+0.3*w, y+0.1*h, "$M$", west)
#
#c.text(x+0.3*w, y+0.7*h, "$a$", southwest)
#
#c.text(x+1.33*w, y+0.5*h, r"$\amalg$", center)
#
#x += 2.4*r
#
#r = 0.7
#p = path.circle(x+r, y+0.5*h, r)
#c.fill(p, [shade])
#c.stroke(p)
##p = path.circle(x+2*r, y+0.5*h, 0.06)
#p = path.circle(x+r, y+0.5*h-r, 0.06)
#c.fill(p)
#
#x += 0.3*w
#
#c.text(x+0.0*w, y+0.5*h, "...")
#
##c.text(x+0.0*w, y+0.2*h, "$N_{\hat{a}}$", west)
#c.text(x+0.1*w, y+0.3*h, "$N$", west)
#
#c.text(x+0.5*w, y+0.9*h, "$\widehat{a}$", southwest)
#
#x += 1.8*r
#mathtext(x, y+0.5*h, r"$\Bigr)$", east)
#
#if SINGLE_COLUMN:
#    x -= 0*r
#    y -= 3*r
#else:
#    x += 3*r
#
#
##c.text(x, y+0.5*h, r"$\to\H\Bigl($", east)
##c.text(x, y+0.5*h, r"$\xrightarrow{\cong}\H\Bigl($", east)
#c.text(x-0.8, y+0.5*h, r"$\H\Bigl($", west)
#c.stroke(path.line(x-2.0, y+0.5*h, x-0.9, y+0.5*h), [deco.arrow()])
#c.text(x-1.5, y+0.6*h, r"$\cong$", south)
#
#print dir(deco)
#
#r = 1.0
##x += 0.5*w
#
#p = path.circle(x+r, y+0.5*h, r)
#c.fill(p, [shade])
#c.stroke(p)
#c.stroke(p)
##c.fill(path.circle(x+2*r, y+0.5*h, 0.06))
#c.fill(path.circle(x+r, y+0.5*h-r, 0.06))
#
#x += 0.3*w
#p = path.circle(x+0.1*w, y+0.5*h, 0.4*r)
#c.stroke(p)
##p = path.circle(x+0.1*w+0.4*r, y+0.5*h, 0.06)
#p = path.circle(x+0.1*w, y+0.5*h-0.4*r, 0.06)
#c.fill(p)
#
#c.text(x+0.1*w, y+0.5*h, r"$N$", center)
##c.text(x+0.2*w, y+0.5*h, r"$...$", center)
#
#c.text(x+0.6*w, y+0.5*h, "...")
#
#c.text(x+0.3*w, y+0.1*h, "$M$", west)
#
#x += 1.8*r
#c.text(x, y+0.5*h, r"$\Bigr)$", east)
#
#
#c.writePDFfile("pic-glue.pdf")
#
#
##############################################################################
##
##
#
#w = 1.5
#h = 1.5
#
#x = 0
#y = 0
#
#c = canvas.canvas()


def surface(x, y, r, fill=shade, mark=False, orient=None):
    p = path.circle(x, y, r)
    if fill is not None:
        c.fill(p, [fill])
    c.stroke(p)
    if orient == True:
        c.stroke(p, [deco.earrow()])
    elif orient == False:
        c.stroke(p, [deco.earrow(), trafo.scale(x=x, y=y, sx=1, sy=-1)])
    if mark:
        p = path.circle(x, y-r, 0.06)
        c.fill(p)

#r = 1.0
#
#surface(x+0, y, r)
#surface(x-0.6*r, y, 0.1*r, fill=white)
#surface(x+0.0*r, y, 0.1*r, fill=white)
#surface(x+0.6*r, y, 0.1*r, fill=white)
#
#c.text(x-0.6*r, y+0.2, "$a$", south)
#c.text(x,       y+0.2, "$b$", south)
#c.text(x+0.6*r, y+0.2, "$c$", south)
#c.text(x+0.9*r, y-0.6, "$\widehat{d}$", northwest)
#
#c.stroke(path.circle(x-0.3*r, y, 0.6*r), [trafo.scale(1., 1.1, x, y)])
#c.stroke(path.circle(x+0.3*r, y, 0.6*r), [trafo.scale(1., 1.1, x, y)])
#
#c.text(x-1.5*r, y, r"$\H\Bigl($", center)
#c.text(x+1.3*r, y, r"$\Bigr)$", center)
#
#x += 4.0*r
#y -= 3.0*r
#
#surface(x-0.7*r, y, 0.6*r)
#surface(x+0.7*r, y, 0.6*r)
#labels = "aybc"
#for i, x0 in enumerate([x-0.9*r, x-0.5*r, x+0.5*r, x+0.9*r]):
#    surface(x0, y, 0.1*r, fill=white)
#    if i==1:
#        c.text(x0, y+0.13, "$%s$"%labels[i], south)
#    else:
#        c.text(x0, y+0.2, "$%s$"%labels[i], south)
#c.text(x+1.1*r, y+0.7, "$\widehat{y}$", west)
#c.text(x-1.1*r, y+0.7, "$\widehat{d}$", east)
#
#mathtext(x-1.5*r, y-0.13, r"$\bigoplus_{y\in\A}\H\Bigl($", east)
#c.text(x+1.7*r, y, r"$\Bigr)$", center)
#
#
#c.text(-0.15, y+0.2, r"$F^{abc}_d$", south)
#c.stroke(path.line(-1.0*r, y, +0.8*r, y), [deco.earrow()])
#
#x -= 7*r
#
#surface(x-0.7*r, y, 0.6*r)
#surface(x+0.7*r, y, 0.6*r)
#labels = "abxc"
#for i, x0 in enumerate([x-0.9*r, x-0.5*r, x+0.5*r, x+0.9*r]):
#    surface(x0, y, 0.1*r, fill=white)
#    c.text(x0, y+0.2, "$%s$"%labels[i], south)
#c.text(x-1.1*r, y+0.7, "$\widehat{x}$", east)
#c.text(x+1.1*r, y+0.7, "$\widehat{d}$", west)
#
#mathtext(x-1.5*r, y-0.13, r"$\bigoplus_{x\in\A}\H\Bigl($", east)
#c.text(x+1.7*r, y, r"$\Bigl)$", center)
#
#c.stroke(path.line(-3.0*r, -2.0*r, -1.5*r, -0.8*r), [deco.earrow()])
#c.text(-2.6*r, -1.4*r, "$\cong$", center)
#
#c.stroke(path.line(+3.4*r, -2.0*r, +1.9*r, -0.8*r), [deco.earrow()])
#c.text(+3.0*r, -1.4*r, "$\cong$", center)
#
#c.writePDFfile("pic-glue-fmove.pdf")
#
#
##############################################################################
##
##
#
#w = 1.5
#h = 1.5
#
#x = 0
#y = 0
#
#c = canvas.canvas()
#
#
#r = 1.4
#
#ccw = False # counter clockwise
#
#surface(x+0, y, r, mark=True, orient=ccw)
#surface(x-0.6*r, y, 0.2*r, fill=white, mark=True, orient=not ccw)
#surface(x+0.6*r, y, 0.2*r, fill=white, mark=True, orient=not ccw)
#
#
##c.text(x-0.6*r, y+0.3*r, "$a_1$", south)
#c.text(x, y, "...", center)
##c.text(x+0.6*r, y+0.3*r, "$a_n$", south)
##c.text(x+0.9*r, y-0.7*r, "$b$", north)
#
#if ccw:
#    c.stroke(path.path(path.arc(x+0.2*r, y-0.5*r, 0.15*r, 20, 330)), [deco.earrow()])
#else:
#    c.stroke(path.path(path.arc(x+0.2*r, y-0.5*r, 0.15*r, 20, 330)),
#        [deco.earrow(), trafo.scale(x=x+0.2*r, y=y-0.5*r, sx=-1,sy=1)])
#
#c.writePDFfile("pic-disc.pdf")
#
#
##############################################################################
##
##
#
#w = 1.5
#h = 1.5
#
#x = 0
#y = 0
#
#c = canvas.canvas()
#
#
#r = 1.4
#
#surface(x+0, y, r, mark=True)
#
##c.stroke(path.line(x-r, y, x+r, y), st_curve+st_arrow)
#r0 = 0.28*r
#c.stroke(path.line(x-r, y, x-r0, y), st_curve)
#c.stroke(path.line(x-r0, y, x+r0, y), st_curve+st_dotted)
#c.stroke(path.line(x+r0, y, x+r, y), st_curve+st_arrow)
#
#r1 = 0.15*r
#surface(x-0.6*r, y, r1, fill=white, mark=True)
#surface(x+0.6*r, y, r1, fill=white, mark=True)
#
#
#c.text(x-0.6*r, y+0.2*r, "$a_1$", south)
##c.text(x, y-r1, "...", center)
#c.text(x, y+0.2*r, "...", south)
#c.text(x+0.6*r, y+0.2*r, "$a_n$", south)
#c.text(x+0.9*r, y-0.7*r, r"$\widehat{b}$", north)
#
#
#c.writePDFfile("pic-disc-standard.pdf")
#
#
##############################################################################
##
##
#
#w = 1.5
#h = 1.5
#
#x = 0
#y = 0
#
#c = canvas.canvas()
#
#
#r0 = 1.3
##surface(x, y, r0)
##c.fill(path.circle(x, y+r0, 0.04))
#c.fill(path.circle(x, y, r0), [shade])
#
#
#r = 0.15
#dx = 4*r
#x1 = x-1.5*dx
#
#t = Turtle(x1, y, 0.*pi)
#t.right(pi, 1.5*dx)
#t.stroke(g_curve+[style.linecap.round])
#
#t = Turtle(x1-0.4*dx, y, 0.*pi)
#t.right(pi, 1.9*dx)
#t.right(pi, 0.4*dx)
#t.left(pi, 1.1*dx)
#t.right(pi, 0.4*dx)
#t.stroke()
#
#t = Turtle(x1-0.4*dx, y, pi)
#t.fwd(0.01)
#t.stroke(st_arrow)
#
#c.stroke(path.circle(x, y, dx), [trafo.scale(0.9, 0.7)])
#c.stroke(path.circle(x, y, dx), st_arrow+[trafo.scale(0.9, 0.7)])
#
#r = 0.12
#
#t = Turtle(x1+1*dx, y, pi/2)
#t.fwd(dx)
#t.stroke(g_curve+[style.linecap.round])
#
#for i in range(4):
#    surface(x1, y, r, white)
#    #c.fill(path.circle(x1, y+r, 0.04))
#    x1 += dx
#
#
#c.writePDFfile("pic-2-curve.pdf")
#
#
##############################################################################
##
##
#
#c = canvas.canvas()
#
#
#r0 = 1.3
#
#
#r = 0.2
#dx = 4*r
#x1 = x-1.5*dx
#
#c.fill(path.circle(x+0.2*dx, y, r0), [shade, trafo.scale(1.8, 0.7)])
#
#
#r = 0.12
#
#t = Turtle(x1-0.8*dx, y, pi/2)
#t.fwd(4.8*dx)
##t.stroke(g_curve+st_dotted)
#t.stroke(g_curve)
#
#for i in range(3):
#    t = Turtle(x1, y, pi/2)
#    t.fwd(dx)
#    #t.stroke(g_curve+[style.linecap.round])
#
#    surface(x1, y, r, white)
#    #c.fill(path.circle(x1, y+r, 0.04))
#
#    c.stroke(path.circle(x1+0.5*dx, y, dx), [trafo.scale(0.9, 0.6, x=x1+0.5*dx, y=0)])
#    c.stroke(path.circle(x1+0.5*dx, y, dx), st_arrow+[trafo.scale(0.9, 0.6, x=x1+0.5*dx, y=0)])
#    x1 += dx
#
#surface(x1, y, r, white)
##c.fill(path.circle(x1, y+r, 0.04))
#
#
##c.text(x-2.2*dx, y-r, "...", north)
#c.text(x+2.4*dx, y-2*r, "...", north)
#
#c.writePDFfile("pic-chain.pdf")
#
#
##############################################################################
##
##
#
#
#w = 1.2
#h = 1.5
#
#x = 0
#y = 0
#
#c = canvas.canvas()
#
#c.text(x, y+0.5*h, r"$V^{ab}_{c} := \H\Bigl($", east)
#
#r = 2*w/3.
#x += 0.0*w
#
#surface(x+r, y+0.5*h, r, mark=True)
#
#x += 0.3*w
#surface(x+0.1*w, y+0.5*h, 0.2*r, white, mark=True)
#
#c.text(x+0.1*w, y+0.65*h, "$a$", south)
#
#x += 0.6*w
#surface(x+0.1*w, y+0.5*h, 0.2*r, white, mark=True)
#
#c.text(x+0.1*w, y+0.65*h, "$b$", south)
#
#
#c.text(x+0.25*w, y+1.0*h, "$\widehat{c}$", southwest)
#
#x += 1.0*r
#mathtext(x, y+0.5*h, r"$\Bigr)$", east)
#
#
#c.writePDFfile("pic-pop.pdf")


#############################################################################
#
#


if 0:
    w = 1.2
    h = 1.5
    
    x = 0
    y = 0
    
    c = canvas.canvas()
    
    
    r = 1.0
    r1 = 0.4*r
    
    surface(x, y, r, shade, mark=True)
    surface(x, y, r1, white, mark=True)
    
    c.stroke(path.line(x, y-r, x, y-r1))
    
    c.text(x-r, y+r, "$\widehat{a}$", northwest)
    c.text(x-r1, y+r1, "${a}$")
    
    c.stroke(path.line(x+1.4*r, y, x+2.6*r, y), [deco.earrow()])
    c.text(x+2.0*r, y+0.4*r, "$f_a$", center)
    
    x += 4*r
    
    surface(x, y, r, shade, mark=True)
    surface(x, y, r1, white, mark=True)
    
    t = Turtle(x, y-r, -0.45*pi)
    dr = 0.15
    r0 = 0.9*r
    for i in range(4):
        t.right(0.53*pi, r0)
        r0 -= dr
    t.stroke()
    
    c.text(x-r, y+r, "$\widehat{a}$", northwest)
    c.text(x-0.8*r1, y-r1, "${a}$", north)
    
    c.writePDFfile("pic-dehn-twist.pdf")
    

#############################################################################
#
#


w = 1.2
h = 1.5

x = 0
y = 0

c = canvas.canvas()


r = 1.0
r1 = 0.4*r

surface(x, y, r, shade, mark=True)
surface(x, y, r1, white, mark=True)

#c.stroke(path.line(x, y-r, x, y-r1))
c.stroke(path.line(x-r, y, x-r1, y), st_curve)
c.stroke(path.line(x+r1, y, x+r, y), st_curve+[deco.earrow()])

c.text(x-r, y+r, "$\widehat{a}$", northwest)
c.text(x-0.5*r1, y+0.2*r1, "${a}$")

c.stroke(path.line(x+1.4*r, y, x+2.6*r, y), [deco.earrow()])
c.text(x+2.0*r, y+0.4*r, "$f$", center)

x += 4*r

surface(x, y, r, shade, mark=True)

t = Turtle(x, y-r, -0.45*pi)
dr = 0.15
r0 = 0.90

dtheta = 0.53*pi
dtheta = 0.45*pi

st_cw = [trafo.rotate(-90, x=x, y=y)]
t.right(0.45*pi, 0.90)
#c.stroke(path.circle(t.x, t.y, 0.1), st_cw)
t.right(0.45*pi, 0.75)
#c.stroke(path.circle(t.x, t.y, 0.1), st_cw)
t.right(0.70*pi, 0.55)
#c.stroke(path.circle(t.x, t.y, 0.1), st_cw)
t.right(0.45*pi, 0.44)


t.stroke(st_curve + st_cw)

t.stroke(st_curve + [trafo.rotate(90, x=x, y=y), deco.earrow()], reverse=True)

surface(x, y, r1, white, mark=True)
c.text(x-r, y+r, "$\widehat{a}$", northwest)
c.text(x-0.5*r1, y+0.2*r1, "${a}$")

c.writePDFfile("pic-dehn-twist.pdf")





