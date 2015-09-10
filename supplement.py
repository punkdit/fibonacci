#!/usr/bin/env python

import sys
from math import *
from random import *
import numpy

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

def arrow(x0, y0, x1, y1, extra=[]):
    c.stroke(path.line(x0, y0, x1, y1),
        extra+[deco.earrow(size=0.1)])


w = 1.7
h = 1.3

x, y = 0., 0.
dx = 1.2*w


st_tau = [style.linewidth.Thick, red, style.linecap.round]
st_vac = [style.linewidth.thick, red]+st_dotted

def frame():
    extra = [style.linewidth.thick]
    c.stroke(path.line(x, y, x, y+h), extra)
    c.stroke(path.line(x+w, y, x+w, y+h), extra)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

c = canvas.canvas()

frame()

c.stroke(path.line(x, y+0.3*h, x+w, y+0.3*h), st_tau)
c.stroke(path.line(x, y+0.7*h, x+w, y+0.7*h), st_tau)

#c.stroke(path.line(x+0.3*w, y+0.05*h, x+0.4*w, y+0.35*h), st_vac)
c.stroke(path.line(x+0.5*w, y+0.3*h, x+0.5*w, y+0.7*h), st_vac)

x += 1.1*w
c.text(x, y+0.5*h, r"$= \phi^{-1}$", west)

x += 0.7*w
frame()
#c.stroke(path.line(x,   y+0.2*h, x+0.3*w, y+0.5*h), st_tau)
#c.stroke(path.line(x,   y+0.8*h, x+0.3*w, y+0.5*h), st_tau)
#c.stroke(path.line(x+w, y+0.2*h, x+0.7*w, y+0.5*h), st_tau)
#c.stroke(path.line(x+w, y+0.8*h, x+0.7*w, y+0.5*h), st_tau)
#c.stroke(path.circle(x+0.0*w, y+0.5*h, 0.3*w), st_tau)
c.stroke(path.path(path.arc(x+0.0*w, y+0.5*h, 0.2*w, -90, 90)), st_tau)
c.stroke(path.path(path.arc(x+1.0*w, y+0.5*h, 0.2*w, 90, -90)), st_tau)
c.stroke(path.line(x+0.2*w, y+0.5*h, x+0.8*w, y+0.5*h), st_vac)


x += 1.1*w
c.text(x, y+0.5*h, r"$+ \phi^{-\frac{1}{2}}$", west)

x += 0.7*w
frame()
#c.stroke(path.line(x,   y+0.2*h, x+0.3*w, y+0.5*h), st_tau)
#c.stroke(path.line(x,   y+0.8*h, x+0.3*w, y+0.5*h), st_tau)
#c.stroke(path.line(x+w, y+0.2*h, x+0.7*w, y+0.5*h), st_tau)
#c.stroke(path.line(x+w, y+0.8*h, x+0.7*w, y+0.5*h), st_tau)
#c.stroke(path.line(x+0.3*w, y+0.5*h, x+0.7*w, y+0.5*h), st_tau)

c.stroke(path.path(path.arc(x+0.0*w, y+0.5*h, 0.2*w, -90, 90)), st_tau)
c.stroke(path.path(path.arc(x+1.0*w, y+0.5*h, 0.2*w, 90, -90)), st_tau)
c.stroke(path.line(x+0.2*w, y+0.5*h, x+0.8*w, y+0.5*h), st_tau)

y -= 1.2*h
x = 1.1*w

c.text(x, y+0.5*h, r"$= \phi^{-1}$", west)

x += 0.7*w
frame()
#c.stroke(path.line(x+0.5*w, y+0.2*h, x+0.8*w, y+0.5*h), st_tau)
#c.stroke(path.line(x+0.5*w, y+0.8*h, x+0.8*w, y+0.5*h), st_tau)
#c.stroke(path.line(x+0.5*w, y+0.2*h, x+0.2*w, y+0.5*h), st_tau)
#c.stroke(path.line(x+0.5*w, y+0.8*h, x+0.2*w, y+0.5*h), st_tau)
c.stroke(path.circle(x+0.5*w, y+0.5*h, 0.2*w), st_tau)

c.stroke(path.line(x+0.0*w, y+0.5*h, x+0.3*w, y+0.5*h), st_vac)
c.stroke(path.line(x+0.7*w, y+0.5*h, x+1.0*w, y+0.5*h), st_vac)

x += 1.1*w
c.text(x, y+0.5*h, r"$+ \phi^{-\frac{1}{2}}$", west)

x += 0.7*w
frame()
#c.stroke(path.line(x+0.5*w, y+0.2*h, x+0.8*w, y+0.5*h), st_tau)
#c.stroke(path.line(x+0.5*w, y+0.8*h, x+0.8*w, y+0.5*h), st_tau)
#c.stroke(path.line(x+0.5*w, y+0.2*h, x+0.2*w, y+0.5*h), st_tau)
#c.stroke(path.line(x+0.5*w, y+0.8*h, x+0.2*w, y+0.5*h), st_tau)
c.stroke(path.circle(x+0.5*w, y+0.5*h, 0.2*w), st_tau)

c.stroke(path.line(x+0.0*w, y+0.5*h, x+0.3*w, y+0.5*h), st_tau)
c.stroke(path.line(x+0.7*w, y+0.5*h, x+1.0*w, y+0.5*h), st_tau)


y -= 1.2*h
x = 1.1*w

c.text(x, y+0.5*h, r"$=$", west)

x += 0.7*w
frame()

c.stroke(path.line(x, y+0.5*h, x+w, y+0.5*h), st_vac)

x += 1.3*w
c.text(x, y+0.5*h, r"$+$", west)

x += 0.5*w
frame()

c.stroke(path.line(x, y+0.5*h, x+w, y+0.5*h), st_tau)


c.writePDFfile("pic-logops.pdf")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


c = canvas.canvas()

x, y = 0., 0.

frame()

for i in range(3):
    a = 0.1*i+0.3
    c.stroke(path.line(x, y+a*h, x+w, y+(a+0.0)*h), st_tau)


dx = 0.2*w
for i in range(3, 6):
    a = 0.1*i+0.3
    c.stroke(path.line(x+0.18*w+dx, y+a*h, x+0.20*w+dx, y+(a+0.00)*h), st_tau)

c.fill(path.rect(x+0.2*w+dx, y, x+0.25*w+dx, y+h), [white])

c.text(x+0.2*w+dx, y+0.55*h, r"$\Big\} k$", west)


x += 1.1*w

c.text(x, y+0.5*h, r"$= f_{k-1}$", west)

x += 0.8*w
frame()

c.stroke(path.line(x, y+0.5*h, x+w, y+0.5*h), st_vac)

x += 1.1*w
c.text(x, y+0.5*h, r"$+ f_k$", west)

x += 0.5*w
frame()

c.stroke(path.line(x, y+0.5*h, x+w, y+0.5*h), st_tau)


c.writePDFfile("pic-kfold.pdf")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

c = canvas.canvas()

x, y = 0., 0.
dx = 1.0
dy = 1.0


#        90
#         ^
#         |
#         |
# 180<--- . ----> 0
#         |
#         |
#         v
#       -90
#
# Arcs go anti-clockwise
#

d = 2.4

r = 0.2*d
r2 = 2**0.5*r

c.stroke(path.path(path.arc(x+0.5*d, y+r2, r, -135, -45)), st_tau)
c.stroke(path.path(path.arc(x+0.5*d, y-r2, r, +45, +135)), st_tau)
c.stroke(path.line(x+0.5*d, y-r2+r, x+0.5*d, y+r2-r), st_vac)

x += 1.0*d
c.text(x, y-0.1*d, "$= \phi^{-1}$", south)

x += 0.5*d

c.stroke(path.path(path.arc(x-r2, y+0.0*d, r, -45, +45)), st_tau)
c.stroke(path.path(path.arc(x+r2, y+0.0*d, r, +135, -135)), st_tau)
c.stroke(path.line(x-r2+r, y+0.0*d, x+r2-r, y+0.0*d), st_vac)

x += 0.5*d
c.text(x, y-0.1*d, r"$+ \phi^{-\frac{1}{2}}$", south)

x += 0.5*d

c.stroke(path.path(path.arc(x-r2, y+0.0*d, r, -45, +45)), st_tau)
c.stroke(path.path(path.arc(x+r2, y+0.0*d, r, +135, -135)), st_tau)
c.stroke(path.line(x-r2+r, y+0.0*d, x+r2-r, y+0.0*d), st_tau)


x = 0.
y -= 0.5*d

c.stroke(path.path(path.arc(x+0.5*d, y+r2, r, -135, -45)), st_tau)
c.stroke(path.path(path.arc(x+0.5*d, y-r2, r, +45, +135)), st_tau)
c.stroke(path.line(x+0.5*d, y-r2+r, x+0.5*d, y+r2-r), st_tau)

x += 1.0*d
c.text(x, y-0.1*d, r"$= \phi^{-\frac{1}{2}}$", south)

x += 0.5*d

c.stroke(path.path(path.arc(x-r2, y+0.0*d, r, -45, +45)), st_tau)
c.stroke(path.path(path.arc(x+r2, y+0.0*d, r, +135, -135)), st_tau)
c.stroke(path.line(x-r2+r, y+0.0*d, x+r2-r, y+0.0*d), st_vac)

x += 0.5*d
c.text(x, y-0.1*d, "$- \phi^{-1}$", south)

x += 0.5*d

c.stroke(path.path(path.arc(x-r2, y+0.0*d, r, -45, +45)), st_tau)
c.stroke(path.path(path.arc(x+r2, y+0.0*d, r, +135, -135)), st_tau)
c.stroke(path.line(x-r2+r, y+0.0*d, x+r2-r, y+0.0*d), st_tau)


c.writePDFfile("pic-skein1.pdf")



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# R-moves

c = canvas.canvas()

x, y = 0., 0.
d = 0.6

r = 0.4*d
r12 = r/(2**0.5)

c.stroke(path.path(path.arc(x, y+1.0*d, r, +135, +45)), st_tau)
c.stroke(path.line(x+r12, y+1.0*d+r12, x+r12-1.5*r, y+1.0*d+r12+1.5*r), st_tau)
c.fill(path.circle(x, y+1.0*d+(2**0.5)*r, 0.08), [white])
c.stroke(path.line(x-r12, y+1.0*d+r12, x-r12+1.5*r, y+1.0*d+r12+1.5*r), st_tau)
c.stroke(path.line(x, y-0.0*d, x, y+1.0*d-r), st_vac)

x += 1.8*d
c.text(x, y+0.8*d, r"$= R_{\mathbb{I}}^{\tau\tau}$", south)

x += 1.6*d
c.stroke(path.path(path.arc(x, y+1.8*d, r, -155, -25)), st_tau)
c.stroke(path.line(x, y+0.3*d, x, y+1.8*d-r), st_vac)

c.text(x+0.7*d, y+0.6*d, r",", south)

x += 2.4*d

c.stroke(path.path(path.arc(x, y+1.0*d, r, +135, +45)), st_tau)
c.stroke(path.line(x+r12, y+1.0*d+r12, x+r12-1.5*r, y+1.0*d+r12+1.5*r), st_tau)
c.fill(path.circle(x, y+1.0*d+(2**0.5)*r, 0.08), [white])
c.stroke(path.line(x-r12, y+1.0*d+r12, x-r12+1.5*r, y+1.0*d+r12+1.5*r), st_tau)
c.stroke(path.line(x, y-0.0*d, x, y+1.0*d-r), st_tau)

x += 1.8*d
c.text(x, y+0.8*d, r"$= R_{\tau}^{\tau\tau}$", south)

x += 1.6*d
c.stroke(path.path(path.arc(x, y+1.8*d, r, -155, -25)), st_tau)
c.stroke(path.line(x, y+0.3*d, x, y+1.8*d-r), st_tau)


c.writePDFfile("pic-skein2.pdf")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

c = canvas.canvas()

x, y = 0., 0.

d = 0.6
r = 0.4*d

def bubble(st_1, st_2, st_3):
    c.stroke(path.line(x, y-3*r, x, y-r), st_1)
    c.stroke(path.circle(x, y, r), st_2)
    c.stroke(path.line(x, y+3*r, x, y+r), st_3)


bubble(st_vac, st_tau, st_vac)
x += 0.7*d
c.text(x, y-0.7*r, "$= \phi$", southwest)
x += 1.6*d
c.stroke(path.line(x, y-3*r, x, y+3*r), st_vac)
c.text(x+0.7*d, y-0.7*r, r",", southwest)


x += 2.0*d

bubble(st_tau, st_tau, st_tau)
x += 0.7*d
c.text(x, y-0.7*r, r"$= \phi^{\frac{1}{2}}$", southwest)
x += 1.7*d
c.stroke(path.line(x, y-3*r, x, y+3*r), st_tau)
c.text(x+0.7*d, y-0.7*r, r",", southwest)


x += 2.0*d

bubble(st_tau, st_tau, st_vac)
x += 0.7*d
c.text(x, y-0.5*r, "$=$", southwest)
x += 1.4*d
bubble(st_vac, st_tau, st_tau)
x += 0.7*d
c.text(x, y-0.5*r, "$=0.$", southwest)



c.writePDFfile("pic-bubble.pdf")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

c = canvas.canvas()

x, y = 0., 0.




#c.writePDFfile("pic-skein3.pdf")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

c = canvas.canvas()

x, y = 0., 0.




#c.writePDFfile("pic-skein3.pdf")



