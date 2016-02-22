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


c = canvas.canvas()


R = 2.4
r = 1.0
r1 = 0.10
r2 = 0.4

theta = 0.
dtheta = 2*pi/5


dxs = [-6*r1, -2*r1, +2*r1, +6*r1]


def ellipse(x, y, r, sy):
    c.stroke(path.circle(x, y, r), [trafo.scale(x=x, y=y, sx=1., sy=sy)])


for i in range(5):

    x = -R*sin(theta) # ccw
    y = R*cos(theta)

    fudge = 0.1 if i in [2,3] else 0.0

    p = path.circle(x+fudge, y, r)
    c.fill(p, [shade])
    c.stroke(p)

    c.stroke(path.line(x-r+fudge, y, x+r+fudge, y), st_curve+st_arrow)

    for dx in dxs:
        p = path.circle(x+dx, y, 0.07)
        c.fill(p, [white])
        c.stroke(p)

    def b2(x):
        ellipse(x, y, 0.9*r2, 0.7)
    def b3(x):
        ellipse(x, y, 1.6*r2, 0.8)

    if i==0:
        b2(x+(dxs[0]+dxs[1])/2.)
        b3(x+(dxs[1]+dxs[1])/2.)
    if i==1:
        b2(x+(dxs[1]+dxs[2])/2.)
        b3(x+(dxs[1]+dxs[1])/2.)
    if i==2:
        b2(x+(dxs[1]+dxs[2])/2.)
        b3(x+(dxs[2]+dxs[2])/2.)
    if i==3:
        b2(x+(dxs[2]+dxs[3])/2.)
        b3(x+(dxs[2]+dxs[2])/2.)
    if i==4:
        b2(x+(dxs[2]+dxs[3])/2.)
        b2(x+(dxs[0]+dxs[1])/2.)

    RR = 1.4*R
    x = -RR*sin(theta+0.5*dtheta) # ccw
    y = RR*cos(theta+0.5*dtheta)
    c.text(x, y, "$F$", center)

    w = 72*(i+1.75)
    if i < 3:
        c.stroke(path.path(path.arc(0., 0., 1.2*R, w-10, w+10)), [deco.earrow()])
    else:
        c.stroke(path.path(path.arcn(0., 0., 1.2*R, w+10, w-10)), [deco.earrow()])

    theta += dtheta


    


c.writePDFfile("pic-pentagon.pdf")


