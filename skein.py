#!/usr/bin/env python

import sys
from math import *
from random import *
import numpy
import scipy

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
st_round = [style.linecap.round]

st_tau = [style.linewidth.Thick, red, style.linecap.round]
st_vac = [style.linewidth.thick, red]+st_dotted


def dopath(ps, extra=[], fill=[], closepath=False, smooth=0.3, stroke=True):
    ps = [path.moveto(*ps[0])]+[path.lineto(*p) for p in ps[1:]]
    if closepath:
        ps.append(path.closepath())
    p = path.path(*ps)
    if fill:
        c.fill(p, [deformer.smoothed(smooth)]+extra+fill)
    if stroke:
        c.stroke(p, [deformer.smoothed(smooth)]+extra)




st_curve = [green, style.linewidth.THick]
st_curve_arrow = st_curve + [deco.earrow(size=0.2)]


def circle(x, y, r, shade, deco=[], mark=False):
    p = path.circle(x, y, r)
    c.fill(p, [shade])
    c.stroke(p, deco)
    if mark:
        c.fill(path.circle(x, y-r, 0.05))



###############################################################################
#
#

c = canvas.canvas()


def getpoints(x, y, r, h, h0=0., offset=0., dtheta=3*pi/2, reverse=False):
    N = 80
    theta = 0.
    
    pts = []
    while theta <= dtheta:
        x1 = x+r*sin(theta+offset)
        y1 = y+(theta/dtheta)*h
        if y1>=h0:
            pts.append((x1, y1))
        theta += dtheta / N
    if reverse:
        pts = list(reversed(pts))

    return pts


def function(x, y, r, h, h0=0., deco=[], offset=0., dtheta=3*pi/2):
    pts = getpoints(x, y, r, h, h0, offset, dtheta)
    dopath(pts, deco)


sy = 0.2
dx = 1.2

def circ(x, y, txt):
    p = path.circle(x, y, 0.5*r0)
    st_scale = [trafo.scale(x=x, y=y, sx=1., sy=sy)]
    c.fill(p, st_scale+[shade2])
    c.stroke(p, st_scale)
    c.fill(path.circle(x, y-sy*0.5*r0, 0.05))
    c.text(x-0.5*r0, y+0.5*r0, txt, center)

def ucirc():
    x1, y1 = x-dx*r, y-r
    st_scale = [trafo.scale(x=x1, y=y1, sx=1., sy=sy)]

    c.fill(path.circle(x1, y1, 0.5*r0), st_scale+[shade0])
    c.stroke(path.path(path.arc(x1, y1, 0.5*r0, 180., 0.)), st_scale)
    x2, y2 = x1-0.5*dx*sy*r0, y1-0.5*sy*r0
    c.stroke(path.line(x, y, x2, y2))
    c.fill(path.circle(x2, y2, 0.05))
    c.text(x2-0.5*r0, y2-0.5*r0, "$\widehat{c}$", southeast)


w, h = 1.5, 2.5
x, y = 0., 0.

r = 0.3*h # length of ribbon segment
r0 = 0.4*w # width of ribbon


pts00 = [(x-dx*r-0.5*r0, y-r), (x-0.5*r0, y)]
pts0 = getpoints(x-0.5*r0, y, -0.4*w, h)
pts1 = getpoints(x, y, -0.4*w, h)
pts2 = getpoints(x+0.5*r0, y, -0.4*w, h, 0.102*h, reverse=True)
pts20 = [(x+0.5*r0, y), (x-dx*r+0.5*r0, y-r)]

dopath(pts00+pts0+pts2+pts20, fill=[shade0], closepath=True, stroke=False, smooth=0.)
#dopath(pts0+pts2, fill=[shade0], closepath=True, stroke=False)

ucirc()

dopath(pts00+pts0, st_curve+st_round)
dopath(pts1)
dopath(pts2, st_curve+st_round)

#r1 = 0.7*r0
#y0 = 2.*h/3
#p = path.path(
#    path.moveto(x,     y0+r1),
#    path.lineto(x+r1,  y0),
#    path.lineto(x,     y0-r1),
#    path.lineto(x+-r1, y0),
#    path.closepath())
#c.fill(p, [white])

pts0 = getpoints(x-0.5*r0, y, 0.4*w, h, 0.102*h)
pts1 = getpoints(x, y, 0.4*w, h)
pts2 = getpoints(x+0.5*r0, y, 0.4*w, h, reverse=True)
dopath(pts0+pts2, fill=[shade0], closepath=True, stroke=False, smooth=0.)
dopath(pts0+pts2, [shade0]+st_thick, closepath=True, smooth=0.) # cover a seam

dopath(pts0, st_curve+st_round)
dopath(pts1)
dopath(pts2+pts20, st_curve_arrow+st_round)

circ(x-0.4*w, h, "$b$")
circ(x+0.4*w, h, "$a$")


#c.stroke(path.line(x-0.5*r0, y, x-dx*r-0.5*r0, y-r), st_curve+st_round)
#c.stroke(path.line(x+0.5*r0, y, x-dx*r+0.5*r0, y-r),  st_curve_arrow+st_round)

#dopath(pts00, st_curve+st_round)
#dopath(pts20, st_curve_arrow+st_round)

####### >>>>

c.stroke(path.line(x+2*r0, y+r0, x+3*w-2*r0, y+r0), [deco.earrow()])
c.text(x+1.5*w, y+1.8*r0, "$R^{ab}_c$", center)

x += 3*w
y += 0.3*h
h1 = 0.7*h
r = 0.6*h
dx = 0.6

pts00 = [(x-dx*r-0.5*r0, y-r), (x-0.5*r0, y)]
pts0 = getpoints(x-0.5*r0, y, -0.4*w, h1, dtheta=pi/2.)
pts1 = getpoints(x+0.5*r0, y, -0.4*w, h1, 0.77*h1, dtheta=pi/2., reverse=True)
pts2 = getpoints(x-0.5*r0, y, 0.4*w, h1, 0.77*h1, dtheta=pi/2.)
pts3 = getpoints(x+0.5*r0, y, 0.4*w, h1, dtheta=pi/2., reverse=True)
pts30 = [(x+0.5*r0, y), (x-1.03*dx*r+0.5*r0, y-1.03*r)]

dopath(pts00+pts0+pts1+pts2+pts3+pts30, fill=[shade0], closepath=True, stroke=False)

ucirc()

#c.stroke(path.line(x-0.5*r0, y, x-dx*r-0.5*r0, y-r), st_curve+st_round)
#c.stroke(path.line(x+0.5*r0, y, x-dx*r+0.5*r0, y-r), st_curve_arrow+st_round)

dopath(pts00+pts0, st_curve+st_round)
dopath(pts1+pts2, st_curve+st_round)
dopath(pts3+pts30, st_curve_arrow+st_round)


circ(x-0.4*w, h, "$b$")
circ(x+0.4*w, h, "$a$")


pts = getpoints(x, y, -0.4*w, h1, dtheta=pi/2.)
dopath(pts)

pts = getpoints(x, y, 0.4*w, h1, dtheta=pi/2.)
dopath(pts)





c.writePDFfile("pic-rmove-skein.pdf")


