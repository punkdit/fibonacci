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

x += 1.2*w
c.text(x, y+0.5*h, r"$+ f_k$", west)

x += 0.5*w
frame()

c.stroke(path.line(x, y+0.5*h, x+w, y+0.5*h), st_tau)


c.writePDFfile("pic-kfold.pdf")




