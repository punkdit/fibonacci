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

x += 0.3*w
p = path.circle(x+0.1*w, y+0.5*h, 0.4*r)
c.fill(p, [white])
c.stroke(p)

c.text(x+0.6*w, y+0.5*h, "...")

#c.text(x+0.1*w, y+0.0*h, "$M_a$", west)
c.text(x+0.1*w, y+0.0*h, "$M$", west)

c.text(x+0.3*w, y+0.7*h, "$a$", southwest)

x += 1.8*r

r = 0.7
p = path.circle(x+r, y+0.5*h, r)
c.fill(p, [shade])
c.stroke(p)

x += 0.3*w

c.text(x+0.0*w, y+0.5*h, "...")

#c.text(x+0.0*w, y+0.2*h, "$N_{\hat{a}}$", west)
c.text(x+0.0*w, y+0.2*h, "$N$", west)

c.text(x+0.1*w, y+0.7*h, "$\hat{a}$", southwest)

x += 1.8*r
c.text(x, y+0.5*h, r"$\Bigr)$", east)

x -= 0*r
y -= 3*r

#c.text(x, y+0.5*h, r"$\to\H\Bigl($", east)
c.text(x, y+0.5*h, r"$\xrightarrow{\cong}\H\Bigl($", east)

r = 1.0
#x += 0.5*w

p = path.circle(x+r, y+0.5*h, r)
c.fill(p, [shade])
c.stroke(p)

x += 0.3*w
p = path.circle(x+0.1*w, y+0.5*h, 0.4*r)
c.stroke(p, st_dashed)
c.text(x+0.1*w, y+0.5*h, r"$N$", center)

c.text(x+0.6*w, y+0.5*h, "...")

c.text(x+0.2*w, y+0.0*h, "$M$", west)

x += 1.8*r
c.text(x, y+0.5*h, r"$\Bigr)$", east)


c.writePDFfile("pic-glue.pdf")


