#!/usr/bin/env python

import sys
from math import *

from pyx import canvas, path, deco, trafo, style, text, color, deformer

text.set(mode="latex") 
text.set(docopt="12pt")
#text.preamble(r"\usepackage{amsmath}")
#text.preamble(r"\

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

light_shade = rgb(0.85, 0.65, 0.1)
light_shade = rgb(0.9, 0.75, 0.4)




st_dashed = [style.linestyle.dashed]
st_dotted = [style.linestyle.dotted]

def arrow(x0, y0, x1, y1, extra=[]):
    c.stroke(path.line(x0, y0, x1, y1),
        extra+[deco.earrow(size=0.1)])

#c.stroke(
#    path.curve(0, 0, 0, 4, 2, 4, 3, 3),
#    [style.linewidth.THICK, style.linestyle.dashed, color.rgb.blue,
#    deco.earrow([deco.stroked([color.rgb.red, style.linejoin.round]),
#                       deco.filled([color.rgb.green])], size=1)])

def line(x0, y0, x1, y1, extra=[]):
    c.stroke(path.line(x0, y0, x1, y1), extra)

def varrow(x, y0, y1, extra=[], label=None):
    arrow(x, y0, x, y1, extra)
    if label:
        c.text(x-0.1, (y0+y1)/2., label, [text.halign.boxright])


def harrow(x0, x1, y, extra=[], label=None):
    arrow(x0, y, x1, y, extra)
    if label:
        c.text((x0+x1)/2., y+0.1, label,
            [text.valign.bottom, text.halign.boxcenter])



if 0:
    # -------------------------------------------------
    
    c = canvas.canvas()
    
    c.text(0.0, 1.8, "$L_2$", [])
    c.text(1.8, 1.8, "$D_n$", [])
    harrow(0.6, 1.8, 2.0, label="$g$")
    
    c.text(0.9, 0.0, "$L_n$", [])
    
    arrow(0.2, 1.7, 1.0, 0.5)
    #c.text(0.2, 0.8, "$\subset$", [])
    c.text(0.2, 0.8, "$i$", [])
    
    arrow(1.2, 0.5, 1.9, 1.7)
    c.text(1.6, 0.8, "$\phi f$", [])
    
    c.writeEPSfile("halftwist-factor.eps")
    
    # -------------------------------------------------


#dashed = [style.linestyle.dashed]
#dotted = [style.linestyle.dotted]

dashed = []
dotted = [style.linestyle.dashed]

c = canvas.canvas()


def anyon(x, y):
    c.stroke(path.circle(x, y, 0.05), [red, style.linewidth.thick])

w, h = 2., 2.
m = 0.1

# --------------------------------------------------------------------

x0, y0 = 0.6, h + 10*m

c.text(x0-0.6, y0, "a)")

c.stroke(path.rect(x0, y0, w, h), dashed)
c.stroke(path.rect(x0+w+m, y0, w, h), dotted)

extra = [green, style.linewidth.THick, deco.earrow(size=0.2)]

y = y0+0.3*h
c.stroke(path.line(x0+0.5*w, y, x0+1.5*w+m, y), extra)
anyon(x0+0.8*w, y)
anyon(x0+m+1.2*w, y)
    
y = y0+0.7*h
c.stroke(path.line(x0+1.5*w+m, y, x0+0.5*w, y), extra)
anyon(x0+0.8*w, y)
anyon(x0+m+1.2*w, y)

# --------------------------------------------------------------------

x0, y0 = 0.6, 0.
    
c.text(x0-0.6, y0, "b)")

c.stroke(path.rect(x0, y0, w, h), dashed)
c.stroke(path.rect(x0+w+m, y0, w, h), dotted)


p = path.path(
    path.moveto(x0+0.5*w, y0-0.3*h), 
    path.lineto(x0+0.5*w, y0+0.3*h), 
    path.lineto(x0+1.5*w+m, y0+0.3*h),
    path.lineto(x0+1.5*w+m, y0+0.7*h), 
    path.lineto(x0+0.5*w, y0+0.7*h),
    path.lineto(x0+0.5*w, y0+1.3*h),
)
c.stroke(p, [deformer.smoothed(0.3)]+extra)

y = y0+0.3*h
anyon(x0+0.8*w, y)
anyon(x0+m+1.2*w, y)
    
y = y0+0.7*h
anyon(x0+0.8*w, y)
anyon(x0+m+1.2*w, y)

# --------------------------------------------------------------------

N = 20

def dopath(ps, extra=[], fill=False, closepath=True):
    ps = [path.moveto(*ps[0])]+[path.lineto(*p) for p in ps[1:]]
    if closepath:
        ps.append(path.closepath())
    p = path.path(*ps)
    if fill:
        c.fill(p, [deformer.smoothed(0.3)]+extra+[color.rgb.white])
    c.stroke(p, [deformer.smoothed(0.3)]+extra)

x0, y0 = 3*w + 5*m, -2*m

dx = w
dy = 12*m

r = 0.5*h
ys = [0.2*h, 0.7*h, 1.2*h, 1.7*h]


def braid(x0, y0, x1, y1):
    p = path.line(x0, y0, x1, y1)
    c.stroke(p, [color.rgb.white, style.linewidth.THICk])
    c.stroke(p, [red])

def braid(x0, y0, x1, y1):
    x, y = x0, y0
    dx = (x1-x0)/N
    dy = (y1-y0)/N
    ps = [(x, y)]
    for i in range(N):
        theta = i*2*pi/(N)
        x += dx*(cos(theta)+2) / (2.)
        y += dy
        ps.append((x, y))
    dopath(ps, [color.rgb.white, style.linewidth.THICk], closepath=False)
    dopath(ps, [red], closepath=False)



x1, y1 = x0+dx, y0+dy
perm = [2, 0, 1, 3]
for i in [0, 1, 2, 3]:
    braid(x0, y0+ys[i], x1, y1+ys[perm[i]])

c.text(x0-1.5, 0, "c)")


y2 = y0+0.95*h
ps = []
for i in range(N):
    theta = 2*pi*i / (N-1)
    ps.append((x0+0.4*r*sin(theta), y2+0.9*r*cos(theta)))

dopath(ps, dotted, fill=True)

ps = []
for i in range(N):
    theta = pi + pi*i / (N-1)
    ps.append((x0+0.5*h*sin(theta), y2+0.9*h*cos(theta)))

y1 = ys[-1]+y0
r1 = ps[-1][1]-y1
for i in range(N):
    theta = pi*i / (N-1)
    ps.append((x0+r1*sin(theta), y1+r1*cos(theta)))

r2 = ps[-1][1]-y2
for i in range(N):
    theta = pi - pi*i / (N-1)
    ps.append((x0-0.5*r2*sin(theta), y2-r2*cos(theta)))

y1 = ys[0]+y0
#r1 = ps[-1][1]-y1
for i in range(N):
    theta = pi*i / (N-1)
    ps.append((x0+r1*sin(theta), y1+r1*cos(theta)))

dopath(ps, dashed, fill=True)

c.stroke(path.line(x0, y0, x0, y0+2*h), extra)
for y in ys:
    anyon(x0, y0+y)


# --------------------------------------------------------------------

c.text(x0+1.2, 0.5*dy, "d)")

x0 += dx
y0 += dy

c.stroke(path.line(x0, y0, x0, y0+2*h), extra)

for y in ys:
    anyon(x0, y0+y)

y2 = y0+0.45*h
ps = []
for i in range(N):
    theta = 2*pi*i / (N-1)
    ps.append((x0+0.4*r*sin(theta), y2+0.8*r*cos(theta)))

dopath(ps, dotted)

y2 = y0+1.45*h
ps = []
for i in range(N):
    theta = 2*pi*i / (N-1)
    ps.append((x0+0.4*r*sin(theta), y2+0.8*r*cos(theta)))

dopath(ps, dashed)



c.writePDFfile("pic-syndrome.pdf")




