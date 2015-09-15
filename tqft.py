#!/usr/bin/env python

import sys
import os

from math import *
from random import *

from pyx import canvas, path, deco, trafo, style, text, color, unit, epsfile, deformer, bitmap

from PIL import Image


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


st_tau = [style.linewidth.Thick, red, style.linecap.round]
#st_vac = [style.linewidth.thick, red]+st_dotted


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

dy = 0.5

y = -1.4*dy
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


y = -1.4*dy
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

p = path.circle(0., 0., 1.)
c = canvas.canvas() # [canvas.clip(p)])


t = trafo.translate(-0.8, 0.)
#ellipse(-0.5, 0., 0.5, 2.0, 1., shade, [t])
ellipse(-0.5, 0., 0.5, 2.0, 2., shade, [t])

#g_arrow = [green, deco.earrow(size=0.1)]
g_arrow = []
c.stroke(path.line(-2., 0., 0., 0.), [t]+g_arrow) 

hole(-1.5, 0., 0.07, '', [t])
hole(-1.0, 0., 0.07, '', [t])
hole(-0.5, 0., 0.07, '', [t])

c.text(0.0, -0.3, r"$f$", [text.halign.boxcenter, text.valign.middle])

c.stroke(path.line(-0.5, 0, 0.5, 0),
    [style.linewidth.Thick, deco.earrow(size=0.2)])


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

hole(-0.5, 0., 0.07, '', [t])
hole(-0.0, 0., 0.07, '', [t])
hole(+0.5, 0., 0.07, '', [t])

c.writePDFfile("pic-twist.pdf")
#yield c, "pic-twist.pdf"

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



